import os
import shutil
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import yaml

# Read the list of notebooks from a YAML file
with open('config/config.yml', 'r') as f:
    config = yaml.safe_load(f)
    notebooks = config['workflow_steps_notebooks']

output_dir = 'results'
os.makedirs(output_dir, exist_ok=True)

for notebook_filename in notebooks:
    # Copy the entire directory to the results folder
    notebook_dir = os.path.dirname(notebook_filename)
    notebook_basename = os.path.basename(notebook_filename)
    result_dir = os.path.join(output_dir, notebook_dir)
    os.makedirs(result_dir, exist_ok=True)
    shutil.copytree(notebook_dir, result_dir, dirs_exist_ok=True)

    # Execute the notebook in the results folder
    with open(os.path.join(result_dir, notebook_basename)) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': result_dir}})
        with open(os.path.join(result_dir, 'executed_' + notebook_basename), 'wt') as f:
            nbformat.write(nb, f)
