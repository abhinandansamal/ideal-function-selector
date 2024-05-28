import os
from pathlib import Path
import logging

# logging string
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = 'ideal_function_selector'

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_loader.py",
    f"src/{project_name}/components/data_processor.py",
    f"src/{project_name}/components/data_visualizer.py",
    f"src/{project_name}/database/database.py",
    f"test/__init__.py",
    "config/config.yaml",
    "data/.gitkeep",
    "requirements.txt",
    "setup.py",
    "main.py",
    "research/trials.ipynb",
    "README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")