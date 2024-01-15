
import dash
from dash import dcc, html,callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from .templates.kpi import generate_kpi

dash.register_page(__name__, path='/',order=1)
# Charger les données (remplacez cette ligne par le chargement de vos propres données)
dataset = "https://github.com/oussama-rhiti/AnalyticsApp/blob/main/data/cleaned-data.csv"
df = pd.read_csv(dataset)
date_time = datetime.datetime.now()
df['Age']=date_time.year - df['Year'] #subtruct this year from the year of data to get the age and save it in a new column call it Age

avg_price = (df['Price'].mean())*1000
min_price = (df['Price'].min())*1000
max_price = (df['Price'].max())*1000
most_common_category = df['Name'].mode().iloc[0]

# Filtrer les colonnes numériques et catégorielles
colonnes_numeriques = df.select_dtypes(include='number').columns
colonnes_categorielles = df.select_dtypes(exclude='number').columns
seuil_modalites = 8

# Mise en page du tableau de bord
layout = html.Div([
    # KPIs
    html.H1("Dashbord with Dash"),
    html.Div([
        generate_kpi("Average price of cars", f'{avg_price:.2f} €'),
        generate_kpi("Minimum price", f'{min_price:.2f} €'),
        generate_kpi("Maximum price", f'{max_price:.2f} €'),
        generate_kpi("The most prominent category", most_common_category),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),

    # Menu déroulant pour sélectionner la colonne
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=colonnes_numeriques[0],  # Colonne numérique par défaut
        style={'width': '50%'}
    ),

    # Graphique (histogram or pie chart)
    dcc.Graph(
        id='chart'
    ),
])

# Callback pour mettre à jour le graphique et les indicateurs en fonction de la colonne sélectionnée
@callback(
    [Output('chart','figure')],
    [Input('column-selector', 'value')]
)
def update_chart(selected_column):
    if selected_column in colonnes_numeriques:
        # Créer un histogramme interactif avec Plotly Express pour les variables numériques
        fig = px.histogram(df, x=selected_column, nbins=40,
                           title=f'Histogram of {selected_column}',
                           labels={selected_column: f'{selected_column}'},
                           opacity=0.7)
    elif selected_column in colonnes_categorielles:
        # Compter les effectifs pour chaque catégorie
        counts = df[selected_column].value_counts()

       # Sélectionner les 6 principales catégories
        top_categories = counts.head(seuil_modalites)

       # Regrouper le reste des catégories sous la catégorie "Autres"
        df[selected_column] = df[selected_column].apply(lambda x: x if x in top_categories.index else 'Autres')

        # Créer le pie chart
        fig = go.Figure(data=[go.Pie(labels=df[selected_column].value_counts().index,
                                 values=df[selected_column].value_counts().values,
                                 title=f'Pie Chart of {selected_column}')])

     # Mettre à jour la mise en page
    fig.update_layout(
        xaxis_title=f'{selected_column}',
        yaxis_title='Count' if selected_column in colonnes_numeriques else 'Percentage',
        showlegend=True
    )
    return [fig]
