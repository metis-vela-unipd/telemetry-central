import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from paho.mqtt.client import Client

from app import app, data, timeouts
from pages import monitor, dashboard
from threading import Timer

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/monitor':
        app.title = "Telemetry Monitor"
        return monitor.layout
    elif pathname == '/dashboard':
        app.title = "Telemetry Dashboard"
        return dashboard.layout
    else:
        return '404'


def on_message(client, userdata, message):
    data[message.topic] = message.payload.decode()
    if message.topic in timeouts:
        timeouts[message.topic].cancel()
    timeouts[message.topic] = Timer(10, reset_data, [message.topic])
    timeouts[message.topic].start()
    print(f'Receive! Topic: {message.topic}; Value: {message.payload.decode()}')


def reset_data(key):
    data[key] = None


if __name__ == '__main__':
    client = Client('monitor')
    client.on_message = on_message
    client.connect('localhost')
    client.subscribe('#')
    client.loop_start()
    app.run_server(host='0.0.0.0')
