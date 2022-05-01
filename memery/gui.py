# import ipywidgets as widgets

# from .core import query_flow
# from pathlib import Path
# from IPython.display import clear_output



# def get_image(file_loc):
#     filepath = Path(file_loc)
#     file = open(filepath, 'rb')
#     image = widgets.Image(value=file.read(),width=200)

#     return(image)

# def get_grid(filepaths, n=4):
#     imgs = [get_image(f) for f in filepaths[:n] if Path(f).exists()]
#     grid = widgets.GridBox(imgs, layout=widgets.Layout(grid_template_columns="repeat(auto-fit, 200px)"))
#     return(grid)

# from PIL import Image
# from io import BytesIO

# def update_tabs(path, query, n_images, searches, tabs, logbox, im_display_zone, image_query=None):
#     stem = Path(path.value).stem
#     slug = f"{stem}:{str(query.value)}"
#     if slug not in searches.keys():
#         with logbox:
#             print(slug)
#             if image_query:
#                 im_queries = [name for name, data in image_query.items()]

#                 img = [Image.open(BytesIO(file_info['content'])).convert('RGB') for name, file_info in image_query.items()]
#                 ranked = query_flow(path.value, query.value, image_query=img[-1])
#                 slug = slug + f'/{im_queries}'

#                 if len(im_queries) > 0:
#                     with im_display_zone:
#                         clear_output()
#                         display(img[-1])
#             else:
#                 ranked = query_flow(path.value, query.value)
#             searches[f'{slug}'] = ranked

#     tabs.children = [get_grid(v, n=n_images.value) for v in searches.values()]
#     for i, k in enumerate(searches.keys()):
#         tabs.set_title(i, k)
#     tabs.selected_index = len(searches)-1


# #     return(True)

# class appPage():

#     def __init__(self):
#         self.inputs_layout =  widgets.Layout(max_width='80%')

#         self.path = widgets.Text(placeholder='path/to/image/folder', value='images/', layout=self.inputs_layout)
#         self.query = widgets.Text(placeholder='a funny dog meme', value='a funny dog meme', layout=self.inputs_layout)

#         self.image_query = widgets.FileUpload()
#         self.im_display_zone = widgets.Output(max_height='5rem')

#         self.n_images = widgets.IntSlider(description='#', value=4, layout=self.inputs_layout)
#         self.go = widgets.Button(description="Search", layout=self.inputs_layout)
#         self.logbox = widgets.Output(layout=widgets.Layout(max_width='80%', height="3rem", overflow="none"))
#         self.all_inputs_layout =  widgets.Layout(max_width='80vw', min_height='40vh', flex_flow='row wrap', align_content='flex-start')

#         self.inputs = widgets.Box([self.path, self.query, self.image_query, self.n_images, self.go, self.im_display_zone, self.logbox], layout=self.all_inputs_layout)
#         self.tabs = widgets.Tab()
#         self.page = widgets.AppLayout(left_sidebar=self.inputs, center=self.tabs)

#         self.searches = {}
#         self.go.on_click(self.page_update)

#         display(self.page)

#     def page_update(self, b):

#         update_tabs(self.path, self.query, self.n_images, self.searches, self.tabs, self.logbox, self.im_display_zone, self.image_query.value)


