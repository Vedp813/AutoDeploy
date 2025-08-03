# code_modifier.py

import os

def find_app_entry(repo_path):
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file == "app.py":
                return os.path.join(root, file)
    return None

def patch_localhost(app_file_path):
    with open(app_file_path, 'r') as f:
        content = f.read()

    # Replace localhost or 127.0.0.1
    patched = content.replace("127.0.0.1", "0.0.0.0").replace("localhost", "0.0.0.0")

    if patched != content:
        with open(app_file_path, 'w') as f:
            f.write(patched)
        print(f"Patched localhost in: {app_file_path}")
    else:
        print("No need to patch localhost")

def find_requirements(repo_path):
    for root, _, files in os.walk(repo_path):
        if "requirements.txt" in files:
            return os.path.join(root, "requirements.txt")
    return None
