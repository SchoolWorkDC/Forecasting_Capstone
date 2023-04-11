    Overview: 
Generic time-series forecasting tool using the Prophet algorithm. Takes url or local csv/excel time series data sets, separates data sets by model groups and produces predicted values (based on configuration). Values are transformed into interactive html plots to review actual and forecasted data.

    Dependencies: 
Included environment.yml file can be used to recreate the environment used for this pipeline.

    Configuration: 
Configure the config.json to set the data source (URL or local filename).

    Usage:
Run pipeline.py 

    Troubleshooting:
Input data rows with non-numeric target values will be dropped, incomplete data sets will still produce forecasted plots. The more complete the data set, the higher the accuracy that can be expected from the predicted values.

