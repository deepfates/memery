__all__ = ['index_flow', 'query_flow']

import time
import torch

from pathlib import Path
from .loader import get_image_files, get_valid_images, archive_loader, db_loader, treemap_loader
from .crafter import crafter, preproc
from .encoder import image_encoder, text_encoder, image_query_encoder
from .indexer import join_all, build_treemap, save_archives
from .ranker import ranker, nns_to_files

def index_flow(path):
    '''Indexes images in path, returns the location of save files'''
    root = Path(path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Loading
    filepaths = loader.get_image_files(root)
    archive_db = {}

    archive_db, new_files = loader.archive_loader(filepaths, root, device)
    print(f"Loaded {len(archive_db)} encodings")
    print(f"Encoding {len(new_files)} new images")

    # Crafting and encoding
    crafted_files = crafter.crafter(new_files, device)
    new_embeddings = encoder.image_encoder(crafted_files, device)

    # Reindexing
    db = indexer.join_all(archive_db, new_files, new_embeddings)
    print("Building treemap")
    t = indexer.build_treemap(db)

    print(f"Saving {len(db)} encodings")
    save_paths = indexer.save_archives(root, t, db)

    return(save_paths)

def query_flow(path, query=None, image_query=None):
    '''
    Indexes a folder and returns file paths ranked by query.

    Parameters:
        path (str): Folder to search
        query (str): Search query text
        image_query (Tensor): Search query image(s)

    Returns:
        list of file paths ranked by query
    '''
    start_time = time.time()
    root = Path(path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Check if we should re-index the files
    print("Checking files")
    dbpath = root/'memery.pt'
    db = loader.db_loader(dbpath, device)
    treepath = root/'memery.ann'
    treemap = treemap_loader(treepath)
    filepaths = get_valid_images(root)

    # # Rebuild the tree if it doesn't
    # if treemap == None or len(db) != len(filepaths):
    #     print('Indexing')
    #     dbpath, treepath = index_flow(root)
    #     treemap = loader.treemap_loader(Path(treepath))
    #     db = loader.db_loader(dbpath, device)

    # Convert queries to vector
    print('Converting query')
    if image_query:
        img = crafter.preproc(image_query)
    if query and image_query:
        text_vec = encoder.text_encoder(query, device)
        image_vec = encoder.image_query_encoder(img, device)
        query_vec = text_vec + image_vec
    elif query:
        query_vec = encoder.text_encoder(query, device)
    elif image_query:
        query_vec = encoder.image_query_encoder(img, device)
    else:
        print('No query!')

    # Rank db by query
    print(f"Searching {len(db)} images")
    indexes = ranker.ranker(query_vec, treemap)
    ranked_files = ranker.nns_to_files(db, indexes)

    print(f"Done in {time.time() - start_time} seconds")

    return(ranked_files)

