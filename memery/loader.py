# Builtins
from pathlib import Path
from typing import Any

# External
from PIL import Image
import torch
from torch import device
from annoy import AnnoyIndex

# We take the filename and last modified time to check for modified images
def hash_path(filepath: str) -> str:
    return f'{filepath.stem}_{str(filepath.stat().st_mtime).split(".")[0]}'

def get_image_files(path: Path) -> list[str]:
    img_extensions = {'.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp'}
    return [(f, hash_path(f)) for f in path.rglob('*') if f.suffix in img_extensions]

def get_valid_images(path: Path) -> list[str]:
    filepaths = get_image_files(path)
    return [f for f in filepaths if verify_image(f[0])]

def verify_image(f: str):
    try:
        img = Image.open(f)
        img.verify()
        return(True)
    except Exception as e:
        print(f'Skipping bad file: {f}\ndue to {type(e)}')
        pass

def archive_loader(filepaths: list[str], db: Any) -> tuple[ set[str], list[str] ]: # Just guessing on the return type

    current_hashes = [hash for path, hash in filepaths]
    archive_db = {i:db[item[0]] for i, item in enumerate(db.items()) if item[1]['hash'] in current_hashes}
    archive_hashes = [v['hash'] for v in archive_db.values()]
    new_files = [(str(path), hash) for path, hash in filepaths if hash not in archive_hashes and verify_image(path)]

    return(archive_db, new_files)

def db_loader(dbpath: str, device: device) -> Any:
    '''
    Loads a .pt file
    '''
    if Path(dbpath).exists():
        db = torch.load(dbpath, device)
    else:
        db = {}
    return(db)

def treemap_loader(treepath: str) -> AnnoyIndex:
    '''
    Loads a .ann file
    '''
    treemap = AnnoyIndex(512, 'angular')
    treepath = Path(treepath)
    if treepath.exists():
        treemap.load(str(treepath))
    else:
        treemap = None
    return(treemap)

if __name__ == '__main__':
    print('TESTING')