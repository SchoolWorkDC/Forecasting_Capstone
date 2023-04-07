import os
import json
from extract import Extract
from preprocess import Preprocess
from transform import Transform
from forecast import Forecast
from report import Report


class Pipeline:
    def __init__(self):
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_file) as f:
            self.config = json.load(f)

    def run(self):
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
