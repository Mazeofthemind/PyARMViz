
from typing import List
from zipfile import ZipFile

from tarfile import TarFile
import tarfile
from io import TextIOWrapper
from io import StringIO
import csv

import logging

import pandas as pd

from os.path import dirname, exists, expanduser, isdir, join, splitext
from bokeh.layouts import row
from PyARMViz.Rule import Rule, generate_rule_from_dict
import json

def load_shopping_transactions() -> List[List]:
    '''
        Test dataset of shopping transaction data for testing PyARMViz visualizations
        once association rules
        
        Original data is a list of individual items with associated customer and transaction
        IDs. This data was created by grouping the items based on customer ID, so essentially
        they reflect the entire buying history of an individual
        
        Stored in compressed csv, provided in Python List-of-List-of-Strings
    '''
    module_path = dirname(__file__)
    shopping_data_uri = join(module_path, 'Online_Retail_Grouped.tar.xz')
    with tarfile.open(shopping_data_uri, "r:xz") as tar:   
        f=tar.extractfile('Online_Retail_Grouped.csv')
        
        
        csv_file_buffer=StringIO(f.read().decode('utf-8'))
        data = list(csv.reader(csv_file_buffer))
        return data
        
        
def load_shopping_rules() -> List[Rule]:
    '''
        Pre-generated association rules generated using standard Apriori with 5% minimum support, 
        70% minimum confifrom the test dataset of shopping transactions
        
        Stored in compressed csv, provided in Pythong List of Tuples
    '''
    module_path=dirname(__file__)
    shopping_rule_data_uri = join(module_path, 'Online_Retail_Rules.json')
    rule_dicts = json.load(open(shopping_rule_data_uri, 'r'))
    rules = list(map(lambda rule_dict: generate_rule_from_dict(rule_dict), rule_dicts))
    return rules