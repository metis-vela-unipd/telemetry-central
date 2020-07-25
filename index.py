import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import monitor, dashboard

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


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
