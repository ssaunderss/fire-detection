'''
Install instructions
Required Package: plotly
$ conda install -c plotly plotly=4.5.0

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