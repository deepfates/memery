# Builtins
from pathlib import Path
from PIL import Image
from io import StringIO, BytesIO
import sys
import argparse
from threading import current_thread
from contextlib import contextmanager
import zipfile

# Local
from memery.core import Memery

# Dependencies
import streamlit as st
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME


# Parses the args from the command line
def parse_args(args: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help='starting directory to search')
    return parser.parse_args(args)

# Initalize session state
args = parse_args(sys.argv[1:])
if 'memery' not in st.session_state:
    st.session_state['memery'] = Memery()
memery: Memery = st.session_state['memery']

# Configs
st.set_page_config(page_title='Memery', layout="centered")

# Draw the sidebar
st.sidebar.title("Memery")

settings = st.sidebar.expander(label="Settings", expanded=False)
with settings:
    do_clear_cache = st.button(label="Clear Cache")
    num_workers = st.slider(label="Number of workers", max_value=8)

dir_l, dir_r = st.sidebar.columns([3,1])
with dir_l:
    path = st.text_input(label='Directory', value=args.root)
with dir_r:
    st.title("")
    do_index = st.button(label="Index", key='do_index')

search_l, search_r = st.sidebar.columns([3,1])
with search_l:
    text_query = st.text_input(label='Text query', value='')
    negative_text_query = st.text_input(label='Negative Text query', value='')
with search_r:
    st.title("")
    search_button = st.button(label="Search", key="search_button")


image_query = st.sidebar.file_uploader(label='Image query')
image_query_display = st.sidebar.container()
if image_query: # Display the image query if there is one
    img = Image.open(image_query).convert('RGB')
    with image_query_display:
        st.image(img)
logbox = st.sidebar.empty()
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

# Index the directory
def index(logbox, path, num_workers):
    if Path(path).exists():
        with logbox:
            with st_stdout('info'):
                    memery.index_flow(path, num_workers)
    else:
        with logbox:
            with st_stdout('warning'):
                print(f'{path} does not exist!')

# Clears out the database and treemap files
def clear_cache(root, logbox):
    memery.clean(root)
    with logbox:
        with st_stdout('info'):
            print("Cleaned database and index files")

# Runs a search
def search(root, text_query, negative_text_query, image_query, image_display_zone, skipped_files_box, num_images, captions_on, sizes, size_choice):
    if not Path(path).exists():
        with logbox:
            with st_stdout('warning'):
                print(f'{path} does not exist!')
                return
    with logbox:
        with st_stdout('info'):
            ranked = memery.query_flow(root, text_query, negative_text_query, image_query)  # Modified line
    ims_to_display = {}
    full_paths = {}  # Store full paths for download functionality
    size = sizes[size_choice]
    for o in ranked[:num_images]:
        name = o.replace(path, '')
        try:
            ims_to_display[name] = Image.open(o).convert('RGB')
            full_paths[name] = o  # Store the full path
        except Exception as e:
            with skipped_files_box:
                st.warning(f'Skipping bad file: {name}\ndue to {type(e)}')
                pass
    with image_display_zone:
        # Add Download All button at the top if there are results
        if ims_to_display:
            # Create a zip file in memory with all the images
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for name, img in ims_to_display.items():
                    original_file_path = full_paths[name]
                    # Use just the filename for the zip entry to avoid path issues
                    filename = Path(original_file_path).name
                    with open(original_file_path, 'rb') as f:
                        zip_file.writestr(filename, f.read())
            
            zip_buffer.seek(0)
            st.download_button(
                label="⬇ Download All as ZIP",
                data=zip_buffer.getvalue(),
                file_name="memery_results.zip",
                mime="application/zip",
                key="download_all"
            )
        
        if captions_on:
            # Display images with captions and download buttons
            cols = st.columns(min(3, len(ims_to_display)))  # Create columns for layout
            for idx, (name, img) in enumerate(ims_to_display.items()):
                col_idx = idx % min(3, len(ims_to_display))
                with cols[col_idx]:
                    st.image(img, width=size, channels='RGB', caption=name)
                    # Add download button for each image - use full path to get original file
                    original_file_path = full_paths[name]
                    with open(original_file_path, 'rb') as file:
                        file_bytes = file.read()
                        filename = Path(original_file_path).name
                        st.download_button(
                            label="⬇ Download",
                            data=file_bytes,
                            file_name=filename,
                            mime=f"image/{Path(original_file_path).suffix[1:]}",
                            key=f"download_{idx}"
                        )
        else:
            st.image([o for o in ims_to_display.values()], width=sizes[size_choice], channels='RGB')


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

# Decide which actions to take
if do_clear_cache:
    clear_cache(path, logbox)
elif do_index:
    index(logbox, path, num_workers)
elif search_button or text_query or image_query:
    search(path, text_query, negative_text_query, image_query, image_display_zone, skipped_files_box, num_images, captions_on, sizes, size_choice)  # Modified line

