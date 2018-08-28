import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import plotly.graph_objs as go
import numpy as np

#connect to the database and read in the necessary tables
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
inflow = pd.read_sql_query("select * from inflow", con=conn)
los = pd.read_sql_query("select * from los", con=conn)
phexits = pd.read_sql_query("select * from phexits", con=conn)

def filter_data(dataframe, selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household):
	'''function that filters data based on inputs'''

	filtered_df = dataframe
	if selected_race == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.race == selected_race]

	if selected_ethnicity == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.ethnicity == selected_ethnicity]

	if selected_gender == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.gender == selected_gender]

	if selected_veteran == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.veteranstatus == selected_veteran]

	if selected_household == 'all':
		filtered_df = filtered_df
	else:
		filtered_df = filtered_df[filtered_df.householdtype == selected_household]
	return filtered_df


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
	html.Div(className="app-header", children=[html.Div('System Exploration App - Boston CoC', className="app-header--title")], style={"margin-left": "10px", "margin-right": "10px"}),
	html.P("""The goal of this web app is to allow and empower the Supportive Housing Divison to explore and ask questions of the HMIS data. The app provides answers to broad system performance questions like "is the average length of stay decreasing?" but also allows users to dig deeper and uncover insights from the data, like "White veterans have shorter lengths of stay than veterans of color." The baseline measures displayed in the app are an adaption/expansion of HUD's System Performance Measures. The Supportive Housing Division collaborated to workshop and tailor these measures to be more relevant to the goals of our CoC.""", style={"margin-left": "10px", "margin-right": "10px"}),
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
					value='all')], className="four columns"
				)], className = "row", style={'margin-left':'50px', 'margin-right':'100px'})
		]),
	html.Br(),
	html.Br(),
	html.H4("Inflow / First time Homeless", style={'font-weight': 'bold', 'margin-left':'50px'}),
	html.Hr(style={'font-weight': 'bold', 'margin-left':'50px', 'color':'#d2d2d2'}),
	html.Div([
		html.Div([
			html.H6("What am I looking at?"),
			html.P("In a given year, how many clients experienced their first-ever overnight stay in a Boston CoC shelter or on the street?")
			], className="three columns"),
		html.Div([
			html.H6("Context:"),
			html.P("This metric gives a sense of how many new clients per year the CoC is serving, which can provide context for the overall census")
			], className="three columns"),
		], className="row", style={'margin-left':'50px', 'margin-right':'100px'}),

	dcc.Graph(id='inflow-graph', style={'margin-left':'80px', 'margin-right':'80px'}),
	html.H4("Length of Stay", style={'font-weight': 'bold', 'margin-left':'50px'}),
	html.Hr(style={'font-weight': 'bold', 'margin-left':'50px', 'color':'#d2d2d2'}),
	html.Div([
		html.Div([
			html.H6("What am I looking at?"),
			html.P("In a given year, how long on average have clients who appeared in a Boston CoC shelter / on the street that year spent cumulatively in a Boston CoC shelter or on the street?")
			], className="three columns"),
		html.Div([
			html.H6("Context:"),
			html.P("This metric gives a sense of how long individuals in the current CoC population have been experiencing homelessness in the CoC. This metric can shed light on whether the CoC's efforts to house its longest-term stayers have been successful.")
			], className="three columns"),
		], className="row", style={'margin-left':'50px', 'margin-right':'100px'}),
	dcc.Graph(id='los-graph', style={'margin-left':'80px', 'margin-right':'80px'}),
	html.H4("Exits to Permanent Housing", style={'font-weight': 'bold', 'margin-left':'50px'}),
	html.Hr(style={'font-weight': 'bold', 'margin-left':'50px', 'color':'#d2d2d2'}),
	html.Div([
		html.Div([
			html.H6("What am I looking at?"),
			html.P("In a given year, how many clients exited to a permanent housing destination?")
			], className="three columns"),
		html.Div([
			html.H6("Context:"),
			html.P("This metric gives a sense of how many clients per year the CoC is helping exit to a permanent housing destination, which can provide insight on whether the CoC is achieving its goal of increasing exits to permanent housing")
			], className="three columns"),
		], className="row", style={'margin-left':'50px', 'margin-right':'100px'}),
	dcc.Graph(id='ph-graph', style={'margin-left':'80px', 'margin-right':'80px'})
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
	#call function to filter data
	filtered_df = filter_data(inflow, selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household)

	#agreggate table into reporting format
	yearly_inflow = pd.DataFrame(filtered_df.groupby('year')['count'].sum())

	#dynamically render figure
	return {
	'data': [go.Scatter(x = yearly_inflow.index,
		y= yearly_inflow['count'],
		mode="lines+markers",
		marker=dict(
			size=15,
			color='rgba(78,145,221, .9)',
			line=dict(
				color='rgba(0, 0, 0, .9)',
				width = 2,
            )
            )
		)
	],
	'layout': go.Layout(
		xaxis={'title': 'Year'},
		yaxis={'title': 'Number of clients'},
		hovermode='closest',
		margin=dict(t=0)
		)
	}

'''callback for Length of Stay'''
@app.callback(dash.dependencies.Output('los-graph', 'figure'),
			  [dash.dependencies.Input('race-dropdown', 'value'),
			  dash.dependencies.Input('ethnicity-dropdown', 'value'),
			  dash.dependencies.Input('gender-dropdown', 'value'),
			  dash.dependencies.Input('veteran-dropdown', 'value'),
			  dash.dependencies.Input('household-dropdown', 'value')
			  ])
def update_figure(selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household):
	#call function to filter data
	filtered_df = filter_data(los, selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household)

	grouped_df = filtered_df.groupby('year')

	def compute_los(grp):
		grp['weighted_los'] = np.average(grp['avglos'], weights = grp['numclients'])
		return grp

	grouped_df = grouped_df.apply(compute_los)

	yearly_los = grouped_df
	print(yearly_los)

	#dynamically render figure
	return {
	'data': [go.Bar(x = yearly_los['year'],
		y= yearly_los['weighted_los'],
		marker=dict(
                color='rgba(78,145,221, .9)',
                line=dict(
                    width=1.5),
            )
		)],
	'layout': go.Layout(
		xaxis={'title': 'Year'},
		yaxis={'title': 'Average Length of Stay'},
		hovermode='closest',
		margin=dict(t=0)
		)
	}


'''callback for PH exits'''
@app.callback(dash.dependencies.Output('ph-graph', 'figure'),
			  [dash.dependencies.Input('race-dropdown', 'value'),
			  dash.dependencies.Input('ethnicity-dropdown', 'value'),
			  dash.dependencies.Input('gender-dropdown', 'value'),
			  dash.dependencies.Input('veteran-dropdown', 'value'),
			  dash.dependencies.Input('household-dropdown', 'value')
			  ])
def update_figure(selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household):
	#call function to filter data
	filtered_df = filter_data(phexits, selected_race, selected_ethnicity, selected_gender, selected_veteran, selected_household)

	#agreggate table into reporting format
	yearly_ph = pd.DataFrame(filtered_df.groupby('year')['count'].sum())

	#dynamically render figure
	return {
	'data': [go.Bar(x = yearly_ph.index,
		y= yearly_ph['count'],
		marker=dict(
                color='rgba(78,145,221, .9)',
                line=dict(
                    width=1.5),
            ))],
	'layout': go.Layout(
		xaxis={'title': 'Year'},
		yaxis={'title': 'Number of clients'},
		hovermode='closest',
		margin=dict(t=0)
		)
	}

if __name__ == '__main__':
	app.run_server(debug=True)