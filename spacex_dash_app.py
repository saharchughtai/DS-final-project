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
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                    options=[
                                                        {'label': 'ALL', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}

                                                            ],
                                                    value="ALL",placeholder='Select a Launch Site here',
                                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,
                                                step=1000,value=[min_payload,max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def generate_chart(sites):
                                if sites =='ALL':
                                    filtered_df= spacex_df[['Launch Site','class']]
                                    dff=filtered_df.groupby(['Launch Site', 'class']).size().reset_index()
                                    dff=dff.rename(columns={0:'count'})
                                    piechart=px.pie(dff,names="Launch Site",values='count')
                                    return piechart
                                else:
                                    filtered_df= spacex_df[['Launch Site','class']]
                                    filtered_df= filtered_df[filtered_df['Launch Site'] == sites]
                                    dff=filtered_df.groupby(['Launch Site', 'class']).size().reset_index()
                                    dff=dff.rename(columns={0:'count'})
                                    piechart = px.pie(dff,values='count',names='class' )
                                    return piechart
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(site,payload):
                               
 
                                #print(payload)
                                #filtered_df1= pd.DataFrame(value2,columns="payload_mass")
                                #filtered_df1.groupby('payload_mass','Class')
                                if site == 'ALL':
                                    filtered_df1=spacex_df[['Launch Site','class','Payload Mass (kg)','Booster Version Category']]
                                    #dff3=filtered_df1[filtered_df1["Payload Mass (kg)"].isin(payload)]
                                    dff3=filtered_df1[filtered_df1["Payload Mass (kg)"]>=payload[0]]
                                    dff3=dff3[dff3["Payload Mass (kg)"]<=payload[1]]
                                    dff3=dff3.groupby(["Launch Site",'Payload Mass (kg)', 'class','Booster Version Category']).size().reset_index()
                                    dff3=dff3.rename(columns={0:'count'})
                                    scatterchart = px.scatter(dff3,x='Payload Mass (kg)',y='count',color="Booster Version Category" )
                                else:
                                    filtered_df1=spacex_df[['Launch Site','class','Payload Mass (kg)','Booster Version Category']]
                                    filtered_df1= filtered_df1[filtered_df1['Launch Site'] == 'CCAFS LC-40']
                                    #dff1=filtered_df1[filtered_df1["Payload Mass (kg)"].isin(payload)]
                                    dff1=filtered_df1[filtered_df1["Payload Mass (kg)"]>=payload[0]]
                                    dff1=dff1[dff1["Payload Mass (kg)"]<=payload[1]]
                                    dff2=dff1.groupby(['Payload Mass (kg)', 'class','Booster Version Category']).size().reset_index()
                                    dff2=dff2.rename(columns={0:'count'})
                                    scatterchart = px.scatter(dff2,x='Payload Mass (kg)',y='count',color="Booster Version Category" )

                                    #scatterchart = px.pie(filtered_df,x='Payload Mass (kg)',y='class',color="Booster Version Category" )
                                return scatterchart  

# Run the app
if __name__ == '__main__':
    app.run_server()
