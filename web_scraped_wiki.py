'''
might need to work on the execution of this script because it runs into problems outside of
jupyter notebook
'''

#import all modules
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

#Open the url to be scraped
url = "https://en.wikipedia.org/wiki/List_of_major_bushfires_in_Australia"
page = urllib.request.urlopen(url)

#Convert page to a beautifulsoup object
soup = BeautifulSoup(page, "lxml")

#Need to find the table
fire_table = soup.find('table', class_='wikitable sortable')

#Set up individual lists for each of the columns
Date = []
#Name = []
States = []
HA = []
Acres = []
Fatalities = []
Homes = []
Other_Buildings = []
Other_Damage = []
Notes = []

#go through each row and append each cell to respective list
for row in fire_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) == 10:
        Date.append(cells[0].find(text=True).strip("\n"))
        #Name.append(cells[1].find(text=True).strip("\n"))
        States.append(cells[2].find(text=True).strip("\n"))
        HA.append(cells[3].find(text=True).strip("\n"))
        Acres.append(cells[4].find(text=True).strip("\n"))
        Fatalities.append(cells[5].find(text=True).strip("approx. \n"))
        Homes.append(cells[6].find(text=True).strip("approx. \n"))
        Other_Buildings.append(cells[7].find(text=True).strip("approx. \n"))
        Other_Damage.append(cells[8].find(text=True).strip("\n"))
        Notes.append(cells[9].find(text=True).strip("\n"))

#Convert all relevant scraped cells into a DataFrame
fire_df = pd.DataFrame(Date, columns=["Date"])
fire_df["States"] = States
fire_df["HA"] = HA
fire_df["Acres"] = Acres
fire_df["Fatalities"] = Fatalities
fire_df["Homes"] = Homes
fire_df["Other Buildings"] = Other_Buildings
fire_df["Other Damage"] = Other_Damage

#Need to do some extra cleaning on the dataframe
fire_df = fire_df.replace(to_replace = "Nil", value = "0")

#Write the DataFrame to a csv file in the data file
fire_df.to_csv (r'data/fire_table.csv', index = None, header=True)

