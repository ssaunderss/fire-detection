'''
Install instructions
Required Package: plotly
$ conda install -c plotly plotly=4.5.0

'''
import pandas as pd
import plotly.graph_objects as go

def generate_map(fires):
    fig = go.Figure(go.Densitymapbox(lat=fires.latitude, lon=fires.longitude, z=fires.brightness,
                                    radius=1))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig.show()

if __name__ == "__main__":
    fires = pd.read_csv('data/fire_nrt_M6_103976.csv')
    generate_map(fires)