'''
Project: Fire-Detection
Capabilities: Visualise all the fires in target region of the word using data from historical NASA satellites and mark the most impactful fires.
MIT License, Copyright (c) 2020, Sergiu Iliev, Austin Saunders, Peng Zeng, Yuan Li

Installation instructions:
0. Install Python version 3.7x
1. Place all .py files in the same directory
2. Download and unzip the data files placing them in a ./data directory
3. Install required packages (using conda or pip):
    $ conda install -c plotly plotly=4.5.0
4. Run main.py
'''
import numpy as np
import pandas as pd

### Define/import all functions
## Import VIIRS & MODIS as df
modis_df = pd.read_csv('data/fire_nrt_M6_103976.csv') # for debugging we only import the Near-Real-Time data
viirs_df = pd.read_csv('data/fire_nrt_V1_103977.csv') # for debugging we only import the Near-Real-Time data
##TODO Drop the columns that are not useful to clean the data
##TODO Ling the Web_scraping function

## Generate Global Grid
'''
Generate Global Gid Dataframe which has the holding coordinate pairs for the centers of the cells in a grid with a given resolution
Inputs and their defaults: s_lat , e_lat = -5 , -45 # start and end lat !they have to be in the same hemisphere i.e. same sign
                           s_lon , e_lon = 105, 155 # start and end longitude
                           cell_side_length = 0.75 # kilometers
'''
def grid_generator(s_lat= -5, e_lat=-45, s_lon = 105, e_lon = 155, cell_side_length = 0.75):
  resolution = cell_side_length/(1*100) # degrees of longitude and latitude per kilometer, 1 degree is 100 km at latitude 20 degrees

  lat = np.arange(s_lat, e_lat, np.sign(s_lat)*resolution) # generate latitude vector
  lon = np.arange(s_lon, e_lon, np.sign(s_lon)*resolution) # generate longitude vector
  spatial_grid = np.transpose([np.tile(lat, len(lon)), np.repeat(lon, len(lat))]) # merge the two to form coordinate pairs for the center of each cell
  spatial_grid=pd.DataFrame(spatial_grid) # dataframe holding the centers of each of the grid cells with the given resolution
  return spatial_grid
print(grid_generator())

##TODO Merge the datasets onto the grid

## Call the Visualise function
generate_map(modis_df)