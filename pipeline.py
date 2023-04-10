"""
This module contains the Pipeline class, which is used to execute the entire
forecasting process, from data extraction to report generation.

Example:
    pipeline = Pipeline()
    pipeline.run()
"""

import os
import json
from extract import Extract
from preprocess import Preprocess
from transform import Transform
from forecast import Forecast
from report import Report


class Pipeline:
    """
    A class used to execute the entire forecasting process, from data extraction
    to report generation.

    Attributes:
        config (dict): A dictionary containing configuration settings.
    """

    def __init__(self):
        """
        Initializes a new instance of the Pipeline class by loading the
        configuration settings from the 'config.json' file.
        """

        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_file) as f:
            self.config = json.load(f)

    def run(self):
        """
        Executes the entire forecasting process, from data extraction to report
        generation, using the following steps:

        1. Extract data from the source.
        2. Create train sets.
        3. Preprocess the data.
        4. Transform the data.
        5. Forecast the data.
        6. Generate the report(s).
        """

        # Extract data from source
        extractor = Extract(self.config)
        data = extractor.run()

        # Create train sets
        train_sets = extractor.create_train_sets(data)

        # Preprocess data
        preprocessor = Preprocess(self.config)
        data_dict = preprocessor.run(train_sets)

        # Transform data
        transformer = Transform(self.config)
        transformed_data = transformer.run(data_dict)

        # Forecast data
        forecaster = Forecast(transformed_data, self.config)
        forecasts = forecaster.run()

        # Generate report
        reporter = Report(transformed_data, forecasts, self.config)
        reporter.create_plots()


if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.run()
