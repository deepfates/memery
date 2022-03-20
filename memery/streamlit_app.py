__all__ = ['st_redirect', 'st_stdout', 'st_stderr', 'send_image_query', 'send_text_query', 'path', 'text_query',
           'image_query', 'im_display_zone', 'logbox', 'sizes']

import argparse
import streamlit as st
from memery import core

from pathlib import Path
from PIL import Image

from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help='starting directory to search', default='./images')
    return parser.parse_args(args)

args = parse_args(sys.argv[1:])

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
    ranked = core.query_flow(path, text_query, image_query=img)
    return(ranked)

@st.cache
def send_text_query(path, text_query):
    ranked = core.query_flow(path, text_query)
    return(ranked)


st.sidebar.title("Memery")

dir_l, dir_r = st.sidebar.columns([3,1])
with dir_l:
    path = st.text_input(label='Directory', value=args.root)
with dir_r:
    st.title("")
    do_index = st.button(label="Index")

search_l, search_r = st.sidebar.columns([3,1])
with search_l:
    text_query = st.text_input(label='Text query', value='')
with search_r:
    st.title("")
    do_search = st.button(label="Search")

image_query = st.sidebar.file_uploader(label='Image query')
im_display_zone = st.sidebar.container()
logbox = st.sidebar.container()

sizes = {'small': 115, 'medium':230, 'large':332, 'xlarge':600}

l, m, r = st.columns([4,1,1])
with l:
    num_images = st.slider(label='Number of images',value=12)
with m:
    size_choice = st.selectbox(label='Image width', options=[k for k in sizes.keys()], index=1)
with r:
    captions_on = st.checkbox(label="Caption filenames", value=False)

if text_query or image_query or do_search:
    if text_query or image_query:
        with logbox:
            with st_stdout('info'):
                if image_query is not None:
                    img = Image.open(image_query).convert('RGB')
                    with im_display_zone:
                        st.image(img)
                    ranked = send_image_query(path, text_query, image_query)
                else:
                    ranked = send_text_query(path, text_query)

        ims_to_display = {}
        for o in ranked[:num_images]:
            name = o.replace(path, '')
            try:
                ims_to_display[name] = Image.open(o).convert('RGB')
            except Exception as e:
                print(e)
                pass
        
        if captions_on:
            images = st.image([o for o in ims_to_display.values()], width=sizes[size_choice], channels='RGB', caption=[o for o in ims_to_display.keys()])
        else:
            images = st.image([o for o in ims_to_display.values()], width=sizes[size_choice], channels='RGB')
    else:
        with logbox:
            with st_stdout('warning'):
                print('Use a text or image query!')

if do_index:
    with logbox:
        with st_stdout('info'):
            core.index_flow(path)
