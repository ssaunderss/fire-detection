'''
Project: Fire-Detection
File Name: main.py
Group Members: Austin Saunders, Sergiu Iliev, Peng Zeng, Yuan Li
Capabilities: Visualise all the fires in target region of the word using data from historical NASA satellites and
mark the most impactful fires.
MIT License, Copyright (c) 2020, Sergiu Iliev, Austin Saunders, Peng Zeng, Yuan Li

Import Notes
This file imports
 - process_data.py so we can load and transform VIIRS/MODIS satellite data
 - Risk_Calculation.py so we can generate historical risk scores for cleaned lat/long coords
 - Websource.py so we can scrape historical fire/Australian city name information
 - visualisation.py so we can visualise our end product
 - pandas so we can read a previously generated csv
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
print("By default we use pre-cleaned data to demonstrate the capabilities of our code,")
print("if you would like to use newer data, you will have to process the data on your")
print("own. This process takes a significant amount of time ~2 hours, so we recommend")
print("using our pre-processed data.\n\n")
while user_input == False:
  try:
    answer = input("Would you like to use default data? (y/n): ")
  except:
    print("Wrong format")
    user_input = False
  if answer != "y" and answer != "n":
    print("You have to enter either \"y\" or \"n\", please try again")
  else:
    user_input = True

# if the user wants to use new data, this will call the process_data file and reprocess all data and
# return new data to display
if answer == "n":
  pro.transform_data()
  #refreshes the risk calculation so the map will also have up to date data
  rc.calc_risk()

#Before visualizing, need to grab the riskcalculation.csv
results = pd.read_csv("data/riskcalculation.csv")

# Call the Visualise function
# Generating the map takes around 2 minutes
generate_map(results)
ws.historical_map()