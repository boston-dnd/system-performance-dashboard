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
	html.Div(className="app-header", children=[html.Div('System Exploration App - Boston CoC', className="app-header--title")]),
	html.Br(),
	html.Div([
		html.Div([
		html.Div([
		html.H5('Race'),
		dcc.Dropdown(
		id='race-dropdown',
		options=[{'label': 'All', 'value': 'all'}, 
		{'label': 'White', 'value': 'White'}, 
		{'label': 'Black / African American', 'value': 'BlackAfAmerican'},
		{'label': 'American Indian / Alaska Native', 'value': 'AmIndAKNative'},
		{'label': 'Asian', 'value': 'Asian'},
		{'label': 'Native Hawaiian / Other Pacific Islander', 'value': 'NativeHIOtherPacific'}],
		value='all'),
		html.Br(),
		html.H5('Veteran Status'),
		dcc.Dropdown(
		id='veteran-dropdown',
		options=[{'label': 'All', 'value': 'all'}, 
		{'label': 'Veterans', 'value': '1.0'}, 
		{'label': 'Non-Veterans', 'value': '0.0'}],
		value='all'
		)], className="four columns"),

		html.Div([
		html.H5('Ethnicity'),
		dcc.Dropdown(
		id='ethnicity-dropdown',
		options=[{'label': 'All', 'value': 'all'}, 
		{'label': 'Hispanic / Latinx', 'value': '1.0'}, 
		{'label': 'Not Hispanic / Latinx', 'value': '0.0'}],
		value='all'),
		html.Br(),
		html.H5('Household Status'),
		dcc.Dropdown(
		id='household-dropdown',
		options=[{'label': 'All', 'value': 'all'}, 
		{'label': 'Individual Adults (25+)', 'value': 'individual adult (25+)'}, 
		{'label': 'Unaccompanied Youth (18-24)', 'value': 'unaccompanied youth'},
		{'label': 'Families', 'value': 'family member'}],
		value='all')], className="four columns"),

		html.Div([
		html.H5('Gender'),
		dcc.Dropdown(
		id='gender-dropdown',
		options=[{'label': 'All', 'value': 'all'}, 
		{'label': 'Male', 'value': '1.0'}, 
		{'label': 'Female', 'value': '0.0'},
		{'label': 'Trans Female', 'value': '2.0'},
		{'label': 'Trans Male', 'value': '3.0'},
		{'label': 'Gender Non-Conforming', 'value': '4.0'}],
		value='all',
		)], className="four columns"),
		], className = "row")
	]),
	dcc.Graph(id='inflow-graph')
])

'''callback for inflow'''
@app.callback(dash.dependencies.Output('inflow-graph', 'figure'),
			  [dash.dependencies.Input('race-dropdown', 'value'),
			  dash.dependencies.Input('ethnicity-dropdown', 'value'),
			  dash.dependencies.Input('gender-dropdown', 'value'),
			  dash.dependencies.Input('veteran-dropdown', 'value'),
			  dash.dependencies.Input('household-dropdown', 'value')
			  ])
def update_figure(selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household):
	filtered_df = inflow
	print(inflow.head)
	#filter race
	if selected_race == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.race == selected_race]

	#filter ethnicity
	if selected_ethnicity == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.ethnicity == selected_ethnicity]

	#filter gender
	if selected_gender == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.gender == selected_gender]

	#filter veteran
	if selected_veteran == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.veteranstatus == selected_veteran]

	#select household
	if selected_household == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.householdtype == selected_household]

	yearly_inflow = pd.DataFrame(filtered_df.groupby('year')['count'].sum())

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