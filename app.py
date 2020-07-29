import dash

app = dash.Dash('telemetry-webapp', suppress_callback_exceptions=True)
server = app.server
data = {}
