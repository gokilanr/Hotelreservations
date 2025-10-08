import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

project_name = "my_project"

list_of_files = [
    ".github/workflows/.gitkeep",
    "src/__init__.py",
    "config/__init__.py",
    "config/config.yaml",
    "pipeline/__init__.py",
    "static/style.css",
    "custom_jenkins/Dockerfile",
    "templates/index.html",
    "app.py",
    "dockerfile",
    "requirements.txt",
    "setup.py",
    "notebook/notebook.ipynb",
    "jenkinsfile",
    ".gitignore"


]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as fp:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists and is not empty: {filepath}, skipping creation.")