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
from visualisation import generate_map

modis_df = pd.read_csv('data/fire_archive_M6_103976.csv')
viirs_df = pd.read_csv('data/fire_archive_V1_103977.csv')

##Drop all columns not relevant to modis and viirs dfs
modis_df = modis_df[['latitude','longitude','brightness','acq_date','instrument','confidence','bright_t31']]
viirs_df = viirs_df[['latitude','longitude','bright_ti4','acq_date','instrument','confidence','bright_ti5']]


##TODO Link the Web_scraping function
#subprocess.call('./web_scraped_wiki.py')
#wiki_df = pd.read_csv('data/fire_table.csv')
#Note: the webscraping dependency might run into problems when it runs as a script in some IDEs


## Generate Global Grid
'''
Generate Global Gid Dataframe which has the holding coordinate pairs for the centers of the cells in a grid with a given resolution
Inputs and their defaults: s_lat , e_lat = -5 , -45 # start and end lat !they have to be in the same hemisphere i.e. same sign
                           s_lon , e_lon = 105, 155 # start and end longitude
                           cell_side_length = 0.75 # kilometers
'''
def grid_generator(s_lat= -5, e_lat=-45, s_lon = 105, e_lon = 155, cell_side_length = 0.375):
  resolution = cell_side_length/(1*100) # degrees of longitude and latitude per kilometer, 1 degree is 100 km at latitude 20 degrees
  lat = np.arange(s_lat, e_lat, np.sign(s_lat)*resolution) # generate latitude vector
  lon = np.arange(s_lon, e_lon, np.sign(s_lon)*resolution) # generate longitude vector
  spatial_grid = np.transpose([np.tile(lat, len(lon)), np.repeat(lon, len(lat))]) # merge the two to form coordinate pairs for the center of each cell
  spatial_grid = pd.DataFrame(spatial_grid) # dataframe holding the centers of each of the grid cells with the given resolution
  return spatial_grid
print(grid_generator())

##Cleans lat and long so that they correspond to values generated in our spatial grid by passing
##columns through a lambda function
modis_df['latitude'] = modis_df['latitude'].map(lambda x: (((x + 5) // .00375 ) * .00375) - 5)
modis_df['longitude'] = modis_df['longitude'].map(lambda x: (((x - 105) // .00375) * .00375) + 105)
viirs_df['latitude'] = viirs_df['latitude'].map(lambda x: (((x + 5) // .00375 ) * .00375) - 5)
viirs_df['longitude'] = viirs_df['longitude'].map(lambda x: (((x - 105) // .00375) * .00375) + 105)

#Rename modis brightness columns of dataset so we can concatenate the datasets easily
modis_df.rename(columns={'brightness': 'bright_ti4','bright_t31': 'bright_ti5'}, inplace=True)

#Now that the lat/long correspond to spatial grid, need to groupby lat/long and aggregate the entities
a = modis_df.groupby(['latitude','longitude']).aggregate(lambda x: x.unique().tolist())  #around 20s on sample
b = viirs_df.groupby(['latitude','longitude']).aggregate(lambda x: x.unique().tolist()) #around 6m51s on sample

#Concats the MODIS and VIIRS datasets together
dfs = [a, b]
comb_df = pd.concat(dfs)
comb_df.groupby(['latitude','longitude']).agg(sum)  #around 11m27s on sample

#Need to rename the columns in MODIS df back to what it was pre-concat
modis_df.rename(columns={'bright_ti4': 'brightness','bright_ti5': 'bright_t31'}, inplace=True)

#Generate CSV of combined dataframes
comb_df.to_csv('data/combined_dataframes_entire_dataset.csv')

##TEST: tests that there are cells with more than one entry in them, KEEP this commented
#a = modis_df.groupby(['latitude','longitude']).aggregate(lambda x: x.unique().tolist())
#a.loc[np.array(list(map(len,a.brightness.values)))>1]

#calls the grid_generator object and creates the grid object
grid = grid_generator()
grid.rename(columns={0 : 'lat', 1 : 'long'}, inplace=True)

## Call the Visualise function
#generate_map(comb_df)