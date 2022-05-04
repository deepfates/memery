# Builtins 
import time
from pathlib import Path
import logging

# Dependencies
import torch
from torch import Tensor, device
from torchvision.transforms import Compose
from PIL import Image


# Local imports
from memery import loader, crafter, encoder, indexer, ranker

class Memery():
    def __init__(self, root: str = None):
        self.index_file = 'memery.ann'
        self.db_file = 'memery.pt'
        self.root = None
        self.index = None
        self.db = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def index_flow(self, root: str, num_workers=0) -> tuple[str, str]:
        '''Indexes images in path, returns the location of save files'''

        start_time = time.time()
        if self.root != root:
            self.root = root
            self.reset_state()
        
        path = Path(root)
        device = self.device

        # Check if we should re-index the files
        print("Checking files")
        dbpath = path/self.db_file
        db = self.get_db(str(dbpath))
        treepath = path/self.index_file
        treemap = self.get_index(str(treepath))
        filepaths = loader.get_valid_images(path)
        
        db_set = set([o['hash'] for o in db.values()])
        fp_set = set([o for _, o in filepaths])

        if treemap == None or db_set != fp_set:
            archive_db = {}

            archive_db, new_files = loader.archive_loader(filepaths, db)
            print(f"Loaded {len(archive_db)} encodings")
            print(f"Encoding {len(new_files)} new images")

            # Crafting and encoding
            crafted_files = crafter.crafter(new_files, device, num_workers=num_workers)
            model = self.get_model()
            new_embeddings = encoder.image_encoder(crafted_files, device, model)

            # Reindexing
            db = indexer.join_all(archive_db, new_files, new_embeddings)
            print("Building treemap")
            treemap = indexer.build_treemap(db)

            print(f"Saving {len(db)} encodings")
            save_paths = indexer.save_archives(path, treemap, db)

        else:
            save_paths = (str(dbpath), str(treepath))
        self.reset_state()
        print(f"Done in {time.time() - start_time} seconds")

        return(save_paths)

    def query_flow(self, root: str, query: str=None, image_query: str=None, reindex: bool=False) -> list[str]:
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

        if self.root != root:
            self.root = root
            self.reset_state()
        path = Path(root)
        device = self.device

        dbpath = path/self.db_file
        treepath = path/self.index_file
        treemap = self.get_index(treepath)
        db = self.get_db(dbpath)

        # Rebuild the tree if it doesn't exist
        if reindex==True or len(db) == 0 or treemap == None:
            print('Indexing')
            dbpath, treepath = self.index_flow(path)
            self.reset_state()
            treemap = self.get_index(treepath)
            db = self.get_db(dbpath)

        model = self.get_model()
        # Convert queries to vector
        print('Converting query')
        if image_query:
            image_query = Image.open(image_query).convert('RGB')
            img = crafter.preproc(image_query)
        if query and image_query:
            text_vec = encoder.text_encoder(query, device, model)
            image_vec = encoder.image_query_encoder(img, device, model)
            query_vec = text_vec + image_vec
        elif query:
            query_vec = encoder.text_encoder(query, device, model)
        elif image_query:
            query_vec = encoder.image_query_encoder(img, device, model)
        else:
            print('No query!')

        # Rank db by query
        print(f"Searching {len(db)} images")
        indexes = ranker.ranker(query_vec, treemap)
        ranked_files = ranker.nns_to_files(db, indexes)
        print(f"Done in {time.time() - start_time} seconds")

        return(ranked_files)

    def clean(self, root: str) -> None:
        '''
        Removes all files produced by Memery
        '''
        return None

    def get_model(self):
        '''
        Gets a new clip model if not initialized
        '''
        if self.model == None:
            self.model = encoder.load_model(self.device)
        return self.model

    def get_index(self, treepath: str):
        '''
        Gets a new index if not initialized

        Parameters:
            path (str): Path to index
        '''
        if self.index == None:
            self.index = loader.treemap_loader(treepath)
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

    def reset_state(self) -> None:
        '''
        Resets the index and db
        '''
        self.index = None
        self.db = None