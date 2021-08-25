# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label': 'Cape Canaveral Launch Complex', 'value': 'CCAFS LC-40'},
                                    {'label': 'Cape Canaveral Space Launch Complex', 'value': 'CCAFS SLC-40'},
                                    {'label': 'Kennedy Space Center Launch Complex', 'value': 'KSC LC-39A'},
                                    {'label': 'Vanderberg Air Force Base Space Launch Complex', 'value': 'VAFB SLC-4E'},
                                    {'label': 'All', 'value': 'All'}],
                                value='All',
                                placeholder='Select A Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=min_payload),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart",component_property="figure"), Input(component_id="site-dropdown",component_property='value'))
# Add computation to callback function and return graph
def get_graph(value):
    site_list = spacex_df['Launch Site'].unique()
    if value == "All":
        values = []
        names = site_list
        for site in site_list:
            launch_success_list = spacex_df[spacex_df['Launch Site'] == site]
            success_count = launch_success_list[launch_success_list['class'] == 1].shape[0]
            failure_count = launch_success_list[launch_success_list['class'] == 0].shape[0]
            values.append(success_count)
        print(values,names)
        fig = px.pie(values=values, names=names)
    else:
        values = []
        names = ["Success","Failure"]
        launch_success_list = spacex_df[spacex_df['Launch Site'] == value]
        success_count = launch_success_list[launch_success_list['class'] == 1].shape[0]
        failure_count = launch_success_list[launch_success_list['class'] == 0].shape[0]
        values.append(success_count)
        values.append(failure_count)
        fig = px.pie(values=values, names=names)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))
# Add computation to callback function and return graph
def get_graph_2(value):
    site_list = spacex_df['Launch Site'].unique()
    if value == "All":
        fig2 = px.scatter(spacex_df,x="Payload Mass (kg)",y="class",color="Booster Version Category")
    else:
        df = spacex_df[spacex_df['Launch Site'] == value]
        fig2 = px.scatter(df,x="Payload Mass (kg)",y="class",color="Booster Version Category")
        
    return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
