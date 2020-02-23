import pandas as pd
import numpy as np

def transform_data():
    print("\nLoading the Data Step 1/7")
    ## Import VIIRS & MODIS as df
    modis_df = pd.read_csv('data/fire_archive_M6_103976.csv')
    viirs_df = pd.read_csv('data/fire_archive_V1_103977.csv')
    print("\tStep 1/7 complete!")

    ##Drop all columns not relevant to modis and viirs dfs
    modis_df = modis_df[['latitude','longitude','brightness','acq_date','instrument','confidence','bright_t31']]
    viirs_df = viirs_df[['latitude','longitude','bright_ti4','acq_date','instrument','confidence','bright_ti5']]

    # Generate Global Gid Dataframe which has the holding coordinate pairs for the centers of the cells in a
    # grid with a given resolution. Inputs and their defaults: s_lat , e_lat = -5 , -45
    # start and end lat. They have to be in the same hemisphere i.e. same sign s_lon , e_lon = 105, 155 start and
    # end longitude, cell_side_length = 0.75 # kilometers
    if __name__ == "__main__":
        # Here is an example of the grid we generate and cast to
        # This only runs in main as a test
        def grid_generator(s_lat= -5, e_lat=-45, s_lon = 105, e_lon = 155, cell_side_length = 0.375):
        # degrees of longitude and latitude per kilometer, 1 degree is 100 km at latitude 20 degrees
            resolution = cell_side_length/(1*100)
        # generates the latitude vector
            lat = np.arange(s_lat, e_lat, np.sign(s_lat)*resolution)
        # generates the longitude vector
            lon = np.arange(s_lon, e_lon, np.sign(s_lon)*resolution)
        # merges the two to form coordinate pairs for the center of each cell
            spatial_grid = np.transpose([np.tile(lat, len(lon)), np.repeat(lon, len(lat))])
        # dataframe holding the centers of each of the grid cells with the given resolution
            spatial_grid = pd.DataFrame(spatial_grid)
            return spatial_grid
        print(grid_generator())

    ##Cleans lat and long so that they correspond to values generated in our spatial grid by passing
    ##columns through a lambda function
    print("\nMapping latitude and longitude of MODIS to spatial grid Step 2/7")
    modis_df['latitude'] = modis_df['latitude'].map(lambda x: (((x + 5) // .00375 ) * .00375) - 5)
    modis_df['longitude'] = modis_df['longitude'].map(lambda x: (((x - 105) // .00375) * .00375) + 105)
    print("\tStep 2/7 complete!")
    print("\nMapping latitude and longitude of VIIRS to spatial grid Step 3/7")
    viirs_df['latitude'] = viirs_df['latitude'].map(lambda x: (((x + 5) // .00375 ) * .00375) - 5)
    viirs_df['longitude'] = viirs_df['longitude'].map(lambda x: (((x - 105) // .00375) * .00375) + 105)
    print("\tStep 3/7 complete!")

    #Rename modis brightness columns of dataset so we can concatenate the datasets easily
    modis_df.rename(columns={'brightness': 'bright_ti4','bright_t31': 'bright_ti5'}, inplace=True)

    #Now that the lat/long correspond to spatial grid, need to groupby lat/long and aggregate the entities
    print("\nGrouping MODIS dataframe to aggregate lat/long Step 4/7")
    print("**This may take a few minutes**")
    a = modis_df.groupby(['latitude','longitude']).aggregate(lambda x: x.unique().tolist())
    print("\tStep 4/7 complete!")
    print("\nGrouping VIIRS dataframe to aggregate lat/long Step 5/7")
    print("**This will take about 30 minutes**")
    b = viirs_df.groupby(['latitude','longitude']).aggregate(lambda x: x.unique().tolist())
    print("\tStep 5/7 complete!")
    #Concats the MODIS and VIIRS datasets together
    print("\nConcatenating MODIS and VIIRS and reaggregating Step 6/7")
    dfs = [a, b]
    comb_df = pd.concat(dfs)
    comb_df.groupby(['latitude','longitude']).agg(sum)
    print("\tStep 6/7 complete!")

    #Need to rename the columns in MODIS df back to what it was pre-concat
    modis_df.rename(columns={'bright_ti4': 'brightness','bright_ti5': 'bright_t31'}, inplace=True)

    #Generate CSV of combined dataframes
    print("\nGenerating CSV of output for future use Step 7/7")
    comb_df.to_csv('data/combined_dataframes.csv')
    print("\tStep 7/7 complete!")
    return(comb_df)