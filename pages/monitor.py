import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

from app import app, data

FOOTER_STYLE = {
    'position': 'absolute',
    'left': '0',
    'bottom': '0',
    'width': '100%',
    'height': '150px'
}

gps_speed_text = html.H1('-', style={
    'fontSize': '200px',
    'marginTop': '-40px',
    'marginBottom': '-20px',
    'textAlign': 'right'
}, id='gps-speed-text')

gps_track_text = html.H1('-', style={
    'fontSize': '200px',
    'marginTop': '-40px',
    'marginBottom': '-20px',
    'textAlign': 'right'
}, id='gps-track-text')

wind_speed_text = html.H1('-', style={
    'fontSize': '200px',
    'marginTop': '-40px',
    'marginBottom': '-20px',
    'textAlign': 'right'
}, id='wind-speed-text')

wind_direction_text = html.H1('-', style={
    'fontSize': '200px',
    'marginTop': '-40px',
    'marginBottom': '-20px',
    'textAlign': 'right'
}, id='wind-direction-text')

degrees_text = html.H1('°', style={
    'fontSize': '200px',
    'marginTop': '-40px',
    'marginBottom': '-20px',
    'marginLeft': '-10px'
})

knots_text = html.H1('kt', style={'fontSize': '100px'})

layout = html.Div([
    dbc.Row(dbc.Col(html.H2("BOAT", className='text-center text-bold'))),
    dbc.Row([dbc.Col(gps_speed_text, width=10), dbc.Col(knots_text, width=2)]),
    dbc.Row([dbc.Col(gps_track_text, width=10), dbc.Col(degrees_text, width=2)]),
    dbc.Row(dbc.Col(html.H2("WIND", className='text-center text-bold'))),
    dbc.Row([dbc.Col(wind_speed_text, width=10), dbc.Col(knots_text, width=2)]),
    dbc.Row([dbc.Col(wind_direction_text, width=10), dbc.Col(degrees_text, width=2)]),
    html.Div(
        html.H1('', className='text-center', style={'fontSize': '113px'}, id='clock-text'),
        style=FOOTER_STYLE,
        className='border-top'),
    dcc.Interval(
        id='update-timer',
        interval=500
    )
], style={'height': '100vh'}, className='container-fluid')


@app.callback(Output('gps-speed-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_gps_speed(n):
    topic = 'sensor/gps0/speed'
    return str(round(float(data[topic]), 1)) if topic in data and data[topic] is not None else '-'


@app.callback(Output('gps-track-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_gps_track(n):
    topic = 'sensor/gps0/track'
    return str(round(float(data[topic]), 1)) if topic in data and data[topic] is not None else '-'


@app.callback(Output('wind-speed-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_wind_speed(n):
    topic = 'sensor/wind0/speed'
    return str(round(float(data[topic]), 1)) if topic in data and data[topic] is not None else '-'


@app.callback(Output('wind-direction-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_wind_direction(n):
    topic = 'sensor/wind0/direction'
    return str(round(float(data[topic]))) if topic in data and data[topic] is not None else '-'


@app.callback(Output('clock-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_clock(n):
    return datetime.now().strftime("%H:%M:%S")
