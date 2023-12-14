import xarray as xr
from data_hunter_era5 import DataRetriver
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import sys;
import ast;

def k_means(variableNames, variableValues, longitude, latitude):
    
    global_observed_data = DataRetriver.retrive_custom_data(
        startDate='2019-11-25',
        endDate='2019-11-28',
        properties= variableNames,
        long_min = longitude - 0.5, 
        long_max = longitude + 0.5, 
        lat_min= latitude - 0.5,
        lat_max= latitude + 0.5)
    

    localized_data = xr.merge(global_observed_data).sel(longitude=longitude, latitude=latitude, method='nearest')
    localized_data = localized_data.drop_vars("longitude")
    localized_data = localized_data.drop_vars("latitude")

    # Assuming ds is your xarray.Dataset

    # Extract the relevant variables for clustering
    # localized_data['wind_speed'] = np.sqrt(localized_data['u10']**2 + localized_data['v10']**2)
    column_names = list(localized_data.variables)
    column_names.pop(0)
    data_for_clustering = localized_data[column_names]

    # Convert xarray.Dataset to numpy array
    data_array = data_for_clustering.to_array().values.T

    # Reshape the array to 2D (time x features)
    data_array_2d = data_array.reshape(data_array.shape[0], -1)

    # Specify the number of clusters (k)
    k = 3

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=0)
    clusters = kmeans.fit_predict(data_array_2d)

    # Add cluster labels to the dataset
    localized_data['cluster_labels'] = xr.DataArray(clusters, dims=['time'])


    # new_data_point = np.array([[1.0, 2.0, 3.0, 4.0]], dtype=np.float64)  # Ensure it has 4 features
    # kmeans.predict(new_data_point)

    # # Visualize the clusters (using only two features for simplicity)
    # ax = plt.subplots()
    # plt.scatter(localized_data['t2m'], localized_data['wind_speed'], c=clusters, cmap='viridis', alpha=0.5)
    # plt.xlabel('t2m')
    # plt.ylabel('wind_speed')
    # plt.title(f'K-means Clustering (k={k})')
    # # ax.axline((0, 0), slope=0, color="red")
    # # ax.axline((0, 0), slope=10000000, color="blue") # high sloping is just tricky way of drawing vertical axis
    # plt.show()
    
    # Add cluster centroids to the dataset
    localized_data['cluster_centroids'] = xr.DataArray(kmeans.cluster_centers_, dims=['cluster', 'feature'])

    # Predict the cluster for a new data point
    new_data_point = np.array([variableValues])  # Replace with actual float values
    new_data_point = new_data_point.astype(kmeans.cluster_centers_.dtype)  # Ensure consistent dtype
    predicted_cluster = kmeans.predict(new_data_point)

    # Display cluster centroids and predicted cluster for a new data point
    result = "\tCluster Centroids:\n\n"

    result += str(localized_data['cluster_centroids'].to_dataframe())

    result += "\nPredicted Cluster for New Data Point:\n\n"
    result += f"The new data point belongs to Cluster {predicted_cluster[0]}"

    return result
    

    
if(__name__ == "__main__"):
    properties = ast.literal_eval(sys.argv[1])
    values = ast.literal_eval(sys.argv[2])
    long = float(sys.argv[3])
    lat = float(sys.argv[4])
    result = k_means(properties, values, long, lat)
    print(result)