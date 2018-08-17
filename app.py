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
    html.Div(className="app-header", children=[html.Div('System Performance Dashboard - Boston CoC', className="app-header--title")]),
    html.Br(),
    html.Div(children=[
        html.H5('Subpopulation'),
        dcc.Dropdown(
        id='subpopulation-dropdown',
        options=[{'label': 'All', 'value': 'all'}, 
        {'label': 'Veterans', 'value': 'veterans'}, 
        {'label': 'Youth (18-24)', 'value': 'youth'}],
        value='all'
        ),
        html.Br(),
        html.H5('Race'),
        dcc.Dropdown(
        id='race-dropdown',
        options=[{'label': 'All', 'value': 'all'}, 
        {'label': 'White', 'value': 'White'}, 
        {'label': 'Black / African American', 'value': 'BlackAfAmerican'},
        {'label': 'American Indian / Alaska Native', 'value': 'AmIndAKNative'},
        {'label': 'Asian', 'value': 'Asian'},
        {'label': 'Native Hawaiian / Other Pacific Islander', 'value': 'NativeHIOtherPacific'}],
        value='all',
        )
        ]
        ),
    dcc.Graph(id='inflow-graph')
])

@app.callback(dash.dependencies.Output('inflow-graph', 'figure'),
              [dash.dependencies.Input('race-dropdown', 'value'),
              dash.dependencies.Input('subpopulation-dropdown', 'value')
              ])
def update_figure(selected_race, selected_subpopulation):
    print(inflow.veteranstatus.head)
    if selected_race == 'all':
        filtered_df = inflow
    else:
        filtered_df = inflow[inflow.race == selected_race]
    if selected_subpopulation == 'all':
        filtered_df = filtered_df
    else:
        if selected_subpopulation == 'veterans':
            filtered_df = filtered_df[filtered_df.veteranstatus == '1.0']
        else:
            filtered_df = filtered_df[filtered_df.unaccompanied_youth == 'True']


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