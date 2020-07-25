import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

FOOTER_STYLE = {
    'position': 'absolute',
    'left': '0',
    'bottom': '0',
    'width': '100%',
    'height': '60px'
}

speed_text = html.H1('15', style={
    'fontSize': '300px',
    'marginTop': '-40px',
    'marginBottom': '-40px',
    'textAlign': 'right'
})

knots_text = html.H1('kt', style={'fontSize': '150px'})

heading_text = html.H1('356', style={
    'fontSize': '300px',
    'marginTop': '-60px',
    'marginBottom': '-40px',
    'textAlign': 'right'
})

degrees_text = html.H1('°', style={
    'fontSize': '300px',
    'marginTop': '-60px',
    'marginBottom': '-40px',
    'marginLeft': '-10px'
})

layout = html.Div([
    dbc.Row([dbc.Col(speed_text, width=10), dbc.Col(knots_text, width=2)]),
    dbc.Row([dbc.Col(heading_text, width=10), dbc.Col(degrees_text, width=2)]),
    html.Footer([], style=FOOTER_STYLE, className='border-top')
], style={'height': '100vh'}, className='container-fluid')
