from optparse import Values
from turtle import position
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


def get_callbacks(app):
    @ app.callback(
    Output('filter_dropdown_player', 'options'),
    Output('filter_dropdown_player', 'value'),
    Input('filter_dropdown_team', 'value'),
    )
    def update_player_dropdown(team):
        dff = df[df['TEAM_NAME'] == team]
        dff = dff.sort_values('shot_count', ascending=False)
        player_select = [{"label": player, "value": player}
                        for player in dff.PLAYER_NAME.unique()]
        value = player_select[0]["value"]
        return player_select, value
    @ app.callback(
        [
            Output('shot-chart', 'figure'),
            Output('filter_dropdown_game', 'options'),
            Output('game-points', 'children'),
            Output('player-percentage', 'children'),
            Output('overall-percentage', 'children'),
            Output('overall-points', 'children'),
            Output('highest-game', 'children'),
            Output('line-chart', 'figure'),
            Output('pie-chart', 'figure'),
            Output('bar-chart', 'figure'),
        ],
        [
            Input('filter_dropdown_player', "value"),
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

        df4 = df2
        df4['shot_count'] = df4.groupby('SHOT_TYPE')['PLAYER_ID'].transform('count')

        pie = px.pie(df4, values='shot_count', names='SHOT_TYPE', color='SHOT_TYPE', hole=.5, color_discrete_map={'2PT Field Goal':'#E85669','3PT Field Goal':'#25A9F3',})
        pie.update_traces(textposition='inside', textinfo='percent+label')

        pie.update_layout(
            {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)'
            },
            showlegend=False,
            autosize=False,
            margin={'t': 0, 'l': 0, 'b': 100, 'r': 0},
            font_color="white",
            hovermode="x",
        )



        df3 = df2.drop_duplicates(subset=["GAME_NAME"])
        line = px.line(df3, x="dates", y="gamepoints", title='Points Scored Per Game', markers=True,
                    labels={
                        "gamepoints": "Points",
                        "dates": "Game",
                    }, hover_data=['GAME_NAME'],)
        line.update_traces(line_color='#41A3CA',)
        line.update_layout(
            {
            'paper_bgcolor': '#32383E',
            'plot_bgcolor': '#32383E'
            },
            showlegend=False,
            autosize=False,
            margin={'t': 60, 'l': 70, 'b': 20, 'r': 0,},
            font_color="white",
        )



        line.update_xaxes(range=[min('dates'), max('dates')], showgrid=False, fixedrange=False)

        line.update_yaxes(range=[0, 50], showgrid=False, dtick=5)
    
        high = df3[df3.gamepoints == df3.gamepoints.max()]
        low = df3[df3.gamepoints == df3.gamepoints.min()]

        highscore = high['gamepoints'].iloc[0].item()
        lowscore = low['gamepoints'].iloc[0].item()

        line.add_annotation(text='Game High ' + str(highscore) + ' Points', y=high.iloc[-1]['gamepoints'], x=high.iloc[-1]['dates'], arrowcolor='white')
        line.add_annotation(text=str(lowscore) + ' Points', y=low.iloc[0]['gamepoints'], x=low.iloc[0]['dates'], arrowcolor='white', font=dict(color="#E85669"))


        top = pd.DataFrame().assign(PLAYER_NAME=df2['PLAYER_NAME'], POINTS=df2['gamepoints'], GAME=df2['GAME_NAME'])
        top = top.drop_duplicates(subset=["GAME"])
        top = top.sort_values('POINTS', ascending=False)
        top = top.head(10)

        action = pd.DataFrame().assign(PLAYER_NAME=df2['PLAYER_NAME'], ACTION=df2['ACTION_TYPE'], PLAYER_ID=df2['PLAYER_ID'])
        action['count'] = action.groupby('ACTION')['PLAYER_ID'].transform('count')
        action = action.drop_duplicates()
        action = action.sort_values('count', ascending=False)
        
        skeet = action
        skeet = skeet.head(10)
        bar = px.bar(skeet, x='ACTION', y='count', title='Most Frequent Shots Taken',)

        bar.update_layout(
            {
            'paper_bgcolor': '#32383E',
            'plot_bgcolor': '#32383E'
            },
            showlegend=False,
            autosize=False,
            margin={'t': 60, 'l': 70, 'b': 0, 'r': 0},
            font_color="white",
            hovermode="x",
        )
        bar.update_xaxes(showgrid=False)
        bar.update_yaxes(showgrid=False,)
        bar.update_traces(marker_color='#25A9F3')



        action = action.head(10)
        action = top.values.tolist()

        player_points = [html.P([f'{str(s[2])}', ], className='mb-0 pb-0') for s in action]

        games = len(df2['GAME_ID'].unique())

        if player:
            shots_taken = len(df2)
            shots_made = len(df2.loc[df2['SHOT_MADE_STRING'] == '1'])
            percentage = shots_made/shots_taken
            percentage = "{:.1%}".format(percentage)
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
            dff = dff[dff['GAME_NAME'].isin(game)]

        if game:
            try:
                game_points = dff['points'].sum()
                shots_taken = len(dff)
                shots_made = len(dff.loc[dff['SHOT_MADE_STRING'] == '1'])
                game_percentage = shots_made/shots_taken
                game_percentage = "{:.2%}".format(game_percentage)
            except:
                pass

        player_chart = px.scatter(dff, x="LOC_X", y="LOC_Y", color="SHOT_MADE_STRING", color_discrete_sequence=[
                                "#E85669", "#41A3CA"], category_orders={"SHOT_MADE_STRING": ['0', '1']},)
        
        max_points = dff['points'].max()



        player_chart.update_xaxes(range=[250, -250], visible=False, fixedrange=True,)
        player_chart.update_yaxes(range=[-55, 420], visible=False, fixedrange=True,)

        player_chart.update_layout(
            showlegend=False,
            autosize=False,
            margin={'t': 0, 'l': 0, 'b': 5, 'r': 0}
        )

        player_chart.update_layout({
            'paper_bgcolor': 'rgba(0,0,0,0)',
            #'plot_bgcolor': '#32383E',
            'plot_bgcolor': 'rgba(0,0,0,0)',
        })

        player_chart.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )

        player_chart.add_layout_image(
            dict(
                source="https://i.ibb.co/HCZ3m50/nba-court.png",
                xref="x",
                yref="y",
                x=250,
                y=415,
                sizex=500,
                sizey=470,
                sizing="stretch",
                opacity=1,
                layer="below",
            )
        )

        player_chart.update_traces(marker=dict(size=10, opacity=1,
                                            line=dict(width=1,
                                                        color='darkslategrey')),
                                selector=dict(mode='markers'))
        
        line.add_hline(y=points, line_width=3, line_dash="dash", line_color="white")
        

        return player_chart, [{"label": game, "value": game} for game in dff.GAME_NAME.unique()], f'Points Scored (Selected): {game_points}', f'Shooting Percentage (Selected): {game_percentage}', f'Overall Shooting Percentage: {percentage}', f'Points Per Game (No Free-throws): {points}', player_points, line, pie, bar


