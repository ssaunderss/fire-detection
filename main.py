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
#import web_scraped_wiki as wsw
import subprocess

### Define/import all functions
## Import VIIRS & MODIS as df
modis_df = pd.read_csv('data/fire_nrt_M6_103976.csv') # for debugging we only import the Near-Real-Time data
viirs_df = pd.read_csv('data/fire_nrt_V1_103977.csv') # for debugging we only import the Near-Real-Time data

##Drop all columns not relevant to modis and viirs dfs
modis_df = modis_df[['latitude','longitude','brightness','acq_date','instrument','confidence','bright_t31']]
viirs_df = viirs_df[['latitude','longitude','bright_ti4','acq_date','instrument','confidence','bright_ti5']]


##TODO Link the Web_scraping function
#subprocess.call('./web_scraped_wiki.py')
#wiki_df = pd.read_csv('data/fire_table.csv')

#the webscraping dependency might run into problems when it runs as a script in some IDEs


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
  spatial_grid = pd.DataFrame(spatial_grid) # dataframe holding the centers of each of the grid cells with the given resolution
  return spatial_grid
print(grid_generator())

#Clean VIIRS and MODIS dfs lat/long so that they now correspond to the cells generated in the grid
viirs_df['lat'] = np.round(viirs_df['latitude'],4)
viirs_df['long'] = np.round(viirs_df['longitude'],3)
modis_df['lat'] = np.round(modis_df['latitude'],4)
modis_df['long'] = np.round(modis_df['longitude'],3)


##TODO Need to figure out how to come up with an efficient way to tie them together
#Have a one-to-many relationship, so we will assign foreign key values to both of the viirs_df and modis_df
#what's the most efficient way to create a point to our cell table?

grid = grid_generator()
grid.rename(columns={0 : 'lat', 1 : 'long'}, inplace=True)
#grid["primary_key"] = grid[['lat','long']].agg('-'.join, axis=1)

## Call the Visualise function
generate_map(modis_df)