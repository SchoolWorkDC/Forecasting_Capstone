import os
import pandas as pd
import requests
from io import StringIO, BytesIO
import validators


class Extract:
    def __init__(self, config):
        self.config = config

    def run(self):
        if validators.url(self.config['data_source']):
            filepath = self.download_file()
            data = self.read_file(filepath)
        else:
            data = pd.read_csv(self.config['data_source'], sep=';')
        return data

    def download_file(self):
        url = self.config['data_source']
        filename = "datasetTest.csv"
        filepath = os.path.join(os.getcwd(), filename)
        print(f"Downloading {url}")
        response = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath

    def read_file(self, filepath):
        if filepath.endswith('.csv'):
            with open(filepath, 'r') as f:
                content = f.read()
            return pd.read_csv(StringIO(content))
        elif filepath.endswith('.xlsx'):
            with open(filepath, 'rb') as f:
                content = f.read()
            return pd.read_excel(BytesIO(content))
        else:
            raise ValueError(f"Unknown file type for {filepath}")

    def create_train_sets(self, data):
        train_sets = {}
        for group_name, group_data in data.groupby(self.config['description_column']):
            train_sets[group_name] = group_data.copy()
        return train_sets
