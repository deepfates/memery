import platform
import subprocess
import torch


def cuda_check(required_cuda_version: str):
    if torch.cuda.is_available():        
        print(f"Detected CUDA version: {torch.version.cuda}, torch: {torch.__version__}")                
    else:
        # Only call check_and_install_cuda if CUDA is not available
        cuda_installed = check_and_install_cuda(required_cuda_version)        
        if cuda_installed and torch.cuda.is_available():            
            print(f"Detected CUDA version: {torch.version.cuda}, torch: {torch.__version__}")        

def check_for_nvidia_gpu():
    try:
        result = subprocess.run(["nvidia-smi", "-L"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "GPU" in result.stdout
    except subprocess.CalledProcessError:
        return False

def download_and_install_cuda(required_cuda_version: str):
    system = platform.system()
    if system == "Linux":
        subprocess.run(["wget", f"https://developer.nvidia.com/cuda-{required_cuda_version}-download-archive"], check=True)
    elif system == "Windows":                
        subprocess.run(["start", f"https://developer.nvidia.com/cuda-{required_cuda_version}-download-archive"], shell=True, check=True)
    elif system == "Darwin":
        print("Sorry, CUDA is not supported on macOS.")
        return False
    else:
        print("Unsupported OS.")
        return False
    print("Please follow the instructions on the opened webpage to install CUDA. After CUDA has been installed you will need to run the following commands")
    print("pip install torch==1.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html")
    print("pip install -e .")
    return True

def check_and_install_cuda(required_cuda_version: str):
    if not check_for_nvidia_gpu():
        print("No CUDA-compatible GPU detected. You must use CPU mode.")
        return False

    try:
        import torch
        installed_cuda_version = torch.version.cuda
        if installed_cuda_version == required_cuda_version:
            return True
    except ImportError:
        print("PyTorch is not installed. Unable to check CUDA version.")
        return False

    # Print in red
    print(f"\033[91mDetected CUDA {installed_cuda_version}, requires {required_cuda_version} for gpu.\033[0m")

    # Collect user input
    user_input = input("\033[94mUsing cpu mode by default. Install CUDA version for gpu mode? [y/N]: \033[0m\n\n")

    if user_input.lower() == 'y':
        return download_and_install_cuda(required_cuda_version)
    else:
        print("Proceeding with CPU mode.")
        return False
