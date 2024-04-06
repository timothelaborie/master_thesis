import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import skew, kurtosis, shapiro
import matplotlib.dates as mdates
import warnings



def get_data(filter1: str, filter2: str):
    # Read the input data from the CSV file
    data = pd.read_csv('inputs.csv', parse_dates=['date']) # date,avg_efficiency,max_efficiency,open_price,count
    data2 = pd.read_csv('../6_calculating_costs/cost.csv', parse_dates=['date']) # date,cost

    # inner join the two dataframes
    data = pd.merge(data, data2, on='date', how='inner')

    # keep only data after filter
    data = data[data['date'] >= filter1]
    data = data[data['date'] < filter2]

    # time variable: (year-2011)*12+month
    data['time'] = (data['date'].dt.year - 2011) * 12 + data['date'].dt.month

    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.fillna(method='bfill', inplace=True)

    # Create quarterly averages
    quarterly_data = data.resample('Q', on='date').mean()
    # Create monthly averages
    monthly_data = data.resample('M', on='date').mean()
    # Create weekly averages
    weekly_data = data.resample('W', on='date').mean()
    # Keep daily data
    daily_data = data

    quarterly_data['count'] = data.resample('Q', on='date').sum()['count']
    monthly_data['count'] = data.resample('M', on='date').sum()['count']
    weekly_data['count'] = data.resample('W', on='date').sum()['count']
    daily_data['count'] = data['count']

    for df in [quarterly_data,monthly_data, weekly_data, daily_data]:
        # Calculate the derivative of ln avg_efficiency
        df['ln_avg_efficiency'] = np.log(df['avg_efficiency'])
        df['d_ln_avg_efficiency'] = df['ln_avg_efficiency'].diff()

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(method='bfill', inplace=True)

        # Differencing the series to make it stationary
        df['ln_open_price'] = np.log(df['open_price'])
        df['d_ln_open_price'] = df['ln_open_price'].diff().fillna(method='bfill')

        df['d_cost'] = df['cost'].diff().fillna(method='bfill')
        df['cost_squared'] = df['cost'] ** 2
        
        df['d_optimistic_speculation'] = df['optimistic_speculation'].diff().fillna(method='bfill')
        df['d_pessimistic_speculation'] = df['pessimistic_speculation'].diff().fillna(method='bfill')
        df['d_bitcoin_adoption'] = df['bitcoin_adoption'].diff().fillna(method='bfill')
        df['d_posts_count'] = df['posts_count'].diff().fillna(method='bfill')

    return quarterly_data,monthly_data, weekly_data, daily_data





