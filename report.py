import plotly.graph_objs as go
import plotly.offline as pyo


class Report:
    def __init__(self, data_dict, forecasts, config):
        self.data_dict = data_dict
        self.forecasts = forecasts
        self.config = config

    # def create_plots(self):
    #     for name, forecast in self.forecasts.items():
    #         data = self.data_dict[name]
    #         forecast = self.forecasts[name]
    #
    #         # Create a Plotly figure object
    #         fig = go.Figure()
    #
    #         # Add the actual data to the plot
    #         fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], name='Actual'))
    #
    #         # Add the forecasted data to the plot
    #         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
    #
    #         # Add upper and lower bounds to the plot
    #         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines',
    #                                  line_color='rgba(0, 0, 255, 0.2)', name='Upper Bound'))
    #         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='lines',
    #                                  line_color='rgba(0, 0, 255, 0.2)', name='Lower Bound'))
    #
    #         # Set the plot layout
    #         # fig.update_layout(title=self.config['title'], xaxis_title='Date', yaxis_title=self.config['y_axis_label'])
    #         fig.update_layout(title=f"{name}", xaxis_title='Date', yaxis_title='nrg')
    #
    #
    #         # Export the plot to an HTML file
    #         pyo.plot(fig, filename=f'{name}_forecast.html')

    def create_plots(self):
        for name, forecast in self.forecasts.items():
            if name != 'Coal Consumption':
                continue

            data = self.data_dict[name]
            forecast = self.forecasts[name]

            # Create a Plotly figure object
            fig = go.Figure()

            # Add the actual data to the plot
            print(data['y'])
            fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], name='Actual'))

            # Add the forecasted data to the plot
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))

            # Add upper and lower bounds to the plot
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines',
                                     line_color='rgba(0, 0, 255, 0.2)', name='Upper Bound'))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='lines',
                                     line_color='rgba(0, 0, 255, 0.2)', name='Lower Bound'))

            # Set the plot layout
            fig.update_layout(title=f"{name}", xaxis_title='Date', yaxis_title='Quadrillion Btu')

            # Export the plot to an HTML file
            pyo.plot(fig, filename=f'{name}_forecast.html')



