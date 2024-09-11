import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the combined DataFrame
df = pd.read_csv('ate-bad-dates.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Prepare data by type
def prepare_data(df, type_label):
    # Filter DataFrame by the specified type
    df_filtered = df[df['Type'] == type_label]
    # Create pivot table
    pivot_df = df_filtered.pivot_table(
        values='Normalized_ATE', index='Duration', columns='Feature', aggfunc='sum')
    # Sort the pivot_df by the Duration index in ascending order
    pivot_df = pivot_df.sort_index(ascending=True)
    # Filter out columns where all values are zero
    pivot_df = pivot_df.loc[:, (pivot_df != 0).any(axis=0)]
    # Sort columns by the total sum of Normalized_ATE values across all durations
    pivot_df = pivot_df.reindex(pivot_df.sum().sort_values(ascending=False).index, axis=1)
    return pivot_df

# Create Plotly Express graphs for each type
def create_figure(data, title):
    fig = px.area(data, title=title)
    fig.update_layout(
        title={'text': title, 'font': {'size': 22}},
        xaxis_title={'text': 'Time of Heater Profile (seconds)', 'font': {'size': 18}},
        yaxis_title={'text': 'Normalized ATE', 'font': {'size': 18}},
        legend={'font': {'size': 15}},
        xaxis={'tickfont': {'size': 14}},
        yaxis={'tickfont': {'size': 14}}
    )
    return fig

# Define the types to include in the dashboard
types = ['IBS_R', 'IBS_N', 'IBS_T', 'OBS_R', 'OBS_N', 'OBS_T']

# Define a function to map types to more descriptive titles
def get_custom_title(type_label):
    if 'IBS' in type_label:
        label_type = 'IBS'
    else:
        label_type = 'OBS'
    
    if '_R' in type_label:
        direction = 'R direction'
    elif '_N' in type_label:
        direction = 'N direction'
    else:
        direction = 'T direction'
    
    return f'{label_type} along {direction}'

# Create figures with custom titles
figures = [create_figure(prepare_data(df, type_label), 
                         f'Normalized Average Treatment Effect of Heater Profiles for : {get_custom_title(type_label)} on Perihelion Dates') 
                         for type_label in types]

# Define the layout of the app to include a graph for each type
app.layout = html.Div([dcc.Graph(figure=fig) for fig in figures])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, port=8071)
