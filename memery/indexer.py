from annoy import AnnoyIndex
import torch

def join_all(db, new_files, new_embeddings) -> dict:
    start = len(db)
    for i, file in enumerate(new_files):
        path, hash = file
        index = i + start
        db[index] = {
            'hash': hash,
            'fpath': path,
            'embed': new_embeddings[i],
        }
    return(db)

def build_treemap(db) -> AnnoyIndex:
    treemap = AnnoyIndex(512, 'angular')
    for k, v in db.items():
        treemap.add_item(k, v['embed'])

    # Build the treemap, with 5 trees rn
    treemap.build(5)

    return(treemap)


def save_archives(root, treemap, db) -> tuple[str, str]:
    dbpath = root/'memery.pt'
    if dbpath.exists():
#         dbpath.rename(root/'memery-bak.pt')
        dbpath.unlink()
    torch.save(db, dbpath)

    treepath = root/'memery.ann'
    if treepath.exists():
#         treepath.rename(root/'memery-bak.ann')
        treepath.unlink()
    treemap.save(str(treepath))

    return(str(dbpath), str(treepath))