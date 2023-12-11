import dependency_installer
import xarray as xr
from data_hunter_era5 import DataRetriver
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import sys
import ast

def multivariate_regression(target_variable, independent_variables, longitude, latitude):

    variableNames = [target_variable] + independent_variables
    regression_observed_Data = DataRetriver.retrive_custom_data(
        startDate='2019-11-25',
        endDate='2019-11-28',
        properties= variableNames,
        long_min = longitude - 0.5, 
        long_max = longitude + 0.5, 
        lat_min= latitude - 0.5,
        lat_max= latitude + 0.5)


    # Extract the data for multivariate regression

    data_for_regression = xr.merge(regression_observed_Data).sel(longitude=longitude, latitude=latitude, method='nearest')
    data_for_regression = data_for_regression.drop_vars("longitude")
    data_for_regression = data_for_regression.drop_vars("latitude")

    independent_variables_names = list(data_for_regression.variables)
    independent_variables_names.pop(0)
    target_variable = independent_variables_names.pop(0)

    data_for_regression = data_for_regression.to_dataframe()
    # Drop the 'time' column as it is not needed for regression
    # data_for_regression = data_for_regression.drop(columns=['time'])

    # Define the target variable and independent variables
    # target_variable = 't2m'
    # independent_variables = ['u10', 'v10', 'sp', 'stl1']  # Adjust based on your specific variables

    # Extract the target and independent variables from the DataFrame
 
    y = data_for_regression[target_variable]
    X = data_for_regression[independent_variables_names]

    # Add a constant term to the independent variables matrix (required for statsmodels)
    X = sm.add_constant(X)

    # Fit the multivariate regression model
    model = sm.OLS(y, X).fit()

    # Print the regression summary
    summary = str(model.summary())

    # Extract coefficients and intercept from the model
    coefficients = model.params
    intercept = model.params['const']

    # Extract variable names
    variable_names = coefficients.index.tolist()[1:]  # Exclude the intercept

    # Create the formula string
    formula_str = f"{intercept:.2f} + "
    formula_str += " + ".join([f"{coefficients[var]:.2f} * {var}" for var in variable_names])

    # Print the formula
    summary += f"\n\nMultivariate Regression Model Formula: \n{target_variable} = {formula_str}"

    return summary


if(__name__ == "__main__"):
    target_variable = sys.argv[1]
    ind_variables = ast.literal_eval(sys.argv[2])
    long = float(sys.argv[3])
    lat = float(sys.argv[4])
    summary = multivariate_regression(target_variable, ind_variables, long, lat)

    print(summary)
