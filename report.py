"""
This module contains the Report class, which is used to create visualizations
of forecasted data using Plotly.

Example:
    data_dict = {...}
    forecasts = {...}
    config = {...}
    report = Report(data_dict, forecasts, config)
    report.create_plots()
"""
import os
import plotly.graph_objs as go
import plotly.offline as pyo


class Report: # pylint: disable=too-few-public-methods
    """
    A class used to create visualizations of forecasted data using Plotly.

    Attributes:
        data_dict (dict): A dictionary containing the actual data.
        forecasts (dict): A dictionary containing the forecasted data.
        config (dict): A dictionary containing configuration settings.
    """

    def __init__(self, data_dict, forecasts, config):
        """
        Initializes a new instance of the Report class.

        Args:
            data_dict (dict): A dictionary containing the actual data.
            forecasts (dict): A dictionary containing the forecasted data.
            config (dict): A dictionary containing configuration settings.
        """

        self.data_dict = data_dict
        self.forecasts = forecasts
        self.config = config

    def create_plots(self):
        """
        Creates and exports a Plotly visualization for each set of forecasted data.

        The visualizations are exported as HTML files with the format "{name}_forecast.html",
        where {name} is the name of the dataset.
        """

        for name, forecast in self.forecasts.items():

            data = self.data_dict[name]
            forecast = self.forecasts[name]

            # Check if the "Reports" folder exists, and create it if not
            reports_folder = "Reports"
            if not os.path.exists(reports_folder):
                os.makedirs(reports_folder)

            # Create a Plotly figure object
            fig = go.Figure()

            # Add the actual data to the plot
            fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], name='Actual'))

            # Add the forecasted data to the plot
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))

            # Add upper and lower bounds to the plot
            fig.add_trace(go.Scatter(x=forecast['ds'],
                                     y=forecast['yhat_upper'], fill=None, mode='lines',
                                     line_color='rgba(0, 0, 255, 0.2)', name='Upper Bound'))
            fig.add_trace(go.Scatter(x=forecast['ds'],
                                     y=forecast['yhat_lower'], fill='tonexty', mode='lines',
                                     line_color='rgba(0, 0, 255, 0.2)', name='Lower Bound'))

            # Set the plot layout
            fig.update_layout(title=f"{name}", xaxis_title='Date', yaxis_title=self.config.get('y_axis_label'))

            # Export the plot to an HTML file inside the "Reports" folder
            filename = os.path.join(reports_folder, f'{name}_forecast.html')
            pyo.plot(fig, filename=filename)
