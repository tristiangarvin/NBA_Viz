from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from data import df

dropdownteam = dcc.Dropdown(
    id="filter_dropdown_team",
    options=[{"label": team, "value": team}
             for team in sorted(df.TEAM_NAME.unique())],
    placeholder="-Select a Team-",
    multi=False,
    value='Dallas Mavericks',
    clearable=False,
)

dropdownshottype = dcc.Dropdown(
    id='filter_dropdown_shot_type',
    placeholder="-Shot Type-",
    multi=False,
    clearable=True,
)

dropdowngame = dcc.Dropdown(
    id="filter_dropdown_game",
    placeholder="-Select a Game (Clear for All)-",
    value=[],
    multi=True,
)

dropdownplayer = dcc.Dropdown(
    id="filter_dropdown_player",
    placeholder="-Select a Player-",
    clearable=False,
)

dropdownmake = dcc.RadioItems(
    id="filter_dropdown_make",
    options=[
        {"label": "All Shots", "value": 'All Shots'},
        {"label": "Makes", "value": 'Makes'},
        {"label": "Misses", "value": 'Misses', },
    ],
    value="All Shots",
    style={'margin-right': '20px'}
)

filter_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5('Chart Filters', className="card-title"),
            dropdownteam,
            html.Div(className="mb-2"),
            dropdownplayer,
            html.Div(className="mb-2"),
            dropdowngame,
            html.Div(dropdownmake, className="mt-2"),
            html.Hr(),
            html.Div(className="mb-2"),
            html.B(id='overall-percentage', className='small-header'),
            html.P(id='player-percentage'),
            html.B(id='overall-points', className='small-header'),
            html.P(id='game-points'),
            html.Hr(),
            html.B('Highest Scoring Games:', className='small-header'),
            html.Div(children=[html.P(id="highest-game"), ]),
        ]
    ), className=""
)

header_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1('NBA Shot Chart Data',),
            html.P('For the 2021-2022 NBA Regular Season (Free-throws not included)',
                   className="m-0 p-0"),
        ]
    )
)

content_layout = dbc.Container([
    dbc.Row([
        header_card,
    ],),
    dbc.Row([
            dbc.Col([
                filter_card,
            ], className="pt-3", lg=3,),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                    dcc.Graph(id='shot-chart', figure={}, responsive=True,
                              config={'displayModeBar': False, },), ], lg=5, className="pt-3 pb-3",),
                    dbc.Col([
                        dcc.Graph(id='line-chart', figure={}, responsive=True,
                                  config={'displayModeBar': False, },),
                    ], className="pt-3 pb-3", lg=7),
                ],),
                dbc.Row([
                    dbc.Col([],lg=1),
                    dbc.Col([
                            dcc.Graph(id='pie-chart', figure={}, responsive=True, config={'displayModeBar': False, },), 
                        ], lg=3, className='pt-3'),
                    dbc.Col([],lg=1),
                    dbc.Col([
                        dcc.Graph(id='bar-chart', figure={}, responsive=True,
                                  config={'displayModeBar': False, },),
                    ], lg=7, className='pt-3',),
                ]),
            ], lg=9),
                
        ], className='align-items-stretch', justify="between",),
    dbc.Row([
    ]),
    dbc.Row([
        dbc.Col(
        )
    ])], fluid= True)
