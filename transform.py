"""
transform.py

A module containing the Transform class, which is used for transforming data frames
based on a provided configuration. The Transform class is primarily designed for
reformatting the date and target columns in a given set of data frames.

"""

import pandas as pd


class Transform:
    """
    A class used to transform data frames based on a provided configuration.

    Attributes
    ----------
    config : dict
        A configuration dictionary containing the keys 'date_column' and 'target_column'
        which represent the names of the date and target columns in the data frames.

    Methods
    -------
    run(data_dict):
        Transforms the data frames in the given data_dict according to the config and returns the transformed data_dict.
    reformat_data_frames(data_dict):
        Renames the date and target columns in the data frames of the given data_dict based on the config and filters only the renamed columns.
    """

    def __init__(self, config):
        """
        Parameters
        ----------
        config : dict
            A configuration dictionary containing the keys 'date_column' and 'target_column'
            which represent the names of the date and target columns in the data frames.
        """
        self.config = config

    def run(self, data_dict):
        """
        Transforms the data frames in the given data_dict according to the config and returns the transformed data_dict.

        Parameters
        ----------
        data_dict : dict
            A dictionary containing data frame objects to be transformed.

        Returns
        -------
        dict
            The transformed data_dict with the date and target columns renamed and filtered.
        """
        data_dict = self.reformat_data_frames(data_dict)
        return data_dict

    def reformat_data_frames(self, data_dict):
        """
        Renames the date and target columns in the data frames of the given data_dict based on the config and filters only the renamed columns.

        Parameters
        ----------
        data_dict : dict
            A dictionary containing data frame objects to be transformed.

        Returns
        -------
        dict
            The transformed data_dict with the date and target columns renamed and filtered.
        """
        for name, dataframe in data_dict.items():
            dataframe = dataframe.rename(columns={self.config['date_column']: 'ds',
                                                  self.config['target_column']: 'y'})
            data_dict[name] = dataframe[['ds', 'y']]
        return data_dict
