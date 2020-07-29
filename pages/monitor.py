import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app, data

FOOTER_STYLE = {
    'position': 'absolute',
    'left': '0',
    'bottom': '0',
    'width': '100%',
    'height': '60px'
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
    dcc.Interval(
        id='update-timer',
        interval=500
    )
], style={'height': '100vh'}, className='container-fluid')


@app.callback(Output('gps-speed-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_gps_speed(n):
    return str(round(float(data['sensor/gps0/speed']), 1)) if 'sensor/gps0/speed' in data else '-'


@app.callback(Output('gps-track-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_gps_track(n):
    return str(round(float(data['sensor/gps0/track']), 1)) if 'sensor/gps0/track' in data else '-'


@app.callback(Output('wind-speed-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_wind_speed(n):
    return str(round(float(data['sensor/wind0/speed']), 1)) if 'sensor/wind0/speed' in data else '-'


@app.callback(Output('wind-direction-text', 'children'),
              [Input('update-timer', 'n_intervals')])
def update_wind_direction(n):
    return str(round(float(data['sensor/wind0/direction']))) if 'sensor/wind0/direction' in data else '-'
