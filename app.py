import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd

#connect to the database and read in the necessary tables
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
inflow = pd.read_sql_query("select * from inflow")

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2('System Performance Dashboard - Boston CoC'),
    html.H4('Race')
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in inflow.race.unique()],
        value='White'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)