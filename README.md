# ideal-function-selector

This project provides a Python package to select ideal functions from a set of training data and process test data accordingly. It utilizes SQLite for database management and Bokeh for data visualization.

...
# How to run?
...
### STEPS:

Clone the repository

```bash
https://github.com/abhinandansamal/ideal-function-selector
```
...
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n venv python=3.10 -y
```

```bash
conda activate venv
```

...
### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```

...
### STEP 03- run the project
```bash
python main.py
```

...
# Project Structure
...
* `config/` - Configuration files.
* `data/` - Directory to store data files.
* `research/` - Notebooks for research and trials.
* `src/ideal_function_selector/` - Source code for the project.
    * `components/` - Contains `data_loader.py`, `data_processor.py`, `data_visualizer.py`.
    * `data_loader.py` - Loads CSV data into the database.
    * `data_processor.py` - Processes data to find best fit functions and map test data.
    * `data_visualizer.py` - Visualizes the data using Bokeh.
    * `database.py` - Handles database-related operations.
* `main.py` - Main script to run the project.
* `test/` - Contains unit test for the project components.
* `README.md` - Project documentation.
* `requirements.txt` - List of dependencies.
* `setup.py` - Setup script for the package.
* `template.py` - Contains Project structure template.

...
# License
...
```bash
MIT
```

### Project Directory Structure
Here is the full directory structure after running `template.py` and adding the required files.

.project_root/
│
├── .github/
│ └── workflows/
│ └── .gitkeep
│
├── config/
│ └── config.yaml
│
├── research/
│ └── trials.ipynb
│
├── src/
│ └── ideal_function_selector/
│ ├── init.py
│ ├── components/
│ │ ├── init.py
│ │ ├── data_loader.py
│ │ ├── data_processor.py
│ │ ├── data_visualizer.py
│ ├── database
│ │ ├── init.py
│ │ ├── database.py
│
├── test/
│ └── init.py
│ └── test_data_loader.py
│ └── test_data_processor.py
│
├── main.py
├── README.md
├── requirements.txt
├── template.py
├── setup.py
└── LICENSE

```bash
### `requirements.txt`
```
numpy
pandas
sqlalchemy
bokeh
ipykernel
notebook
pyyaml

```bash
### Git Commands

To clone the branch, commit changes, and push to the repository:

```bash
# Clone the repository and checkout the develop branch
git clone -b develop <repository_url>
cd <repository_name>

# Make changes to the code and add a new function
# After making changes, add, commit, and push the changes
git add .
git commit -m "Added new function to process data"
git push origin develop

# Create a pull request on GitHub or your Git management platform
```