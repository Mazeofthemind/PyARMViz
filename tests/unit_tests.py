import unittest
import PyARMViz

import pandas as pd
from RareMiner import RareMiner

import os

import logging

class MyTest(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        #logging.basicConfig(level=logging.INFO)

        RetailTransactions_df = pd.read_csv('./reduced_retail.csv',)
        #RetailTransactions_df = pd.read_csv('./transactions_by_dept.csv',)
        
        #print(RetailTransactions_df.columns)
        
        invoice_grouped_transactions_df = RetailTransactions_df.groupby(by=['CustomerID'])
        #invoice_grouped_transactions_df = RetailTransactions_df.groupby(by=['POS Txn'])
        
        transaction_list = []
        for group_name, group in invoice_grouped_transactions_df:
            items = tuple(group['StockCode'].unique())
            #items = tuple(group['Dept'].unique())
            transaction_list.append(items)
        
        total_length = len(transaction_list)
        
        #print(transaction_list)
        results = RareMiner.apriori_frequent_from_collection(transaction_list, 0.05, 3, False)
            
        self.rules = list(RareMiner.rules.generate_rules_apriori(results, 0.7, total_length))
    
    '''
    def test_plotly_rule_graph(self):
        graph = PyARMViz.generate_rule_graph_graphml(self.rules,)
        self.assertTrue(True)
        #generate_rule_strength_plot(rules)
    def test_graphml_rule_graph(self):
        test_file_path = './test.graphml'
        graph = PyARMViz.generate_rule_graph_graphml(self.rules, test_file_path)
        self.assertTrue(os.path.exists(test_file_path))
    
    def test_plotly_rule_strength_plot(self):
        PyARMViz.generate_rule_strength_plot(self.rules)
        self.assertTrue(True)
    '''  
    def test_plotly_parallel_plot(self):
        PyARMViz.generate_parallel_plot(self.rules)
        