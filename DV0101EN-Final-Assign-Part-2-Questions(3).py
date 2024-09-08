import pandas as pd
import dash
from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt

# Load the data using pandas
data = pd.read_csv('df_final_1980_2013.csv')

# List of years 
year_list = [i for i in range(1980, 2014, 1)]

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1('Automobile Statistics Dashboard 1980 - 2013',
                style={'textAlign': 'center', 'color': '#503D36','font-size': 24}),
        
        html.Div([html.Label('Select Statistics'),
                  dcc.Dropdown(id='dropdown-statistics',
                               options=[{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                                        {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
                               placeholder='Select a Report',
                               style= {'width': '80%',
                                       'padding': '3px',
                                       'font-size': 20,
                                       'text-Align': 'center'})]),
        
        html.Div([html.Label('Select Year'),
                  dcc.Dropdown(id='select-year',
                               options=[{'label': i, 'value': i} for i in year_list],
                               placeholder='---',
                               style= {'width': '80%',
                                       'padding': '3px',
                                       'font-size': 20,
                                       'text-Align': 'center'})]),
        html.Div(id='output-container',
                 className='chart-grid',
                 style= {'display': 'flex'}),
    ]
) #End of the layout components

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return True
    else: 
        return False
    
#Callback for plotting
# Define callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
  
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_data=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_data, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))         

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        
        # use groupby to create relevant data for plotting
        #Hint:Use Vehicle_Type and Automobile_Sales columns
        average_sales = recession_data.groupby('Verhicle_Type')                 
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Verhicle_Type',
            y='Automobile_Sales',
            title="AVG Number of Verhicles Type Sold During Recession"))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # grouping data for plotting
	# Hint:Use Vehicle_Type and Advertising_Expenditure columns
        exp_data= recession_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_data,
            values='Advertising_Expenditure',
            names='Verhicle_Type',
            title="Adverticement Expenditure per Verhicle Type During Recession"
                    )
        )

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        #grouping data for plotting
	# Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
        unemp_data = recession_data.groupby('Verhicle_Type')
        R_chart4 = dcc.Graph(figure=px.bar(unemployment_rate,
        x='Verhicle_Type',
        y='Automobile_Sales',
        labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
        title='Effect of Unemployment Rate on Vehicle Type and Sales'))
    
    return [
        html.Div(
            className='chart-item', 
                 children=[
                     html.Div(children=R_chart1),
                     html.Div(children=R_chart2)],
                 style={}),
        html.Div(
            className='chart-item',
            children=[
                html.Div(children=R_chart3),
                html.Div(children=R_chart4)],
            style={'display': 'flex'})
    ]
# Yearly Statistic Report Plots                             
elif (input_year and selected_statistics=='Yearly Statistics') :
    print(input_year)
    yearly_data = data[data['Year'] == input_year]
                                                 
#plot 1 Yearly Automobile sales using line chart for the whole period.
yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(figure=px.line(yas, 
        x = 'Year',
        y = 'Automobile_Sales',
        title = 'Average automobiles sales over time'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
yearly_data = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
    Y_chart2 = dcc.Graph(figure=px.line(
        yearly_data,
        x = 'Month',
        y = 'Automobile_Sales',
        title= 'Total automobile sales per month in the year {}'.format(input_year)))

# Plot bar chart for average number of vehicles sold during the given year
avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
        x = 'Vehicle_Type',
        y = 'Automobile_Sales',
        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

# Total Advertisement Expenditure for each vehicle using pie chart
exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    Y_chart4 = dcc.Graph(figure=px.pie(
        exp_data,
        Values='Advertising_Expenditure',
        Names = 'Vehicle_Type',
        title = 'Advertising Expenditure per Vehicle Type in the year {}'.format(inpute_year)))

#TASK 2.6: Returning the graphs for displaying Yearly data
return [
        html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=Y_chart1),
                    html.Div(children=Y_chart2)],
                style={'display':'flex'}),
            html.Div(
                className='chart-item', 
                children=[
                    html.Div(children=Y_chart3),
                    html.Div(children=Y_chart4)],
                style={'display': 'flex'})
                ]
        

# Run the Dash app

if __name__ == '__main__':
    app.run_server(debug=True)