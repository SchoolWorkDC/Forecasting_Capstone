"""
This module provides the Preprocess class for preprocessing data in pandas DataFrames.
The class contains methods for converting date columns to strings, eliminating invalid rows,
converting date columns back to datetime objects, and dropping non-numeric target rows.
"""

import pandas as pd


class Preprocess:
    """
        The Preprocess class is responsible for preparing the input data for forecasting
        by performing various preprocessing steps on pandas DataFrames. These steps include
        converting date columns to strings, eliminating invalid rows, converting date columns
        back to datetime objects, and dropping non-numeric target rows. The class takes a
        configuration dictionary as input, which contains the necessary information for
        carrying out the preprocessing tasks.
    """
    def __init__(self, config):
        """
        Initialize the Preprocess class with a configuration dictionary.

        :param config: Dictionary containing configuration for preprocessing steps,
                       including date_column, date_format, and target_column keys.
        """
        self.config = config

    def run(self, data_dict):
        """
        Execute preprocessing steps on the data_dict, which contains pandas DataFrames.

        :param data_dict: Dictionary containing pandas DataFrames.
        :return: Preprocessed data_dict with DataFrames after applying preprocessing steps.
        """
        data_dict = self.convert_date_column_to_str(data_dict)
        data_dict = self.eliminate_invalid_rows(data_dict)
        data_dict = self.convert_date_column_to_datetime(data_dict)
        data_dict = self.drop_non_numeric_target_rows(data_dict)
        return data_dict

    def convert_date_column_to_str(self, data_dict):
        """
        Convert the date column in each DataFrame to a string format.

        :param data_dict: Dictionary containing pandas DataFrames.
        :return: Dictionary with updated DataFrames after converting date columns to strings.
        """
        for _, dataframe in data_dict.items():
            dataframe[self.config['date_column']] = \
                dataframe[self.config['date_column']].astype(str)
        return data_dict

    def eliminate_invalid_rows(self, data_dict):
        """
        Eliminate rows with invalid date strings in the date column.

        :param data_dict: Dictionary containing pandas DataFrames.
        :return: Dictionary with updated DataFrames after eliminating invalid rows.
        """
        for name, dataframe in data_dict.items():
            dataframe = dataframe[~dataframe[self.config['date_column']].str.endswith('13')]
            data_dict[name] = dataframe
        return data_dict

    def convert_date_column_to_datetime(self, data_dict):
        """
        Convert the date column in each DataFrame back to a datetime object.

        :param data_dict: Dictionary containing pandas DataFrames.
        :return: Dictionary with updated DataFrames
        after converting date columns to datetime objects.
        """
        for _, dataframe in data_dict.items():
            dataframe[self.config['date_column']] = \
                pd.to_datetime(dataframe[self.config['date_column']],
                               format=self.config['date_format'])
        return data_dict

    def drop_non_numeric_target_rows(self, data_dict):
        """
        Drop rows in the target column that contain non-numeric values.

        :param data_dict: Dictionary containing pandas DataFrames.
        :return: Dictionary with updated DataFrames after dropping non-numeric target rows.
        """
        for name, dataframe in data_dict.items():
            if not pd.api.types.is_numeric_dtype(dataframe[self.config['target_column']]):
                print(f"Warning: Non-numeric values found in data frame {name}")
                dataframe[self.config['target_column']] = \
                    pd.to_numeric(dataframe[self.config['target_column']], errors='coerce')
                dataframe = dataframe.dropna(subset=[self.config['target_column']])
            data_dict[name] = dataframe
        return data_dict
