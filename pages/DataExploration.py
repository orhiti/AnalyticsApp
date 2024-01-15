import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from phik import phik_matrix

# Assuming you have an app instance defined
dash.register_page(__name__, path='/Analyse', order=3)

# Load data from the CSV file
dataset = "https://github.com/oussama-rhiti/AnalyticsApp/blob/main/data/cleaned-data.csv"
df = pd.read_csv("dataset")

# Mapping for Fuel_Type
fuel_type_mapping = {
    0: 'CNG',
    1: 'Diesel',
    2: 'Petrol',
    3: 'LPG',
    4: 'Electric'
}

# Apply the mapping to the 'Fuel_Type' column
df['Fuel_Type'] = df['Fuel_Type'].map(fuel_type_mapping)

# Create the correlation matrix with phik
corr_matrix = df.drop(['Brand', 'Year', 'Name', 'Model'], axis=1).phik_matrix()

# Calculate the count of each fuel type
fuel_type_counts = df['Fuel_Type'].value_counts()

# Create a bar chart showing the count of each fuel type
fuel_type_count_chart = px.bar(
    x=fuel_type_counts.index,
    y=fuel_type_counts.values,
    title='Count of Cars by Fuel Type',
    labels={'x': 'Fuel Type', 'y': 'Count'}
)

# Display the correlation matrix using Plotly with a smaller size and a gradient of dark blue color scale
correlation_heatmap = go.Figure(data=[
    go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        text=[f'{val:.2f}' for val in corr_matrix.values.flatten()],  # Display values
        colorscale='Blues',  # Change to the Blues color scale
        colorbar={'title': 'Correlation', 'tickvals': [0, 1], 'ticktext': ['Low', 'High']}
    )
], layout={
    'title': 'Correlation Matrix between Variables',
    'xaxis': {'title': 'Features'},
    'yaxis': {'title': 'Features'},
    'margin': {'l': 40, 'b': 40, 't': 40, 'r': 40},
    'hovermode': 'closest',
    'width': 600  # Set the height of the correlation matrix
})

# Create a Pair Plot for selected numerical columns with dark blue color
pair_plot = px.scatter_matrix(df, dimensions=['Kilometers_Driven', 'Fuel_Type', 'Price'],
                              color='Fuel_Type', title='Pair Plot of Selected Variables',
                              color_continuous_scale='Black')

# Define the layout of the app without a black background
layout = html.Div(
    children=[
        html.H1("Analysis Page"),

        # Display the bar chart showing the count of each fuel type
        dcc.Graph(
            id='fuel-type-count-chart',
            figure=fuel_type_count_chart
        ),

        # Add space between the bar chart and the correlation matrix
        html.Br(),

        # Display the correlation matrix
        dcc.Graph(
            id='correlation-heatmap',
            figure=correlation_heatmap
        ),

        # Add space between the correlation matrix and the pair plot
        html.Br(),

        # Display the Pair Plot for selected variables with a dark blue color
        dcc.Graph(
            id='pair-plot',
            figure=pair_plot,
            style={'height': '80vh'}  # Adjust the height of the Pair Plot
        ),
    ])
