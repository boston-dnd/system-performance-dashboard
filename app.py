import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import plotly.graph_objs as go

#connect to the database and read in the necessary tables
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
inflow = pd.read_sql_query("select * from inflow", con=conn)

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2('System Performance Dashboard - Boston CoC'),
    html.H4('Race'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in inflow.race.unique()],
        value='White'
    ),
    dcc.Graph(id='inflow-graph')
])

@app.callback(dash.dependencies.Output('inflow-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def update_figure(selected_race):
    filtered_df = inflow[inflow.race == selected_race]
    print(filtered_df)
    yearly_inflow = pd.DataFrame(filtered_df.groupby('year')['count'].sum())
    print(yearly_inflow)
    return {
    'data': [go.Bar(x = yearly_inflow.index,
        y= yearly_inflow['count'])],
    'layout': go.Layout(
        title='Yearly Inflow',
        xaxis={'title': 'Year'},
        yaxis={'title': 'Number of clients'},
        hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)