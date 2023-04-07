from prophet import Prophet
import pandas as pd

class Forecast:
    def __init__(self, data_dict, config):
        self.data_dict = data_dict
        self.config = config
        self.max_train_date = pd.to_datetime(config['max_train_date'], format=config['date_format'])

    def run(self):
        forecasts = {}
        for name, df in self.data_dict.items():
            if name != 'Coal Consumption':
                continue
            train_data = df[df['ds'] <= self.max_train_date]
            m = Prophet()
            m.fit(train_data)
            future = m.make_future_dataframe(periods=12, freq='M')
            forecast = m.predict(future)
            forecasts[name] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        return forecasts
