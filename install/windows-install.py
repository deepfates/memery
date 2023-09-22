import subprocess
import platform
import webbrowser
from packaging import version

from cuda_install import cuda_check

def get_python_version():
    return platform.python_version()

def open_python_download_page():
    webbrowser.open("https://www.python.org/downloads/") 

def is_poetry_installed():
    try:
        subprocess.run(["poetry", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_poetry():
    try:
        subprocess.run(["pip", "install", "poetry"], check=True)
        print("Poetry installed successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Failed to install Poetry: {e}")

if __name__ == "__main__":
    current_version = get_python_version()
    print(f"Found Python version: {current_version}. Project tested with Python 3.10.6.")
    
    if version.parse(current_version) < version.parse("3.9.0"):
        print("\033[91mProject requires Python greater than 3.9. Please install Python 3.9 or greater.\033[0m")
        open_python_download_page()

    if is_poetry_installed():
        print("Poetry is already installed.")
    else:
        print("Poetry is not installed. Installing...")
        install_poetry()
    # Poetry install 

    # check if cuda is installed
    # cuda_check("11.3.0")
