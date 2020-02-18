import numpy as np
import pandas as pd
import ast
import time
import datetime
import statistics 
from tqdm import tqdm

# function
def calculateDays(date1, date2):
    day1 = time.strptime(date1, "%Y-%m-%d")
    day1 = datetime.datetime(day1[0], day1[1], day1[2])
    day2 = time.strptime(date2, "%Y-%m-%d")
    day2 = datetime.datetime(day2[0], day2[1], day2[2])
    #today = datetime.datetime.today()
    interval = day1 - day2
    return interval.days

# read the cleaned and procesed data
c_df = pd.read_csv('data/combined_dataframes.csv')

# Convert the contents of the pandas array from strings looking like lists to actual lists
brightness_MODIS = c_df.loc[:,'bright_ti4'].apply(ast.literal_eval)
brightness_VIIRS = c_df.loc[:,'bright_ti5'].apply(ast.literal_eval)
instrument = c_df.loc[:,'instrument'].apply(ast.literal_eval)

# Initialise the risk vector
risk = np.zeros(len(c_df.latitude))

for i,list in enumerate(tqdm(iterable = brightness_MODIS, desc = "Insert brightness_MODIS")):
    risk[i] += statistics.mean(list)

for i,list in enumerate(tqdm(iterable = brightness_VIIRS, desc = "Insert brightness_VIIRS")):
    risk[i] += statistics.mean(list)

# Calculate the average of each of the brightnesses
for i,list in enumerate(tqdm(iterable = risk, desc = "Calculate the average")):
    risk[i] = risk[i] / len(instrument[i]) # divide by the number of instruments i.e. mean of 1 or mean of 2
# risk = np.mean(brightness_MODIS, brightness_VIIRS) # does not work

timeRange = np.zeros(len(c_df.latitude))
timeData = c_df["acq_date"].apply(ast.literal_eval)
for i, value in enumerate(tqdm(iterable = timeData, desc = "Calculate Time Range")):
    # if only one day, the result will be the difference between that and the date today
    if len(value) == 1:
        timeRange[i] = abs(calculateDays("2020-02-15",timeData[i][0]))
    # if more than one day, the result will be the difference between the start day and the end day
    elif len(value) > 1:
        # start day
        date1 = timeData[i][0]
        # end day
        date2 = timeData[i][-1]
        timeRange[i] = abs(calculateDays(date2,date1))
# divided by the time range
for i,list in enumerate(tqdm(iterable = risk, desc = "Generate the final Risk")):
    risk[i] = risk[i] / timeRange[i]

# export the risk as a CSV
c_df['Risk'] = risk
c_df.to_csv("data/riskcalculation.csv")