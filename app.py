from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from flask import Flask,request
import os
import numpy as np

server = Flask(__name__) # define flask app.server

dir = "C:\\Users\\tgarvin\\Desktop\\Projects\\dash"
os.chdir(dir)

df = pd.read_csv('AllStats.csv')
df['SHOT_MADE_STRING'] = df['SHOT_MADE_FLAG'].astype(str)
df['count'] = df.groupby('PLAYER_ID')['PLAYER_ID'].transform('count')
df = df[df['count'] > 100]
df = df[df['LOC_Y'] < 420]
df = df.sort_values(by='count', ascending=False)
df['dates'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')
df['dates']=df['dates'].astype(str)

df['GAME_NAME'] = df['HTM'] + ' @ ' + df['VTM'] + ' ' + df['dates']

conditions = [
    (df['SHOT_TYPE'] == '3PT Field Goal') & (df['SHOT_MADE_FLAG'] == 1),
    (df['SHOT_TYPE'] == '2PT Field Goal') & (df['SHOT_MADE_FLAG'] == 1),
    (df['SHOT_MADE_FLAG'] == 0)]
choices = [3,2,0]
df['points'] = np.select(conditions, choices)

df['gamepoints'] = df.groupby(['PLAYER_ID', 'GAME_ID'])['points'].transform('sum')
df['gamepoints'] = df['gamepoints'].astype(str)

df['GAME_NAME'] = df['HTM'] + ' @ ' + df['VTM'] + ' ' + df['dates'] + ' (' + df['gamepoints'] + ' Points Scored)'
df['gamepoints'] = df['gamepoints'].astype(int)
df

top = pd.DataFrame().assign(PLAYER_NAME=df['PLAYER_NAME'], POINTS=df['gamepoints'], GAME=df['GAME_NAME'])
top = top.drop_duplicates()
top = top.sort_values('POINTS', ascending=False)
top = top.head(20)

result = top.values.tolist()

result

# for i in result:
#     print(str(i[0]) + ': ' + str(i[2]))

df = df.sort_values('dates')


def generate_top(top_shortName):
    return html.P(children=str(top_shortName),
                      className="mr-1",
                      id=str(top_shortName))


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE], #bootstrap theme settings
            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
            )

dropdownteam =  dcc.Dropdown(
            id="filter_dropdown_team",
            options=[{"label": team, "value": team} for team in sorted(df.TEAM_NAME.unique())],
            placeholder="-Select a Team-",
            multi=False,
            value='Dallas Mavericks'
            )

dropdowngame =  dcc.Dropdown(
            id="filter_dropdown_game",
            placeholder="-Select a Game (Clear for All)-",
            )

dropdown =  dcc.Dropdown(
            id="filter_dropdown",
            placeholder="-Select a Player-",
            )

dropdownmake =  dcc.Dropdown(
            id="filter_dropdown_make",
            options=['All Shots', 'Makes', 'Misses'],
            value="All Shots",
            )

app.layout = dbc.Container([
    dbc.Row([
            dbc.Col([
                html.H1('NBA Shot Chart Data', className="text-white"),
                html.P('For the 2021-2022 NBA Season (Free-throws not included)', className=""),
                dropdownteam,
                html.Div(className="mb-2"),
                dropdown,
                html.Div(className="mb-2"),
                dropdownmake,
                html.Div(className="mb-2"),
                dropdowngame,
                html.Hr(),
                html.Div(className="mb-2"),
                html.B(id='player-percentage', className='text-white'),
                html.P(id='overall-percentage'),
                html.B(id='my-output', className='text-white'),
                html.P(id='overall-points'),
            ], className="my-auto", lg=3),
            dbc.Col([], lg=1),
            dbc.Col([
                    dcc.Graph(id='shot-chart', figure={}, responsive=True, style={'height': 750}, config={'displayModeBar': False,},),
                ], lg=5, className="my-auto pb-3",),
            dbc.Col([
                #dcc.Graph(id="player-info", figure={})
                # html.P(children=[generate_top(str(i[0]) + ': ' + str(i[2])) for i in result])
            ],lg=3),
    ], justify="between", style={'height': '100vh'}),
    dbc.Row([
    ]),
    dbc.Row([
        dbc.Col(
        )
    ])
], fluid=True)

@app.callback(
    Output('filter_dropdown', 'options'),
    Input('filter_dropdown_team', 'value'),
)
def update_player_dropdown(team):
    dff = df[df['TEAM_NAME'] == team]
    dff = dff = dff.sort_values('count', ascending=False)
    return [{"label": player, "value": player} for player in dff.PLAYER_NAME.unique()]

@app.callback(
    [
        Output('shot-chart', 'figure'),
        Output('filter_dropdown_game', 'options'),
        Output('my-output', 'children'),
        Output('player-percentage', 'children'),
        Output('overall-percentage', 'children'),
        Output('overall-points', 'children'),
    ],
    [
        Input('filter_dropdown', "value"),
        Input('filter_dropdown_make', "value"),
        Input('filter_dropdown_game', "value"),
    ]
)
def update_chart(player, make_miss, game):
    percentage = ''
    game_percentage = ''
    points = ''
    game_points = ''

    df2 = df[df['PLAYER_NAME'] == player]
    games = len(df2['GAME_ID'].unique())


    if player:
        shots_taken = len(df2)
        shots_made = len(df2.loc[df2['SHOT_MADE_STRING'] == '1'])
        percentage = shots_made/shots_taken
        percentage = "{:.2%}".format(percentage)
        points = df2['points'].sum()
        points = points/games
        points = points.round(1)

    if make_miss == 'Makes':
        df2 = df2[df2['SHOT_MADE_FLAG'] == 1]
    elif make_miss == 'Misses':
        df2 = df2[df2['SHOT_MADE_FLAG'] == 0]

    dff = df2

    if not game:
        dff = df2
    else:
        dff = dff[dff['GAME_NAME'] == game]
    
    if game:
        try:
            game_points = dff['points'].sum()
            shots_taken = len(dff)
            shots_made = len(dff.loc[dff['SHOT_MADE_STRING'] == '1'])
            game_percentage = shots_made/shots_taken
            game_percentage = "{:.2%}".format(game_percentage)
        except:
            pass


    player_chart = px.scatter(dff, x="LOC_X", y="LOC_Y", color="SHOT_MADE_STRING", color_discrete_sequence=["red", "blue"], category_orders={"SHOT_MADE_STRING": ['0', '1']},)
    player_chart.update_xaxes(range=[250, -250], visible=False)
    player_chart.update_yaxes(range=[-47.5, 422.5], visible=False)
    player_chart.update_layout (
        showlegend=False,
        autosize=False,
        margin={'t': 0,'l':10,'b':0,'r':10}
    )

    player_chart.update_layout ({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)'
    })

    player_chart.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
        gridcolor='rgba(0,0,0,0)'
    )

    player_chart.add_layout_image(
        dict(
            source= "https://i.ibb.co/Yp8dtW0/court.jpg",
            xref="x",
            yref="y",
            x = 250,
            y = 410,
            sizex=500,
            sizey= 470,
            sizing="stretch",
            opacity=1,
            layer="below",
        )
    )
    player_chart.update_traces(marker=dict(size=20, opacity=.6,
                              line=dict(width=1,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

    return player_chart, [{"label": game, "value": game} for game in df2.GAME_NAME.unique()], f'Game Points Scored: {game_points}', f'Game Shooting Percentage: {game_percentage}', f'Overall Shooting Percentage: {percentage}', f'Points Per Game (No Free-throws): {points}'


if __name__ == "__main__":
    while True:
        app.run_server(debug=True)
