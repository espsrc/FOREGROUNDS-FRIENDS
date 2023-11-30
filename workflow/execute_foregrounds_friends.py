import os
import shutil
import subprocess
import yaml
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


# Read the list of tasks from a YAML file
with open('config/config.yml', 'r') as f:
    config = yaml.safe_load(f)
    tasks = config['tasks']

output_dir = 'results'
os.makedirs(output_dir, exist_ok=True)
original_dir = os.getcwd()


for task in tasks:
    # Copy the entire directory to the results folder
    task_path = task['path']
    task_dir = os.path.dirname(task_path)
    task_basename = os.path.basename(task_path)
    result_dir = os.path.join(output_dir, task_dir)
    os.makedirs(result_dir, exist_ok=True)
    shutil.copytree(task_dir, result_dir, dirs_exist_ok=True)

    # Check if the task is a notebook or a Python script
    if task['type'] == 'notebook':
        # Execute the notebook in the results folder
        with open(os.path.join(result_dir, task_basename)) as f:
            nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            ep.preprocess(nb, {'metadata': {'path': result_dir}})
            with open(os.path.join(result_dir, task_basename), 'wt') as f:
                nbformat.write(nb, f)
    elif task['type'] == 'script':
        # Change the current working directory
        os.chdir(result_dir)
        # Execute the Python script in the results folder with command-line arguments
        args = ['python3', task_basename] + task.get('args', [])
        print(' '.join(args))
        subprocess.run(args, check=True)
        os.chdir(original_dir)
    if task['type'] == 'bash':
        # Change the current working directory
        os.chdir(result_dir)
        # Execute the bash script in the results folder with command-line arguments
        args = ['bash', task_basename] + task.get('args', [])
        print('Executing script:')
        print(' '.join(args))
        subprocess.run(args, check=True)
        os.chdir(original_dir)



