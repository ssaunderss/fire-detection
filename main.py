'''
Project: Fire-Detection
Capabilities: Visualise all the fires in target region of the word using data from historical NASA satellites and mark the most impactful fires.
MIT License, Copyright (c) 2020, Sergiu Iliev, Austin Saunders, Peng Zeng, Yuan Li

Installation Instructions & Description: please see Readme 
'''
from visualisation import generate_map
import subprocess
import process_data as pro
import Risk_Calculation as rc
import Websource as ws
import pandas as pd

# first we need the user to decide if they will be processing all new data or be using our data
user_input = False
answer = "y"
while user_input:
  try:
    print("""By default we use pre-cleaned data to demonstrate the capabilities of this code,
    if you would like to use up to date data, you will have to process the data on your own.
     This process takes a significant amount of time ~2 hours, so we recommend just using the data
     we have already process.""")
    answer = input("Would you like to use default data? (y/n)")
  except:
    print("Wrong format")
    user_input = False
  if answer != "y" and answer != "n":
    print("You have to enter either \"y\" or \"n\", please try again")
  else:
    user_input = False

# if the user wants to use new data, this will call the process_data file and reprocess all data and
# return new data to display
if answer == "n":
  pro.transform_data()
  #refreshes the risk calculation so the map will also have up to date data
  rc.calc_risk()

#Before visualizing, need to grab the riskcalculation.csv
results = pd.read_csv("data/riskcalculation.csv")

# Call the Visualise function
generate_map(results)
ws.historical_map()