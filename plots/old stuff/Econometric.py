'''
Mathematically, the model can be formalized as follows:
Model: Y_i = β_0 + ε_i

Where:
Y_i is the average value of "TH/J" for year i.
β_0 is the intercept of the regression line, representing the average value of "TH/J" across all years.
ε_i is the error term for year i, representing the deviation of the yearly average from the regression line.
In this code, we first load and preprocess the data. We group the data by year, calculate the average "TH/J" for each
year, and then fit a simple linear regression model with the average "TH/J" as the dependent variable and a constant
term as the independent variable (β_0). The summary of the regression results will provide information about the
intercept (β_0), the coefficient (which is not explicitly estimated as it's just the constant term), and statistical
metrics such as R-squared, which measures the goodness of fit. This approach allows you to analyze the yearly trend and
intercept in your time series data.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Define the variable name for the unit power efficiency column
unit_power_efficiency = 'TH/J'

# Load your data from the CSV file
data = pd.read_csv('final3.csv')

# Convert the 'date' column to a datetime format
data['date'] = pd.to_datetime(data['date'])

# Extract year from the 'date' column and create a new column 'year'
data['year'] = data['date'].dt.year

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Extract years from the data
years = data['year'].unique()

# Initialize lists to store yearly 'TH/J' values
th_j_values = []

# Create an empty array to store the regression lines
regression_lines = []

# Iterate over each year, calculate the slope, and store the data
for year in years:
    # Filter data for the current year
    yearly_data = data[data['year'] == year]

    # Fit a linear regression model
    model = LinearRegression()
    X = np.arange(len(yearly_data)).reshape(-1, 1)
    y = yearly_data[unit_power_efficiency]
    model.fit(X, y)

    # Calculate the slope for the year
    slope = model.coef_[0]

    # Calculate the mean 'TH/J' value for the year
    th_j_mean = yearly_data[unit_power_efficiency].mean()

    # Store the yearly 'TH/J' value
    th_j_values.append(th_j_mean)

    # Store the regression line for the year (point at the end of the year)
    end_of_year_date = yearly_data['date'].max()
    regression_lines.append((end_of_year_date, th_j_mean))

# Create a DataFrame to store the yearly 'TH/J' values and regression points
results = pd.DataFrame({'Year': years, unit_power_efficiency: th_j_values})

# Print the yearly 'TH/J' values
print(results)

# Scatter plot for all data points
plt.scatter(data['date'], data[unit_power_efficiency], c='blue', s=10, label='Data Points', alpha=0.5)

# Plot the regression lines (one point per year)
regression_dates, regression_th_j_values = zip(*regression_lines)
plt.plot(regression_dates, regression_th_j_values, marker='o', linestyle='-', color='black', label=f'Yearly {unit_power_efficiency} Regression')

plt.yscale('log')  # Set the y-axis to a logarithmic scale base 10

# Add year labels with angled text
for year, th_j_value in zip(years, regression_th_j_values):
    plt.text(year, th_j_value, str(year), rotation=45, ha='right', va='center', fontsize=10)

plt.ylabel('Power Efficiency' + unit_power_efficiency)
plt.title(f'Yearly-Updated {unit_power_efficiency} with Data Points')
plt.legend(loc='upper left')
plt.yticks()
plt.tight_layout()
plt.show()