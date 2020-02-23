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

# look through the confidence, there are some string "h", "n" and "l"
# This instruction is to convert these three strings to "100", "50" and "0"
def convertConfidence(confidence):
    for i in tqdm(iterable = range(len(confidence)), desc = "Convert confidence"):
        for j in range(len(confidence[i])):
            if isinstance(confidence[i][j], str):
                if confidence[i][j] == "h":
                    confidence[i][j] = 100
                elif confidence[i][j] == "n":
                    confidence[i][j] = 50
                elif confidence[i][j] == "l":
                    confidence[i][j] = 0
    return confidence

def calc_risk():
    # read the cleaned and procesed data
    c_df = pd.read_csv('data/combined_dataframes.csv')

    # Convert the contents of the pandas array from strings looking like lists to actual lists
    brightness_MODIS = c_df.loc[:,'bright_ti4'].apply(ast.literal_eval) # brightness from MODIS
    brightness_VIIRS = c_df.loc[:,'bright_ti5'].apply(ast.literal_eval) # birghtness from VIIRS
    confidence = c_df.confidence.apply(ast.literal_eval)
    instrument = c_df.loc[:,'instrument'].apply(ast.literal_eval)

    # Convert every element in confidence to integer
    confidence = convertConfidence(confidence)
    c_df.confidence = confidence

    # Initialise the risk vector
    risk = np.zeros(len(c_df.latitude))

    # Calculate brightness by confidence weighted average
    for i in tqdm(iterable = range(len(confidence)), desc = "Calculate brightness by confidence weighted average"):
        for j in range(len(confidence[i])):
            if len(confidence[i]) == len(brightness_MODIS[i]) == len(brightness_VIIRS[i]):
                risk[i] += ((confidence[i][j] * 0.01) * (brightness_MODIS[i][j]) + (confidence[i][j] * 0.01)
                            * (brightness_VIIRS[i][j])) / len(confidence[i])
        else:
            risk[i] = (statistics.mean(confidence[i])) * 0.01 * statistics.mean(brightness_MODIS[i]) + \
                      (statistics.mean(confidence[i]) * 0.01) * statistics.mean(brightness_VIIRS[i])

    # Calculate the average of each of the brightnesses
    for i,list in enumerate(tqdm(iterable = risk, desc = "Calculate the brightness average")):
        # divide by the number of instruments i.e. mean of 1 or mean of 2
        risk[i] = risk[i] / len(instrument[i])

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

    # generate columns called TimeRange and Risk
    c_df["TimeRange"] = timeRange
    c_df['Risk'] = risk

    # export the risk as a CSV
    c_df.to_csv("data/riskcalculation.csv")