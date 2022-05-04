import typer
from memery.core import Memery
import memery
import streamlit.cli
from typing import Optional
# Sometimes you just want to be able to pipe information through the terminal. This is that command

app = typer.Typer()

def main():
    app()

@app.command()
def recall(
    root: str = typer.Argument(None, help="Image folder to search"),
    text: str = typer.Option(None, *("-t", "--text"), help="Text query"),
    image: str = typer.Option(None, *("-i", "--image"), help="Filepath to image query") ,
    count: int = typer.Option(10, *("-c", "--count"), help="Number of results to return")
    ) -> list[str]:
    """Search recursively over a folder from the command line"""
    memery = Memery()
    ranked = memery.query_flow(root, query=text, image_query=image)
    print(ranked[:count])

@app.command()
def serve(root: Optional[str] = typer.Argument(None)):
    """Runs the streamlit GUI in your browser"""
    app_path = memery.__file__.replace('__init__.py','streamlit_app.py')
    if root is None:
        streamlit.cli.main(['run', app_path, './images'])
    else:
        streamlit.cli.main(['run', app_path, f'{root}'])

@app.command()
def build(
    root: str = typer.Argument(None),
    workers: int = typer.Option(default=0)
    ):
    '''
    Indexes the directory and all subdirectories
    '''
    memery = Memery()
    memery.index_flow(root, num_workers=workers)
    return None

@app.command()
def purge(root: str = typer.Argument(None)):
    """
    Cleans out all files saved by memery
    """
    memery = Memery()
    memery.clean(root)
    print("Purged files!")

if __name__ == "__main__":
    main()