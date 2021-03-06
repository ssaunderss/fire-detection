'''
Project: Fire-Detection
File Name: Websource.py
Group Members:  Yuan Li, Austin Saunders, Sergiu Iliev, Peng Zeng
Capabilities: Scrapes two websites: historical fires in Australia and lists of cities in Australia, then cleans the
data for visualization
MIT License, Copyright (c) 2020, Sergiu Iliev, Austin Saunders, Peng Zeng, Yuan Li

Dependency Notes
main.py imports this module

Import Notes
This module imports
 - urllib request to connect to website
 - beautifulsoup4 to scrape websites and convert them to an object that is easy to work with
 - plotly graph objects and express so we can visualize our results
 - pandas and numpy so that we can manipulate large data sets and perform vectorized operations
'''
#import all modules
import urllib.request
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# Part 1, get a list of city for visualization ploting
def historical_map():
    # get lat and long for list of australia cities
    city_df = pd.read_html('https://www.latlong.net/category/cities-14-15.html')
    city_df = city_df[0]


    # split the city, state and country
    s = city_df['Place Name'].str.split(", ", n = 2, expand = True)

    city_df["City"]= s[0]
    city_df["State"]= s[1]
    city_df["Country"]= s[2]

    pd.options.mode.chained_assignment = None

    # cleaning
    city_df['City'][8] = 'Chessnok'
    city_df['State'][8] = 'NSW'
    city_df['Country'][8] = 'Australia'
    city_df['City'][71] = 'Greenvale'
    city_df['State'][71] = 'Victoria'
    city_df['Country'][71] = 'Australia'
    city_df['City'][83] = 'Gladstone'
    city_df['State'][83] = 'QLD'
    city_df['Country'][83] = 'Australia'
    city_df['City'][80] = 'Gladstone'
    city_df['State'][80] = 'QLD'
    city_df['Country'][80] = 'Australia'
    city_df['State'] = city_df['State'].str.replace('Queensland', 'QLD')
    city_df['State'] = city_df['State'].str.replace('Tasmania', 'TAS')
    city_df['State'] = city_df['State'].str.replace('Victoria', 'VIC')
    city_df['State'] = city_df['State'].str.replace('Canberra', 'ACT')
    city_df['State'] = city_df['State'].str.replace('Northern Territory', 'NT')


    # Part 2, summarize historical numbers by state

    #Open the url to be scraped
    url = "https://en.wikipedia.org/wiki/List_of_major_bushfires_in_Australia"
    page = urllib.request.urlopen(url)

    #Convert page to a beautifulsoup object
    soup = BeautifulSoup(page, "lxml")

    #Need to find the table
    fire_table = soup.find('table', class_='wikitable sortable')

    #Set up individual lists for each of the columns
    Date = []
    States = []
    HA = []
    Acres = []
    Fatalities = []
    Homes = []

    #go through each row and append each cell to respective list
    for row in fire_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 10:
            Date.append(cells[0].find(text=True).strip("\n"))
            States.append(cells[2].find(text=True).strip("\n"))
            HA.append(cells[3].find(text=True).strip("\n"))
            Acres.append(cells[4].find(text=True).strip("\n"))
            Fatalities.append(cells[5].find(text=True).strip("approx. \n"))
            Homes.append(cells[6].find(text=True).strip("approx. \n"))

    #Convert all relevant scraped cells into a DataFrame
    fire_df = pd.DataFrame(Date, columns=["Date"])
    fire_df["States"] = States
    fire_df["Area_burned"] = HA
    fire_df["Fatalities"] = Fatalities
    fire_df["Homes_damaged"] = Homes

    #Need to do some extra cleaning on the dataframe
    fire_df = fire_df.replace(to_replace = "Nil", value = "0")

    # cleaning
    fire_df['Area_burned'] = fire_df['Area_burned'].str.replace(',', '')
    fire_df['Fatalities'] = fire_df['Fatalities'].str.replace(',', '')
    fire_df['Homes_damaged'] = fire_df['Homes_damaged'].str.replace(',', '')
    fire_df['Homes_damaged'] = fire_df['Homes_damaged'].str.replace(',', '')
    fire_df['Area_burned'][7] = 160000
    fire_df['Fatalities'][4] = 20
    fire_df['Homes_damaged'][19] = 0
    fire_df['Year'] = fire_df['Date'].str[-4:]
    fire_df['Year'][197] = 2020

    # transform data type to numeric
    fire_df['Area_burned'] = pd.to_numeric(fire_df['Area_burned'], errors='coerce')
    fire_df['Fatalities'] = pd.to_numeric(fire_df['Fatalities'], errors='coerce')
    fire_df['Homes_damaged'] = pd.to_numeric(fire_df['Homes_damaged'], errors='coerce')
    fire_df['Year'] = pd.to_numeric(fire_df['Year'], errors='coerce')

    # pivot table to get summary by state
    df1=pd.pivot_table(fire_df, index=['States'],values=['Area_burned','Fatalities','Homes_damaged'],aggfunc=np.sum)
    df2=fire_df.groupby('States').Date.nunique()
    wiki_df = pd.concat([df1,df2],axis=1)
    wiki_df= wiki_df.rename(columns={'Date': 'FireCount'})
    wiki_df['State_ab']=('NA', 'ACT', 'NW', 'NSW', 'NT', 'SA', 'TAS', 'VIC', 'WA')

    # left join two dataframes
    combine_df = pd.merge(left=city_df,right=wiki_df, how='left', left_on='State', right_on='State_ab')
    # print(combine_df)
    combine_df.to_csv ('data/websource_combined.csv', header=True)
   
    # plot on map
    fig = px.scatter_mapbox(combine_df, lat="Latitude", lon="Longitude", hover_name="City",
                            hover_data=["Fatalities", "Area_burned", "Homes_damaged", "FireCount"],zoom=3)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()