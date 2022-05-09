# Memery
> Use human language to search your image folders!

## What is memery?

![meme about having too many memes](images/E2GoeMyWEAAkcLz.jpeg)

The problem: you have a huge folder of images. Memes, screenshots, datasets, product photos, inspo albums, anything. You know that somewhere in that folder is the exact image you want, but you can't remember the filename or what day you saved it. There's nothing you can do but scroll through the folder, skimming hundreds of thumbnails, hoping you don't accidentally miss it, and that you'll recognize it when you do see it. 

Humans do this amazingly well. But even with computers, local image search is still a manual effort - you're still sorting through folders of images, like an archivist of old.

**Now there's Memery**.

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
  - Use the library
- Development
- Contributing
  - Who works on this project

## Installation

With Python 3.9 or greater:

From github (recommended)
```
pip install git+https://github.com/deepfates/memery.git
```
or
```
git clone https://github.com/deepfates/memery.git
cd memery
poetry install
```
From PyPi
```
pip install memery
pip install git+https://github.com/openai/CLIP.git
```

Currently memery defaults to GPU installation. This will 
probably be switched in a future version. 

For now, if you want to run CPU-only, run the following command after installing memery:

`pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`

Someday memery will be packaged in an easy to use format, but since this is a Python project it is hard to predict when that day will be.

If you want to help develop memery, you'll need to clone the repo. See below.

## Usage

What's your use case? 

**I have images and want to search them with a GUI app**
   
   ↳  Use the Browser GUI
   
**i have a program/workflow and want to use image search as one part of it**
   
   ↳ Use as a Python module
   
   ↳ Use from command line or shell scripts
   
**i want to improve on and/or contribute to memery development**
 
   ↳ Start by cloning the repo 

### Use GUI

Currently memery has a rough browser-based GUI. To launch it, run the following in a command line: 

```memery serve```

or set up a desktop shortcut that points to the above command.

Optionally, you can pass a directory to open on startup, like so:

```memery serve home/user/Pictures/memes```

Relative directories will also work:

```
cd ~/Pictures
memery serve memes
```

The default directory passed will be `./images`, which is memery's example meme directory.

Memery will open in a browser window. The interface is pretty straightforward, but it has some quirks.

![screenshot of memery GUI displaying wholesome memes](images/streamlit-screenshot.png)

The sidebar on the left controls the location and query for the search. The "Directory" box requires a full directory path; unfortunately, Streamlit does not yet have a folder-picker component. The path is relative to your current working directory when you run `memery serve`.

The search will run once you enter a text or image query. If you enter both text and image queries, memery will search for the combination.

Beneath these widgets is the output area for temporary messages displayed with each search. Mostly this can be ignored.

The right hand panel displays the images and associated options. Major errors will appear here as giant stack traces; sometimes, changing variables in the other widgets will fix these errors live. If you get a large error here it's helpful to take a screenshot and share it with us in Github Issues.

### Use CLI

The memery command line matches the core functionality of memery.

Use the `recall` command to search for images, passing the path and optionally passing the -n flag to control how many images are returned (default 10). Use the -t flag to pass a text query and the -i flag to pass an image query or both

```
memery recall PATH/TO/IMAGE/FOLDER -t 'text_query' -i 'PATH/TO/IMAGE.jpg' -n 20
```

You can encode and index all the images with the `build` command, optionally specifying the number of workers to build the dataset with (default 0)

```
memery build PATH/TO/IMAGE/FOLDER --workers 4
```

Clear out the encodings and index using the `purge` command

```
memery purge PATH/TO/IMAGE/FOLDER`
```

### Use as a library

The core functionality of memery is wrapped into the Memery() class 

```
from memery.core import Memery
memery = Memery()
```

The function currently called `query_flow` accepts a folder name and a query and returns a ranked list of image files. You can query with text or a filepath to an image or both. 


```
ranked = memery.query_flow('./images', 'dad joke')

print(ranked[:5])
```
```
Converting query
Searching 82 images
Done in 4.014755964279175 seconds
['images/memes/Wholesome-Meme-68.jpg', 'images/memes/Wholesome-Meme-74.jpg', 'images/memes/Wholesome-Meme-88.jpg', 'images/memes/Wholesome-Meme-78.jpg', 'images/memes/Wholesome-Meme-23.jpg']
```

Here's the first result from that list:

![](images/memes/Wholesome-Meme-68.jpg)


So that's how to use memery. Let's look at how you can help make it better.

## Development

### Pull the repo

Clone this repository from Github:

`git clone https://github.com/deepfates/memery.git`


### Install dependencies and memery
Enter the `memery` folder and install requirements:

```
cd memery
poetry install
```

And finally install your local, editable copy of memery with 

`pip install -e .`

## Contributing

Memery is open source and you can contribute. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how you can help.

### Who works on this project

Memery was first written by Max Anton Brewer aka @deepfates in the summer of 2021. Some commits are listed from @robotface-io but that was just me using the wrong account when I first started. 

Many UI and back-end improvements were added by @wkrettek in 2022! 🙌🎉🌟 

I wrote this to solve my own needs and learn notebook-based development. I hope it helps other people too. If you can help me make it better, please do. I welcome any contribution, guidance or criticism.

**The ideal way to get support is to open an issue on Github**. However, the *fastest* way to get a response from me is probably to [direct message me on twitter](twitter.com/deepfates).

