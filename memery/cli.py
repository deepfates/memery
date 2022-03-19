__all__ = ['app', 'recall', 'serve', '__main__']

import typer
import memery.core
import streamlit.cli

app = typer.Typer()

@app.command()
def recall(path: str, query: str, n: int = 10):
    """Search recursively over a folder from the command line"""
    ranked = memery.core.query_flow(path, query=query)
    print(ranked[:n])
#     return(ranked)

@app.command()
def serve():
    """Runs the streamlit GUI in your browser"""
    path = memery.__file__.replace('__init__.py','streamlit_app.py')
    streamlit.cli.main(['run',path])

def __main__():
    app()