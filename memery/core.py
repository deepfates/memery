__all__ = ['index_flow', 'query_flow']

# Builtins 
import time
from pathlib import Path

# Machine Learning
import torch
from torch import Tensor, device
from torchvision.transforms import Compose

# Local imports
from memery import loader, crafter, encoder, indexer, ranker

class Memery():
    def __init__(self):
        self.index = None
        self.db = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        

    def index_flow(self, path: str):
        '''Indexes images in path, returns the location of save files'''
        start_time = time.time()
        root = Path(path)
        device = self.device

        # Check if we should re-index the files
        print("Checking files")
        dbpath = root/'memery.pt'
        db = loader.db_loader(dbpath, device)
        treepath = root/'memery.ann'
        treemap = loader.treemap_loader(treepath)
        filepaths = loader.get_valid_images(root)
        
        db_set = set([o['hash'] for o in db.values()])
        fp_set = set([o for _, o in filepaths])

        if treemap == None or db_set != fp_set:
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
            treemap = indexer.build_treemap(db)

            print(f"Saving {len(db)} encodings")
            save_paths = indexer.save_archives(root, treemap, db)
        else:
            save_paths = (str(dbpath), str(treepath))

        print(f"Done in {time.time() - start_time} seconds")

        return(save_paths)


    def query_flow(self, path: str, query: str=None, image_query: Tensor=None, reindex: bool=False):
        '''
        Indexes a folder and returns file paths ranked by query.

        Parameters:
            path (str): Folder to search
            query (str): Search query text
            image_query (Tensor): Search query image(s)
            reindex (bool): Reindex the folder if True
        Returns:
            list of file paths ranked by query
        '''
        start_time = time.time()
        root = Path(path)
        device = self.device

        dbpath = root/'memery.pt'
        treepath = root/'memery.ann'
        treemap = loader.treemap_loader(Path(treepath))
        db = loader.db_loader(dbpath, device)

        # Rebuild the tree if it doesn't
        if reindex==True or len(db) == 0 or treemap == None:
            print('Indexing')
            dbpath, treepath = self.index_flow(root)
            treemap = loader.treemap_loader(Path(treepath))
            db = loader.db_loader(dbpath, device)

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

    def get_model(self):
        '''
        Gets a new clip model if not initialized

        Parameters:
            path (str): Path to model
        '''
        if self.model == None:
            self.model = encoder.load_model(self.device)
        return self.model

    def get_index(self):
        '''
        Gets a new index if not initialized

        Parameters:
            path (str): Path to index
        '''
        if self.index == None:
            self.index = loader.treemap_loader(self.treepath)
        return self.index

    def get_db(self, dbpath: str):
        '''
        Gets a new db if not initialized

        Parameters:
            path (str): Path to db
        '''
        if self.db == None:
            self.db = loader.db_loader(dbpath, self.device)
        return self.db
