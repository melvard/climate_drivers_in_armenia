import xarray as xr
from data_hunter_era5 import DataRetriver
import matplotlib.pyplot as plt
import sys;
import ast;
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import os
import io
import base64


def save_plot_in_base64():
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    return my_base64_jpgData

def pca(variableNames,  longitude, latitude):

    pca_observed_Data = DataRetriver.retrive_custom_data(
        startDate='2019-11-25',
        endDate='2019-11-28',
        properties= variableNames,
        long_min = longitude - 0.5, 
        long_max = longitude + 0.5, 
        lat_min= latitude - 0.5,
        lat_max= latitude + 0.5)
    

    data_for_pca = xr.merge(pca_observed_Data)
    data_for_pca = data_for_pca.drop_vars("longitude")
    data_for_pca = data_for_pca.drop_vars("latitude")
    selected_variables = list(data_for_pca.variables)[1:]

    data_for_pca = data_for_pca.to_dataframe()
    data_for_pca = data_for_pca[selected_variables]

    # Standardize the data (optional but recommended for PCA)
    standardized_data = (data_for_pca - data_for_pca.mean()) / data_for_pca.std()

    # Initialize PCA with the number of components you want to retain
    n_components = len(data_for_pca.columns)  # Adjust the number of components based on your requirements
    pca = PCA(n_components=n_components)

    # Fit and transform the data
    pca_result = pca.fit_transform(standardized_data)

    # Create a DataFrame to store the PCA results
    pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i+1}' for i in range(n_components)])

    # Add the time index back to the PCA DataFrame
    pca_df['time'] = data_for_pca.index

    # Visualize the explained variance ratio
    explained_variance_ratio = pca.explained_variance_ratio_

    summary = 'Explained Variance Ratio: ' +  str(explained_variance_ratio) + "\n"

    # Visualize the cumulative explained variance
    cumulative_explained_variance = np.cumsum(explained_variance_ratio)
    summary += 'Cumulative Explained Variance: ' + str(cumulative_explained_variance) + "\n\n"

    import matplotlib.pyplot as plt

    # Plot the explained variance ratio
    plt.bar(range(1, n_components + 1), explained_variance_ratio, alpha=0.7, align='center')
    plt.title('Explained Variance Ratio by Principal Component')
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.savefig('pca_images/Explained_Variance_Ratio_by_Principal_Component.png')

    my_base64_jpgData_explained_variance = save_plot_in_base64()

    print(my_base64_jpgData);

    # plt.show()
    plt.clf()
    # Plot the cumulative explained variance
    plt.plot(range(1, n_components + 1), cumulative_explained_variance, marker='o', linestyle='-', color='b')
    plt.title('Cumulative Explained Variance by Principal Component')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.savefig('pca_images/Cumulative_Explained_Variance_by_Principal_Component.png')

    my_base64_jpgData_cumulative_explained_variance = save_plot_in_base64()

    
    # Access the principal components (coefficients of original variables)
    components_matrix = pca.components_

    # Create a DataFrame to display the coefficients
    components_df = pd.DataFrame(data=components_matrix, columns=selected_variables, index=[f'PC{i+1}' for i in range(n_components)])

    # Print the DataFrame
    summary += "Principal Components (Coefficients of Original Variables):\n\n"
    summary += str(components_df)
    
    return summary




if(__name__ == "__main__"):
    if(not os.path.exists("pca_images")):
        os.mkdir("pca_images")

    properties = ast.literal_eval(sys.argv[1])
    long = float(sys.argv[2])
    lat = float(sys.argv[3])
    summary = pca(properties, long, lat)

    print(summary)
