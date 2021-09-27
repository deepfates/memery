# memery
> Search over large image datasets with natural language and computer vision!


*^ that is so nerdy. can we do something like "Local-first AI image search"? or is that still too opaque*

![meme about having too many memes](images/E2GoeMyWEAAkcLz.jpeg)

The problem: you have a huge folder of images. Memes, screenshots, datasets, product photos, inspo albums, anything. You know that somewhere in that folder is the exact image you want, but you can't remember the filename or what day you saved it. There's nothing you can do buit scroll through the folder, skimming hundreds of thumbnails, hoping you don't accidentally miss it, hoping you'll recognize it when you do see it. 

Humans do this amazingly well. But even with computers, local image search is still a manual effort - you're still sorting through folders of images, like an archivist of old.

**Until memery**.

The `memery` package provides natural language search over local images. You can use it to search for things like "a line drawing of a woman facing to the left" and get _reasonably good results!_ 

You can do this over thousands of images (it's not optimized for performance yet, but search times scale well under O(n)). 

You can view the images in a browser GUI, or pipe them through command line tools. 

You can use `memery` or its modules in Jupyter notebooks, including GUI functions! 

Under the hood, `memery` makes use of **CLIP**, the [Contrastive Language-Image Pretraining transformer](https://github.com/openai/CLIP), released by OpenAI in 2021. CLIP trains a vision transformer and a language transformer to find the same latent space for images and their captions. This makes it perfect for the purpose of natural language image search. CLIP is a giant achievement, and `memery` stands on its shoulders.

Outline:
- Usage
  - Install locally
  - Use GUI
  - Use CLI
  - Use in Jupyter
  - Use the library
- Development
  - Notebook-driven development
  - Pull the repo
  - Branch and install
  - Notebook-driven development
  - Change the notebooks
  - Test the notebooks
  - Notebook-driven development
  - Tangle the source code
  - Weave the documentation
- Contributing
  - Who works on this project
  - How you can help
  - What we don't do
  - Thanks

## Install

The necessary CLIP and torch packages will be installed by pip.

*what does this mean? why are you telling me this? what if they aren't?*

You might want to make sure you have a sane CUDA environment before and after this step if you're trying to use GPU. If you don't have a GPU, `memery` should still work on your CPU.

*this is backwards and also impenetrable if you're not a nerd*

If you have any trouble please **open an issue on Github**! I want to make this package useful for as many people as possible. Help me know what's going wrong :) 

*still true, pretty clear. use emoji or go home though*

*This is the crucial command, huh? Seems a little far down the page. Maybe a quick-start section earlier, then a more in-depth Installation section here*

`pip install memery`

If you don't have a GPU for PyTorch, this command might help:
`pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`

*did you scrape this from stackoverflow? or the CLIP source code or what. it looks very specific and arbitrary. I think it's meant to install pytorch CPU version, but the average user shouldn't have to know that! if you are trying to use CUDA and GPU it should be an easy toggle, and if you're a regular person wihtout a data science project you shouldn't have to go through a bunch of weird command line stuff.*

*In fact, how can we package this in a way that you don't have to type a single command? There has to be ways to wrap up a whole python setup and install it on a different computer, with all the same dependencies. Right? Ugh, unfortunately this is Python, so it might not exist. But I can at least scale the difficulty level with the user story.*

*Yes, user stories. We have to think about the interface between human and computer as another API, and look for the endpoints we can serve to different users with different protocols.*

*This means thinking about the reasons people come to the program, and how they expect it to respond. Currently I see three user stories:* 
 * *i have images and want to search them with a GUI app*
   * *streamlit GUI*
 * *i have a program/workflow and want to use image search as one part of it*
   * *CLI tool*
   * *python module*
   * *jupyter GUI*
 * *i want to improve on and/or contribute to memery development*
   * *clone the repo*
   

*Each one has an increasing level of complexity and expected knowledge.*

## How to use

### Use GUI

The browser GUI is a Streamlit app. You can run it from the command line with 

`memery serve`

or set up a desktop shortcut to use it from your menu.


*Why do I have to use a CLI to get a GUI? This is very annoying. In any case, this does not provide instructuions on how to use the GUI or any of its particular quirks. There should be a screenshot, also*

If you're in a Jupyter environment, you can summon an ipywidgets GUI directly into an output cell like this:


```python
from memery.gui import appPage

```

```python
app = appPage()
display(app)
```


    <memery.gui.appPage at 0x7ff3072db110>


*This doesn't transfer to the README, so it should be fixed or be scrapped. Screenshots would work fine. Also I'm not sure if the interactive widgets would make sense without a kernel behind them anyway.*

### Use CLI

From the command line, you can use `memery` on any folder and it will search for images recursively, returning a list object to stdout.

*Why is it that behavior? Is it possible to make it not recursive? What is the usual behavior of a search in POSIX? What is the use case for a CLI memery: is it shell scripts? in-console image browsing? risk-tolerant batch modification? Think about this further*

*at least you can control how much output it spews to your terminal*

Pass the --n flag to control how many images are returned (default 10).

`memery recall PATH/TO/IMAGE/FOLDER 'query' --n 20
`

### Use as a library

*the following paragrah cannot be comprehended by any human mind. if you can even read to the end of it you should go touch grass*

Simply use `queryFlow` to search over a folder recursively! The folder will be indexed, if an index doesn't already exist. Then any new images will be CLIP-encoded, an Annoy treemap built, and a list of ranked filenames returned.

*okay, we survived. What are we supposed to say here instead?*

*I think what he's trying to get at is explaining the underlying mechanism of the search. Really all we need here is a function signature, as anyone who's going to use it as a library will probably also be looking at the docs for further information. Have a link here too, that goes to the `core` file where the main flows and executors are explained.*

```python
from memery.core import queryFlow
from memery.gui import get_grid
```

```python
ranked = queryFlow('./images', 'dad joke')

print(ranked[:5])
```

---

*Okay, now we need a whole part about development.

---

*Compile this notebook*

```python
from nbdev.export import notebook2script; notebook2script()

```

    Converted 00_core.ipynb.
    Converted 01_loader.ipynb.
    Converted 02_crafter.ipynb.
    Converted 03_encoder.ipynb.
    Converted 04_indexer.ipynb.
    Converted 05_ranker.ipynb.
    Converted 06_fileutils.ipynb.
    Converted 07_cli.ipynb.
    Converted 08_jupyter_gui.ipynb.
    Converted 09_streamlit_app.ipynb.
    Converted index.ipynb.

