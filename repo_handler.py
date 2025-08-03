import os
import tempfile
import subprocess
import uuid
from urllib.parse import urlparse

def fetch_repo(link, download_dir=None):
    if download_dir is None:
        temp_dir = tempfile.mkdtemp()
    else:
        # Create a unique subfolder inside download_dir
        unique_folder = os.path.join(download_dir, f"repo_{uuid.uuid4().hex[:8]}")
        os.makedirs(unique_folder, exist_ok=True)
        temp_dir = unique_folder

    if link.endswith(".zip"):
        import zipfile
        with zipfile.ZipFile(link, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif "github.com" in link:
        subprocess.run(["git", "clone", link, temp_dir], check=True)
    else:
        raise ValueError("Invalid repo source. Provide a GitHub link or zip file.")

    return temp_dir

def analyze_repo(repo_path):
    app_file = None
    requirements_file = None

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file == "app.py":
                app_file = os.path.join(root, file)
            if file == "requirements.txt":
                requirements_file = os.path.join(root, file)

    return app_file, requirements_file
