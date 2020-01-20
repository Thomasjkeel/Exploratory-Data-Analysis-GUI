import os
import shutil
from pathlib import Path
import pandas as pd
# shutil.rmtree() -> for removing directories

# DEFINE GLOBAL VARIABLES
# CURRENT_YEAR = pd.datetime.now().year

### The Processes of the app ###
def process_1(data):
    new_data = data.sum()
    return new_data


def process_2(data):
    new_data = data.sum()
    return new_data


def process_3(data):
    new_data = data.sum()
    return new_data


def process_4(data):
    new_data = data.sum()
    return new_data

def make_output_directories(output_dir):
    if not os.path.exists(output_dir / 'app_outputs'):
        os.mkdir(output_dir / 'app_outputs')
    else:
        shutil.rmtree(output_dir / 'app_outputs')
        os.mkdir(output_dir / 'app_outputs')


### Useful functions (Suggestion: move to a file called 'utils.py')
def subsetData(data):
    """
        function to subset data based on inputs
    """
    ### processes
    return data


def testAnalysis(data):
    """
        Test Process to sum the data from the csv
    """
    new_data = data.sum()
    return new_data
