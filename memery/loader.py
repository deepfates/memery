__all__ = ['slugify', 'get_image_files', 'verify_image', 'device', 'archive_loader', 'db_loader', 'treemap_loader']

from pathlib import Path
from PIL import Image
from tqdm import tqdm

def slugify(filepath):
    return f'{filepath.stem}_{str(filepath.stat().st_mtime).split(".")[0]}'

def get_image_files(path):
    img_extensions = {'.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp'}
    return [(f, slugify(f)) for f in tqdm(path.rglob('*')) if f.suffix in img_extensions]

def get_valid_images(path):
    filepaths = get_image_files(path)
    return [f for f in filepaths if verify_image(f[0])]

# This returns boolean and should be called is_valid_image or something like that
def verify_image(f):
    try:
        img = Image.open(f)
        img.verify()
        return(True)
    except Exception as e:
        print(f'Skipping bad file: {f}\ndue to {type(e)}')
        pass


import torch
import torchvision

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device

def archive_loader(filepaths, root, device):
    dbpath = root/'memery.pt'
#     dbpath_backup = root/'memery.pt'
    db = db_loader(dbpath, device)

    current_slugs = [slug for path, slug in filepaths]
    archive_db = {i:db[item[0]] for i, item in enumerate(db.items()) if item[1]['slug'] in current_slugs}
    archive_slugs = [v['slug'] for v in archive_db.values()]
    new_files = [(str(path), slug) for path, slug in filepaths if slug not in archive_slugs and verify_image(path)]

    return(archive_db, new_files)

def db_loader(dbpath, device):

    # check for savefile or backup and extract
    if Path(dbpath).exists():
        db = torch.load(dbpath, device)
#     elif dbpath_backup.exists():
#         db = torch.load(dbpath_backup)
    else:
        db = {}
    return(db)

from annoy import AnnoyIndex

def treemap_loader(treepath):
    treemap = AnnoyIndex(512, 'angular')

    if treepath.exists():
        treemap.load(str(treepath))
    else:
        treemap = None
    return(treemap)

if __name__ == '__main__':
    print('TESTING')