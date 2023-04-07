import pandas as pd


class Transform:
    def __init__(self, config):
        self.config = config

    def run(self, data_dict):
        # # Group data frames by description column
        # groups = {}
        # for name, df in data_dict.items():
        #     group_col = self.config['description_column']
        #     if group_col in df.columns:
        #         for group_name, group_data in df.groupby(group_col):
        #             groups[name + '_' + group_name] = group_data
        #     else:
        #         groups[name] = df

        # Check for missing values
        for name, df in data_dict.items():
            if not pd.api.types.is_numeric_dtype(df[self.config['target_column']]):
                print(f"Warning: Non-numeric values found in data frame {name}")
                df = df[pd.to_numeric(df[self.config['target_column']], errors='coerce').notnull()]
            data_dict[name] = df

        # Reformat data frames for
        # Prophet algorithm
        for name, df in data_dict.items():
            if name != 'Coal Consumption':
                continue
            df = df.rename(columns={self.config['date_column']: 'ds', self.config['target_column']: 'y'})
            data_dict[name] = df[['ds', 'y']]
        return data_dict
