__all__ = ['st_redirect', 'st_stdout', 'st_stderr', 'send_image_query', 'send_text_query', 'path', 'text_query',
           'image_query', 'im_display_zone', 'logbox', 'sizes']

import argparse
# from os import F_ULOCK
# from unittest import skip
import streamlit as st
from memery import core

from pathlib import Path
from PIL import Image

from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys

# Parses the args from the command line
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help='starting directory to search')
    return parser.parse_args(args)

# Initalize session state
args = parse_args(sys.argv[1:])

# Configs
st.set_page_config(page_title='Memery', layout="centered")

# Index the directory
def index(logbox, path):
    if Path(path).exists():
        with logbox:
            with st_stdout('info'):
                    core.index_flow(path)
    else:
        with logbox:
            with st_stdout('warning'):
                print(f'{path} does not exist!')

# Clears out the database and treemap files
def clear_cache(path, logbox):
    root = Path(path)
    if root.exists():
        db = root/'memery.pt'
        treemap = root/'memery.ann'
        if db.exists() or treemap.exists():
            db.unlink(), treemap.unlink()
            with logbox:
                with st_stdout('info'):
                    print("Cache emptied! Removed memery.pt and memery.ann")
        else:
            with logbox:
                st.warning("No cached files found!")
    else:
        with logbox:
            with st_stdout('warning'):
                print(f'{path} does not exist!')

# Runs a search
def search(path, text_query, image_query, image_query_display, image_display_zone, logbox, skipped_files_box, num_images, captions_on, sizes, size_choice):
    if Path(path).exists():
        if text_query or image_query:
            with logbox:
                with st_stdout('info'):
                    if image_query is not None:
                        img = Image.open(image_query).convert('RGB')
                        with image_query_display:
                            st.image(img)
                        ranked = send_image_query(path, text_query, img)
                    else:
                        ranked = send_text_query(path, text_query)

            ims_to_display = {}
            for o in ranked[:num_images]:
                name = o.replace(path, '')
                try:
                    ims_to_display[name] = Image.open(o).convert('RGB')
                except Exception as e:
                    with skipped_files_box:
                        st.warning(f'Skipping bad file: {name}\ndue to {type(e)}')
                        pass
            
            with image_display_zone:
                if captions_on:
                    images = st.image([o for o in ims_to_display.values()], width=sizes[size_choice], channels='RGB', caption=[o for o in ims_to_display.keys()])
                else:
                    images = st.image([o for o in ims_to_display.values()], width=sizes[size_choice], channels='RGB')
        else:
            with logbox:
                with st_stdout('warning'):
                    print('Use a text or image query!')
    else:
        with logbox:
            with st_stdout('warning'):
                print(f'{path} does not exist!')


@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b + '')
                output_func(buffer.getvalue() + '')
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    with st_redirect(sys.stderr, dst):
        yield

@st.cache
def send_image_query(path, text_query, image_query):
    ranked = core.query_flow(path, text_query, image_query)
    return(ranked)

@st.cache
def send_text_query(path, text_query):
    ranked = core.query_flow(path, text_query)
    return(ranked)

# Draw the sidebar
st.sidebar.title("Memery")

settings = st.sidebar.expander(label="Settings", expanded=False)
with settings:
    do_clear_cache = st.button(label="Clear Cache")

dir_l, dir_r = st.sidebar.columns([3,1])
with dir_l:
    path = st.text_input(label='Directory', value=args.root)
with dir_r:
    st.title("")
    do_index = st.button(label="Index", key='do_index')

search_l, search_r = st.sidebar.columns([3,1])
with search_l:
    text_query = st.text_input(label='Text query', value='')
with search_r:
    st.title("")
    search_button = st.button(label="Search", key="search_button")


image_query = st.sidebar.file_uploader(label='Image query')
image_query_display = st.sidebar.container()
logbox = st.sidebar.container()
skipped_files_box = st.sidebar.expander(label='Skipped files', expanded=False)

# Draw the main page
sizes = {'small': 115, 'medium':230, 'large':332, 'xlarge':600}
l, m, r = st.columns([4,1,1])
with l:
    num_images = st.slider(label='Number of images',value=12)

with m:
    size_choice = st.selectbox(label='Image width', options=[k for k in sizes.keys()], index=1)
with r:
    captions_on = st.checkbox(label="Caption filenames", value=False)
image_display_zone = st.container()

# Decide which actions to take
if search_button or text_query or image_query and not do_clear_cache:
    search(path, text_query, image_query, image_query_display, image_display_zone, logbox, skipped_files_box, num_images, captions_on, sizes, size_choice)
if do_index:
    index(logbox, path)
if do_clear_cache:
    clear_cache(path, logbox)
