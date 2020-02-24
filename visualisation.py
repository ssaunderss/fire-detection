'''
Project: Fire-Detection
File Name: visualisation.py
Group Members:  Sergiu Iliev, Yuan Li, Austin Saunders, Peng Zeng
Capabilities: Takes cleaned data and visualizes it on a map of Australia using plotly
MIT License, Copyright (c) 2020, Sergiu Iliev, Austin Saunders, Peng Zeng, Yuan Li

Install instructions
Required Package: plotly
$ conda install -c plotly plotly=4.5.0

Dependency Notes
main.py imports this module

Import Notes
This module imports
 - pandas so we can read a previously generated csv
 - plotly graph objects so we can graph the results
'''

import pandas as pd
import plotly.graph_objects as go

def generate_map(results):
    fig = go.Figure(go.Densitymapbox(lat=results.latitude, lon=results.longitude, z=results.Risk,
                                    radius=1))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig.show()

if __name__ == "__main__":
    # If called directly, the function generates a map of the input risk data
    results = pd.read_csv('data/riskcalculation.csv')
    generate_map(results)