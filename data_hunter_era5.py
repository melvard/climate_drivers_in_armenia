import cdsapi
import pandas as pd
import xarray as xr
import os

cds = cdsapi.Client()

class DataRetriver:

    download_path = "./NetCDF_data/era5/"
    
    def retrieve_single_day_data_func(day, month, year, parameters, area, filename):
        cds.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type':'reanalysis',
                'format':'netcdf',
                'variable':parameters,
                'year':[
                      year
                ],
                'month':[
                      month
                ],
                'day':[
                    day
                ],
                'time':[
                    '00:00','01:00','02:00',
                    '03:00','04:00','05:00',
                    '06:00','07:00','08:00',
                    '09:00','10:00','11:00',
                    '12:00','13:00','14:00',
                    '15:00','16:00','17:00',
                    '18:00','19:00','20:00',
                    '21:00','22:00','23:00'
                ],
            'area': area
            },
            filename)
        return
    
    @staticmethod
    def retrive_data(start_date, end_date, parameters, area):
        if(len(parameters) == 0):
            raise Exception("Parameters can't be empty")
        if(area==""): # todo: check to match with area pattern
            raise Exception("Area is not specified")
        if(start_date == ""): # todo: check to match datetime pattern
            raise Exception("Start date is not specified")
        elif (end_date == ""): # todo: check to match datetime pattern
            raise Exception("End date is not specified")

        dataList = pd.date_range(start_date,end_date).tolist()
        df = pd.to_datetime(dataList)
        pathList = []

        parameterFolder = ''
        for paramName in parameters:
            parameterFolder += paramName + "_"

        area_folder = ''
        for area_coordinate in area:
            area_folder += str(area_coordinate) + "_"

        relative_path = DataRetriver.download_path + parameterFolder + "/" + area_folder +"/"; 

        if(not os.path.exists(relative_path)):
            os.makedirs(relative_path)

        for i in df:

            file_name = str(i.year)+"_"+str(i.month).zfill(2)+"_"+str(i.day).zfill(2)+".nc"

            file_path =  relative_path + file_name
            pathList.append(file_path)

            if(os.path.exists(file_path)):
                # print(f"File {file_path} already exist.")
                continue
            else:
                # print(i.year,i.month,i.day)
                DataRetriver.retrieve_single_day_data_func(str(i.day).zfill(2), 
                                                           str(i.month).zfill(2), 
                                                           i.year, 
                                                           parameters, 
                                                           area, 
                                                           file_path)

        return pathList
        
    @staticmethod
    def retrive_data_xarray(start_date, end_date, parameters, area):
        pathList = DataRetriver.retrive_data(start_date, end_date, parameters, area)
        retrived_days_data = []

        for file_path in pathList:
            # print(file_path)
            ds = xr.open_dataset(file_path)
            retrived_days_data.append(ds)

        return retrived_days_data
        
    @staticmethod
    def retrive_custom_data(startDate, endDate, properties, long_min, long_max, lat_min,lat_max):
        # [N,W,S,E]
        area = [lat_max, long_min, lat_min, long_max]
        return DataRetriver.retrive_data_xarray(startDate, endDate, properties, area)

