import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

# Charger les données (remplacez cette ligne par le chargement de vos propres données)
from .templates.kpi import generate_kpi

dash.register_page(__name__, path='/home2')
dataset = "https://raw.githubusercontent.com/oussama-rhiti/AnalyticsApp/main/data/cleaned-data.csv"
df = pd.read_csv(dataset, delimiter=',', encoding="latin")


df = pd.read_csv(dataset)
brand_model_counts = df.groupby(['Brand', 'Model']).size().reset_index(name='Count')
city_coordinates = {
    'Mumbai': (19.0760, 72.8777),
    'Hyderabad': (17.3850, 78.4867),
    'Kochi': (9.9312, 76.2673),
    'Coimbatore': (11.0168, 76.9558),
    'Pune': (18.5204, 73.8567),
    'Delhi': (28.6139, 77.2090),
    'Kolkata': (22.5726, 88.3639),
    'Chennai': (13.0827, 80.2707),
    'Jaipur': (26.9124, 75.7873),
    'Bangalore': (12.9716, 77.5946),
    'Ahmedabad': (23.0225, 72.5714),
}

# Charger GeoJSON pour les villes indiennes
with urlopen('https://gist.githubusercontent.com/rupinder-developer/9cf97efbbd9651eef88729fb390485c1/raw/d1f9b712521271747d26c6524e93afbe2a8562df/indian-cities.geojson') as response:
    indian_cities_geojson = json.load(response)

# Create a DataFrame with city coordinates
city_df = pd.DataFrame(list(city_coordinates.items()), columns=['Location', 'Coordinates'])
# Split the Coordinates column into Latitude and Longitude
city_df[['Latitude', 'Longitude']] = pd.DataFrame(city_df['Coordinates'].tolist(), index=city_df.index)

# Mise en page principale du tableau de bord
layout = html.Div([
    # Quadrant supérieur gauche
    html.Div([
        html.H3("Choropleth Map"),
        dcc.Graph(id='choropleth-map', style={'border': '2px solid black', 'border-radius': '10px', 'backgroundColor': '#f0f0f0'}),
    ], style={'width': '48%', 'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),

    # Quadrant supérieur droit
    html.Div([
        html.H3("Boxplot"),
        dcc.Graph(id='boxplot', style={'border': '2px solid black', 'border-radius': '10px', 'backgroundColor': '#f0f0f0'}),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),

    # Quadrant inférieur gauche
    html.Div([
        html.H3("Bar Chart"),
        dcc.Graph(id='bar_chat', style={'border': '2px solid black', 'border-radius': '10px', 'backgroundColor': '#f0f0f0'}),
    ], style={'width': '48%', 'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),

    # Quadrant inférieur droit
    html.Div([
        html.H3("Treemap"),
        dcc.Graph(id='graph4', style={'border': '2px solid black', 'border-radius': '10px', 'backgroundColor': '#f0f0f0'}),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
], style={'width': '80%', 'margin': 'auto', 'justify-content': 'center', 'align-items': 'center', 'overflowX': 'scroll'})

# Callback pour mettre à jour les graphiques en fonction des données
@callback(
    [Output('choropleth-map', 'figure'),
     Output('boxplot', 'figure'),
     Output('bar_chat', 'figure'),
     Output('graph4', 'figure')],
    [Input('choropleth-map', 'id')]
)
def update_choropleth_map(value):
    # Créer le choropleth map avec Plotly Express
    choropleth_fig = px.scatter_geo(city_df,
                                    lat='Latitude',
                                    lon='Longitude',
                                    text='Location',
                                    title='Number of Cars by Location',
                                    size=df['Location'].value_counts().values,
                                    color=df['Location'].value_counts().values,
                                    color_continuous_scale='Viridis',  # Change the color scale
                                    projection='natural earth')

    # Set initial zoom to India
    choropleth_fig.update_geos(center=dict(lon=78, lat=22),  # Center coordinates for India
                                projection_scale=3.5)  # Adjust the scale as needed

    # Adjusting the update_geos for scatter_geo
    choropleth_fig.update_geos(
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="Azure",
        showcountries=True, countrycolor="darkgray"
    )

    # Créer le boxplot avec Plotly Express
    boxplot_fig = px.box(df, x='Brand', y='Price', color='Fuel_Type',
                         title='Boxplot of Price by FuelType')
    boxplot_fig.update_yaxes(range=[0, 50])

    bar_chat = px.bar(df, x="Age", y="Kilometers_Driven", color="Age", title="Long-Form Input")

    graph4 = px.treemap(brand_model_counts, path=['Brand', 'Model'], values='Count',
                        title='Car Model Distribution by Brand', color_discrete_sequence=px.colors.qualitative.Pastel1)

    # Redimensionner les plots
    choropleth_fig.update_layout(height=400, width=600)
    boxplot_fig.update_layout(height=400, width=600)
    graph4.update_layout(height=400, width=600)
    bar_chat.update_layout(height=400, width=600)
    # Mettre à jour la présentation du layout

    choropleth_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return choropleth_fig, boxplot_fig, bar_chat, graph4

