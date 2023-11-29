import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import yaml

# Read the list of notebooks from a YAML file
with open('config/config.yml', 'r') as f:
    config = yaml.safe_load(f)
    notebooks = config['workflow_steps_notebooks']

for notebook_filename in notebooks:
    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': './'}})
        with open('executed_'+notebook_filename, 'wt') as f:
            nbformat.write(nb, f)
