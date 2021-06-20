import streamlit as st

from pathlib import Path
from PIL import Image
from memery.core import queryFlow

from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys


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
    ranked = queryFlow(path, text_query, image_query=img)
    return(ranked)

@st.cache
def send_text_query(path, text_query):
    ranked = queryFlow(path, text_query)
    return(ranked)


st.sidebar.title("Memery")

path = st.sidebar.text_input(label='Directory', value='./images')
text_query = st.sidebar.text_input(label='Text query', value='dad joke')
image_query = st.sidebar.file_uploader(label='Image query')
im_display_zone = st.sidebar.beta_container()
logbox = st.sidebar.beta_container()


sizes = {'small': 115, 'medium':230, 'large':332, 'xlarge':600}

l, m, r = st.beta_columns([4,1,1])
with l:
    num_images = st.slider(label='Number of images',value=12)
with m:
    size_choice = st.selectbox(label='Image width', options=[k for k in sizes.keys()])
with r:
    captions_on = st.checkbox(label="Caption filenames", value=False)

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
    ims = [Image.open(o).convert('RGB') for o in ranked[:num_images]]
    names = [o.replace(path, '') for o in ranked[:num_i`mages]]

    if captions_on:
        images = st.image(ims, width=sizes[size_choice], channels='RGB', caption=names)
    else:
        images = st.image(ims, width=sizes[size_choice], channels='RGB')
