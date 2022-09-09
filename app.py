from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
import os
import numpy as np

from layout import content_layout
from data import df
from callback import get_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],  # bootstrap theme settings
           meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.2, minimum-scale=0.5,"}
]
)
server = app.server  # define flask app.server

# dir = "C:\\Users\\trist\Documents\\CodeRepository\\DogImageAPI\\nba"
# os.chdir(dir)

# dir = "C:\\Users\\tgarvin\\Desktop\\Projects\\dash"
# os.chdir(dir)

app.layout = content_layout

get_callbacks(app)

if __name__ == "__main__":
    while True:
        app.run_server(debug=True)