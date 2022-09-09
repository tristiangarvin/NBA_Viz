from dash import Dash
import dash_bootstrap_components as dbc

from layout import content_layout
from callback import get_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],  # bootstrap theme settings
           meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.2, minimum-scale=0.5,"}
]
)
server = app.server

app.layout = content_layout

get_callbacks(app)

if __name__ == "__main__":
    while True:
        app.run_server(debug=True)