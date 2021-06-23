# memery
> Search over large image datasets with natural language and computer vision!


## Install

The necessary CLIP and torch packages will be installed by pip. You might want to make sure you have a sane CUDA environment before and after this step if you're trying to use GPU. If you don't have a GPU, `memery` should still work on your CPU. 

If you have any trouble please **open an issue on Github**! I want to make this package useful for as many people as possible. Help me know what's going wrong :)

`pip install memery`

If you don't have a GPU for PyTorch, this command might help
    
`pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`


## How to use

### Use GUI

The browser GUI is a Streamlit app. You can run it from the command line with 

`memery serve`

or set up a desktop shortcut to use it from your menu.

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

`memery recall PATH/TO/IMAGE/FOLDER 'query' --n 20
`

### Use as a library

Simply use `queryFlow` to search over a folder recursively! The folder will be indexed, if an index doesn't already exist. Then any new images will be CLIP-encoded, an Annoy treemap built, and a list of ranked filenames returned.

```python
from memery.core import queryFlow
from memery.gui import get_grid
```

```python
ranked = queryFlow('./images', 'dad joke')

print(ranked[:5])
```
