import typer
from memery.core import Memery
import memery
import streamlit.cli
from typing import Optional
# Sometimes you just want to be able to pipe information through the terminal. This is that command

app = typer.Typer()

@app.command()
def recall(path: str, query: str, n: int = 10) -> list[str]:
    """Search recursively over a folder from the command line"""
    memery = Memery()
    ranked = memery.query_flow(path, query=query, reindex=True)
    print(ranked[:n])

@app.command()
def serve(root: Optional[str] = typer.Argument(None)):
    """Runs the streamlit GUI in your browser"""
    app_path = memery.__file__.replace('__init__.py','streamlit_app.py')
    if root is None:
        streamlit.cli.main(['run', app_path, './images'])
    else:
        streamlit.cli.main(['run', app_path, f'{root}'])

def __main__():
    app()