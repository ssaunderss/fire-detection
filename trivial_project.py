
# File:      trivial_project.py
# Author(s): John Ostlund

import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 15 day weather forecast for Pittsburgh on Aug. 30, 2018

pwfc = '''
Date    Hi(F)  Lo(F)  %Hum
AUG 30     79     64    60
AUG 31     82     66    20
SEP  1     85     68    20
SEP  2     85     68    30
SEP  3     87     69    30
SEP  4     87     69    20
SEP  5     87     69    20
SEP  6     85     67    20
SEP  7     81     63    30
SEP  8     79     61    20
SEP  9     77     61    20
SEP 10     77     59    20
SEP 11     77     59    20
SEP 12     77     59    20
SEP 13     77     59    50
'''

pwfc_lines = pwfc.split('\n')
# pwfc_lines is a list of lines
# print('type(pwfc_lines):', type(pwfc_lines))

# pwfc_lines has empty lines at the beginning and end
# print("len(pwfc_lines):", len(pwfc_lines)) # empty lines at

# display the lines in pwfc_lines, with empty lines identified
'''
for line in pwfc_lines:
    if len(line) == 0:
        print('(EMPTY LINE)')
    else:
        print(line)
'''

# delete the first and last lines
pwfc_lines[:1] = []
pwfc_lines[-1:] = []

# now pwfc_lines has no empty lines
# print("len(pwfc_lines):", len(pwfc_lines)) # empty lines at

# display the lines in pwfc_lines, with empty lines identified
'''
for line in pwfc_lines:
    if len(line) == 0:
        print('(EMPTY LINE)')
    else:
        print(line)
'''

# create a Pandas DataFrame (essentially a spreadsheet)
# with days as row labels, and line 0 column names
# as column labels (except for 'Date')
row_labels = []   # start with an empty list, and append
for i in range(1,len(pwfc_lines)):       # skip line 0
    row_labels.append(pwfc_lines[i][:6]) # each day is 6 characters
# print('row_labels:', row_labels)

col_labels = pwfc_lines[0].split()       # split at spaces
col_labels[:1] = []                      # eliminate 'Date'
# print('col_labels:', col_labels)

# create a list of lists of int values for high temp, low temp,
# and % humidity for each day
tbl_temp_hum = []    # start with an empty table
for i in range(1,len(pwfc_lines)):
    line_cols = pwfc_lines[i][6:].split()
    int_cols = []
    for j in line_cols:
        int_cols.append(int(j))
    tbl_temp_hum.append(int_cols)
# print('tbl_temp_hum:')
# print(tbl_temp_hum)

# combine the row labels, column labels, and tbl_temp_hum into
# a DataFrame
df_temp_hum = pd.DataFrame(data=tbl_temp_hum,
                           index=row_labels,
                           columns=col_labels)
# print('df_temp_hum:')
# print(df_temp_hum)

# now that we have wrangled our data, here is the main program:
answer = ''
while answer != 'Q' and answer != 'q':
    print('''
    Please select from this menu:

    1)  Display temp and humidity table
    2)  Plot high and low temperatures
    3)  Display temperature statistics
    Q)  Quit from this program
    ''')
    answer = input('    Your choice: ').strip()
    if answer == '1':
        print(df_temp_hum)
    elif answer == '2':
        # BEWARE the plot may appear BEHIND other windows
        df_temp_hum.loc[:, 'Hi(F)':'Lo(F)'].plot()
        plt.show()
    elif answer == '3':
        print()
        print('    Mean high temp (F):', df_temp_hum['Hi(F)'].mean())
        print('    Mean low temp (F): ', df_temp_hum['Lo(F)'].mean())
        print('    Mean % humidity:   ', df_temp_hum['%Hum'].mean())
        print()
    elif answer == 'q' or answer == 'Q':
        pass   # the loop will terminate
    else:
        print('\n    Your choice is not valid:', answer, '\n')
          
