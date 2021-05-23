# memery
> Search over large image datasets with natural language and computer vision!


## Install

The necessary CLIP and torch packages will be installed by pip. You might want to make sure you have a sane CUDA environment before and after this step if you're trying to use GPU. If you don't have a GPU, `memery` should still work on your CPU. 

If you have any trouble please **open an issue**! I want to make this package useful for as many people as possible. Help me know what's going wrong :)

`pip install memery`

## How to use

### Use GUI

The browser GUI is a Voilá app, which basically runs a Jupyter notebook without showing any of the code cells. To use this way, navigate to your `memery` folder in a terminal and run:

`voila serve app.ipynb`

If you're in a Jupyter environment, you can summon the GUI directly into an output cell like this:


```python
from memery.gui import appPage

```

```python
app = appPage()
display(app)
```


    <memery.gui.appPage at 0x7f6c0e7c80d0>


### Use CLI

From the command line, you can use `memery` on any folder and it will search for images recursively, returning a list object to stdout.

Pass the --n flag to control how many images are returned (default 10).

`memery PATH/TO/IMAGE/FOLDER 'query' --n 20
`

### Use as a library

Simply use `queryFlow` to search over a folder recursively! The folder will be indexed, if an index doesn't already exist. Then any new images will be CLIP-encoded, an Annoy treemap built, and a list of ranked filenames returned.

```python
from memery.core import queryFlow
from memery.gui import get_grid
```

```python
ranked = queryFlow('./images', 'dad joke')
```

    Searching 78 images


```python
get_grid(ranked, n=3)
```

```python
print(ranked[:5])
```

    ['images/Wholesome-Meme-68.jpg', 'images/Wholesome-Meme-74.jpg', 'images/Wholesome-Meme-88.jpg', 'images/Wholesome-Meme-78.jpg', 'images/Wholesome-Meme-23.jpg']


## TODO:

- Documentation and tests in notebooks
- Optimize GUI to cache results of searches
- Optimize the image loader and number of trees based on memory and db size
- Type annotations
- Search/browse by image or image+text
- Tags and filters
- Native GUI frontend client for various platforms
- Distributed server backend

## DONE:
- _Code for joining archived data to new data_
- _Code for saving indexes to archive_
- _Flows_
- _Cleanup repo_
- _CLI_
- _interactive GUI_
