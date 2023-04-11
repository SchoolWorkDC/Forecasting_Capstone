"""
This module provides the Extract class, which is responsible for downloading and reading data
from the given source (URL or local file). The class handles CSV and Excel file formats and
creates training sets based on the specified description column in the configuration.
"""

from io import StringIO, BytesIO
import os
import pandas as pd
import requests
import validators


class Extract:
    """
    Extract class is responsible for downloading and reading the data from the given source
    (URL or local file).
    This class handles CSV and Excel file formats and creates training sets based on the specified
    description column in the configuration.
    """

    def __init__(self, config):
        """
        Initializes the Extract class with the given configuration.

        :param config: dict, configuration settings for the ETL pipeline.
        """
        self.config = config

    def run(self):
        """
        Runs the extraction process. Downloads the file if the data source is a URL, otherwise reads
        the local file.

        :return: DataFrame, extracted data in pandas DataFrame format.
        """
        if validators.url(self.config['data_source']):
            filepath = self.download_file()
            data = self.read_file(filepath)
        else:
            data = pd.read_csv(self.config['data_source'])
        return data

    def download_file(self):
        """
        Downloads the file from the specified URL.

        :return: str, filepath of the downloaded file.
        """
        url = self.config['data_source']
        filename = "datasetTest.csv"
        filepath = os.path.join(os.getcwd(), filename)
        print(f"Downloading {url}")
        response = requests.get(url, timeout=30)
        with open(filepath, "wb") as file:
            file.write(response.content)
        return filepath

    def read_file(self, filepath):
        """
        Reads the file and returns the data as a pandas DataFrame.

        :param filepath: str, path of the file to be read.
        :return: DataFrame, data in pandas DataFrame format.
        """
        if filepath.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            return pd.read_csv(StringIO(content))
        if filepath.endswith('.xlsx'):
            with open(filepath, 'rb') as file:
                content = file.read()
            return pd.read_excel(BytesIO(content))
        raise ValueError(f"Unknown file type for {filepath}")

    def create_train_sets(self, data):
        """
        Creates training sets by grouping the data based on the specified description column.

        :param data: DataFrame, data in pandas DataFrame format.
        :return: dict, training sets with group names as keys and corresponding data as values.
        """
        train_sets = {}
        for group_name, group_data in data.groupby(self.config['description_column']):
            train_sets[group_name] = group_data.copy()
        return train_sets
