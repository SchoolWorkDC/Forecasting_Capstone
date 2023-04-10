from prophet import Prophet
import pandas as pd


class Forecast:
    def __init__(self, data_dict, config):
        """
        Initializes the Forecast class with data and configuration.

        Parameters
        ----------
        data_dict : dict
            A dictionary containing data frame objects with 'ds' (date) and 'y' (target) columns.
        config : dict
            A configuration dictionary containing the keys 'max_train_date', 'date_format', 'prediction_start',
            'predict_periods', and 'period_frequency'.
        """
        self.data_dict = data_dict
        self.config = config
        self.max_train_date = pd.to_datetime(config['max_train_date'], format=config['date_format'])
        self.prediction_start = pd.to_datetime(config['prediction_start'], format=config['date_format'])

    def filter_train_data(self, df):
        """
        Filters the data frame based on the max_train_date.

        Parameters
        ----------
        df : pd.DataFrame
            The input data frame.

        Returns
        -------
        pd.DataFrame
            The filtered data frame containing only the dates <= max_train_date.
        """
        return df[df['ds'] <= self.max_train_date]

    def create_prophet_model(self, train_data):
        """
        Creates and fits a Prophet model on the given train_data.

        Parameters
        ----------
        train_data : pd.DataFrame
            The input data frame containing the training data.

        Returns
        -------
        Prophet
            The fitted Prophet model.
        """
        m = Prophet()
        m.fit(train_data)
        return m

    def make_future_dataframe(self, m):
        """
        Creates a future data frame for the given Prophet model.

        Parameters
        ----------
        m : Prophet
            The input Prophet model.

        Returns
        -------
        pd.DataFrame
            The future data frame with dates for which predictions will be made.
        """
        return m.make_future_dataframe(periods=self.config['predict_periods'], freq=self.config['period_frequency'])

    def get_forecast(self, m, future):
        """
        Generates the forecast for the given Prophet model and future data frame.

        Parameters
        ----------
        m : Prophet
            The input Prophet model.
        future : pd.DataFrame
            The future data frame containing the dates for predictions.

        Returns
        -------
        pd.DataFrame
            The forecast data frame containing 'ds', 'yhat', 'yhat_lower', and 'yhat_upper' columns.
        """
        forecast = m.predict(future)
        return forecast[forecast['ds'] >= self.prediction_start]

    def run(self):
        """
        Generates forecasts for the data frames in data_dict using the Prophet model.

        Returns
        -------
        dict
            A dictionary containing the forecasts with 'ds', 'yhat', 'yhat_lower', and 'yhat_upper' columns.
        """
        forecasts = {}
        for name, df in self.data_dict.items():
            train_data = self.filter_train_data(df)
            m = self.create_prophet_model(train_data)
            future = self.make_future_dataframe(m)
            forecast = self.get_forecast(m, future)
            forecasts[name] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        return forecasts
