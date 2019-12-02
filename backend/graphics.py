import plotly.graph_objects as go
import plotly.offline as opy

from .sql_requests import *


def author_graph(year):
    a = get_all_authors_and_count_game(year)
    colors = ['black',] * len(a)
    auth = []
    count = []
    for i, j in a:
        auth.append(i)
        count.append(j)

    fig = go.Figure(data=[go.Pie(labels=auth,
                                 values=count,
                                 showlegend=False,
                                 title={'text': 'Количество игр', 'position':'top center', 'font':{'color': 'gold', 'size': 24}}
                                 )],
                    layout=go.Layout(
                        plot_bgcolor='rgba(0,0,0,0.8)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        autosize=False,
                        width=350,
                        height=350,
                        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=4)),)
    div = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})

    return div


def forum_resonance_bar(year):
    a = get_top_forum_resonance(year)
    name = []
    count = []
    for i, j in a:
        name.append(i)
        count.append(j)

    fig = go.Figure(
        data=[go.Bar(
            x=name,
            y=count,
            name='График',
            opacity=1,
            marker={
                'line':{
                    'color': 'rgba(0,0,0,1)',
                },
                'color': 'rgba(255,215,1,1)',
            },
        )],
        layout=go.Layout(
            title={
                'text': 'Количество сообщений в каждой игре',
                'font':{
                    'size': 20,
                    'color': 'gold'
                },

            },
            font={
                'size': 11,
                'color': 'gold'
            },

            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    forum = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})

    return forum


def quality_top_bar(year):
    top_quality_list = get_top_game_quality(year)
    names = []
    quality = []
    for name,  q in top_quality_list:
        names.append(name)
        quality.append(q)

    fig = go.Figure(
        data = [go.Bar(
            x=names,
            y=quality,
            marker={
                'line':{
                    'color': 'rgba(0,0,0,1)',
                },
                'color': 'rgba(255,215,1,1)',
            },
        )],
        layout=go.Layout(
            title={
                'text': 'Качество игр',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    quality_graph = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return quality_graph


def total_players_per_year_bar():
    total_players = get_total_players_per_year()
    count = []
    years = []
    for value, year in total_players:
        count.append(value)
        years.append(int(year))

    fig = go.Figure(
        data = [
            go.Bar(
                x=years,
                y=count,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество игроков по годам',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_player_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_player_bar


def total_players_per_month_bar(year):
    period = year
    total_players = get_total_players_per_month(year)
    count = []
    years = []
    for value, year in total_players:
        count.append(value)
        years.append(year)

    fig = go.Figure(
        data = [
            go.Bar(
                x=years,
                y=count,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество игроков по месяцам (' + str(period) + ' год)',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_players_per_month_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_players_per_month_bar


def total_teams_per_year_bar():
    total_teams = get_total_teams_per_year()
    count = []
    years = []
    for value, year in total_teams:
        count.append(value)
        years.append(int(year))

    fig = go.Figure(
        data = [
            go.Bar(
                x=years,
                y=count,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество команд по годам',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_team_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_team_bar


def total_teams_per_month_bar(year):
    period = year
    total_teams = get_total_teams_per_month(year)
    count = []
    years = []
    for value, year in total_teams:
        count.append(value)
        years.append(year)

    fig = go.Figure(
        data = [
            go.Bar(
                x=years,
                y=count,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество команд по месяцам (' + str(period) + ' год)',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_teams_per_month_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_teams_per_month_bar


def total_teams_per_game_bar(year):
    period = year
    total_teams = get_total_teams_per_game(year)
    count = []
    games = []
    for value, game in total_teams:
        count.append(value)
        games.append(game)

    fig = go.Figure(
        data = [
            go.Bar(
                x=count,
                y=games,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество команд по играм (' + str(period) + ' год)',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_teams_per_game_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_teams_per_game_bar


def total_players_per_game_bar(year):
    period = year
    total_teams = get_total_players_per_game(year)
    count = []
    games = []
    for value, game in total_teams:
        count.append(value)
        games.append(game)

    fig = go.Figure(
        data = [
            go.Bar(
                x=count,
                y=games,
                marker={
                    'line':{
                        'color': 'rgba(0,0,0,1)',
                    },
                    'color': 'rgba(255,215,1,1)',
                },
            )
        ],
        layout=go.Layout(
            title={
                'text': 'Количество игроков по играм (' + str(period) + ' год)',
                'font': {
                    'size': 20,
                    'color': 'gold'
                },
            },
            font={
                'size': 11,
                'color': 'gold'
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
    )

    total_players_per_game_bar = opy.plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
    return total_players_per_game_bar
