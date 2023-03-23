# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dcc

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
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'}, {'label': 'CCAFS LC-40', 'value': 'CCAFSLC'}, {'label': 'VAFB SLC-4E', 'value': 'VAFB'}, {'label': 'KSC LC-39A', 'value': 'KSC'}, {'label': 'CCAFS SLC-40', 'value': 'CCAFSSLC'},], value='ALL', placeholder="Select a Launch Site here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'}, value=[0, 1000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    #Data frame for all data
    all_data = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
    #Data for location CCAFS LC-40
    df_1 =  spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
    df_1 = df_1['class'].value_counts()
    #Data for location VAFB SLC-4E
    df_2 =  spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
    df_2 = df_2['class'].value_counts()
    #Data for location KSC LC-39A
    df_3 =  spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
    df_3 = df_3['class'].value_counts()
    #Data for location CCAFS SLC-40
    df_4 =  spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
    df_4 = df_4['class'].value_counts()

    if entered_site == 'ALL':
        fig = px.pie(all_data, values='class', 
        names='Launch Site', 
        title='title')
        return fig
    elif entered_site == 'CCAFSLC':
        fig = px.pie(df_1, values=df_1.values, 
        names=df_1.index, 
        title="Total Success Launches for site CCAFS LC-40")
        return fig
    elif entered_site == 'VAFB':
        fig = px.pie(df_2, values=df_2.values, 
        names=df_2.index, 
        title="Total Success Launches for site VAFB SLC-4E")
        return fig
    elif entered_site == 'KSC':
        fig = px.pie(df_3, values=df_3.values, 
        names=df_3.index, 
        title="Total Success Launches for site KSC LC-39A")
        return fig
    elif entered_site == 'CCAFSSLC':
        fig = px.pie(df_4, values=df_4.values, 
        names=df_4.index, 
        title="Total Success Launches for site CCAFS SLC-40")
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))
def get_scat_plot(entered_site, entered_payloads):

    dff = spacex_df[(spacex_df['Payload Mass (kg)']>=entered_payloads[0])&(spacex_df['Payload Mass (kg)']<=entered_payloads[1])]

    if entered_site == 'ALL':
        scatterplot=px.scatter(data_frame=dff,x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return scatterplot
    elif entered_site == 'CCAFSLC':
        dff1 = dff[dff['Launch Site']=='CCAFS LC-40']
        scatterplot=px.scatter(data_frame=dff1,x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return scatterplot
    elif entered_site == 'VAFB':
        dff2 = dff[dff['Launch Site']=='VAFB SLC-4E']
        scatterplot=px.scatter(data_frame=dff2,x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return scatterplot
    elif entered_site == 'KSC':
        dff3 = dff[dff['Launch Site']=='KSC LC-39A']
        scatterplot=px.scatter(data_frame=dff3,x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return scatterplot
    elif entered_site == 'CCAFSSLC':
        dff4 = dff[dff['Launch Site']=='CCAFS SLC-40']
        scatterplot=px.scatter(data_frame=dff4,x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return scatterplot



# Run the app
if __name__ == '__main__':
    app.run_server()