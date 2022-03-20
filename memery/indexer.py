__all__ = ['join_all', 'build_treemap', 'save_archives']

def join_all(db, new_files, new_embeddings):
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

from annoy import AnnoyIndex

def build_treemap(db):
    treemap = AnnoyIndex(512, 'angular')
    for k, v in db.items():
        treemap.add_item(k, v['embed'])

    # Build the treemap, with 5 trees rn
    treemap.build(5)

    return(treemap)


import torch

def save_archives(root, treemap, db):
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