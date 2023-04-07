import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime


class Preprocess:
    def __init__(self, config):
        self.config = config

    def run(self, data_dict):
        # Convert date column to string format
        for name, df in data_dict.items():
            df[self.config['date_column']] = df[self.config['date_column']].astype(str)

        # Eliminate rows with month value of 13
        for name, df in data_dict.items():
            df = df[~df[self.config['date_column']].str.endswith('13')]
            data_dict[name] = df

        # Convert date column to datetime format
        for name, df in data_dict.items():
            df[self.config['date_column']] = pd.to_datetime(df[self.config['date_column']], format=self.config['date_format'])
        return data_dict

        # # Convert date column to datetime format
        # for name, df in data_dict.items():
        #     df[self.config['date_column']] = pd.to_datetime(df[self.config['date_column']], format='%Y%m')
        # print(data_dict)
        # return data_dict

