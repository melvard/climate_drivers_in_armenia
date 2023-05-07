# climate_drivers_in_armenia

Purpose of project:

    The goal of project is to understand the drivers of climate variability and extremes in the territory of Armenia using ML approaches. Project illustrates how climate data fromERA5 reanalysis data servers can be downloaded and processed. The nearest goal is to take under our exploration a climate event from past in Armenia (cyclon for example) and using statistical and ML methodologies of analysing variables before that event simulate the happening of that event. The  Project is done within the colaboration of UFAR (French University of Armenia) and IIAP (Institute for Informatics and Automation Problems).

^^^^^ USAGE ^^^^^

Dependencies:

    1) In order to make things work install dependencies from 'requirements.txt' one of this alternatives:

        1) `pip install -r requirements.txt`
        2) `python dependency_installer.py`

    2) .cdsapirc file with personal key and url should be set up in your PC to use cdsapi
        1) For linux it should be in the directory `$HOME/.`
        2) For macOS it should be in the directory `/Users/user/.`

        Note: .cdsapirc look smth like this:
            url: https://cds.climate.copernicus.eu/api/v2
            key: here_is_your_key

        for more information see: https://cds.climate.copernicus.eu/api-how-to

    3) To run .ipynb notebook files install Jupyter Notebook

NetCDF data hunter:

    This python-implemented  tool includes methods that provide a class to run cdsapi client to download any climate related data you want for any period of time.
    Importing data_hunter_era5.DataRetriver class you can access 2 methods to download netCDF data:

        1) retrive_data(start_date, end_date, parameters, area)
           Downloads climate data from ERA5 with provided variables, time period and for specific area. Saves data at./NetCDF_data/era5

           returns --> list of paths to downloaded .nc files

        2) retrive_data_xarray(start_date, end_date, parameters, area)

           calls retrive_data(...) method and reads all files as xarray DataSet

           returns --> list of xarray DataSet

    Note: Both methods are relying on caching system, so duplicated data will not be downloaded

// todo : add description about example 2m_temperature.ipynb
