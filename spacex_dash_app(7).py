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
launch_Sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': launch_Sites[0], 'value': launch_Sites[0]},
                                        {'label': launch_Sites[1], 'value': launch_Sites[1]},
                                        {'label': launch_Sites[2], 'value': launch_Sites[2]},
                                        {'label': launch_Sites[3], 'value': launch_Sites[3]},
                                        ],
                                    value='ALL',
                                    placeholder="Select a Launch Site",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload,max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )

def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site','class']]

    if entered_site == 'ALL':
        fig = px.pie(filtered_df.groupby('Launch Site', as_index=False).sum(), 
        values='class', 
        names='Launch Site', 
        title='Percentage of Sucessful Launches for all Sites')
        return fig
    else:
        fig = px.pie(filtered_df[filtered_df['Launch Site']==entered_site].groupby('class', as_index=False).count(), 
        values='Launch Site', 
        names='class', 
        title='Total Success Launches for ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )

def get_scat_chart(entered_site,minandmax):
    
    mystring = ''.join(str(e) for e in minandmax)
    filtered_df_2=spacex_df[(spacex_df['Payload Mass (kg)'] >= minandmax[0]) & (spacex_df['Payload Mass (kg)'] <= minandmax[1])]

    if entered_site == 'ALL':        
        fig2 = px.scatter(filtered_df_2, 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category', 
        title='Correlation between Payload and Success for All Sites')
        return fig2
    else:
        fig2 = px.scatter(filtered_df_2[filtered_df_2['Launch Site']==entered_site], 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category', 
        title='Correlation between Payload and Success for ' + entered_site)
        return fig2


# Run the app
if __name__ == '__main__':
    app.run_server()
