import dash
from dash import html, dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import xgboost as xgb
import pandas as pd
import joblib
import shap
import plotly.graph_objects as go
import numpy as np
import requests

dash.register_page(__name__, path='/car-price-prediction', order=4)  # Set the order for the pages

# URL of the pre-trained XGBoost model
# Download the model file with correct extension
md = "https://github.com/oussama-rhiti/AnalyticsApp/raw/main/models/car_price_predictor"
# Load the pre-trained XGBoost model
model = joblib.load(md + ".joblib")

# Sample DataFrame, replace this with your actual data
df = pd.DataFrame({
    'Location': [1],
    'Kilometers_Driven': [72000],
    'Transmission': [0],
    'Mileage': [26.6],
    'Engine': [998.0],
    'Seats': [5],
    'Age': [14],
    'Brand': [0],
    'Fuel_Type': [0],  # Add Fuel_Type to the DataFrame
    'Owner_Type': [0]  # Add Owner_Type to the DataFrame
})

# Mapping dictionary for 'Location' numerical values and their corresponding names
location_mapping = {
    0: 'Mumbai',
    1: 'Hyderabad',
    2: 'Kochi',
    3: 'Coimbatore',
    4: 'Pune',
    5: 'Delhi',
    6: 'Kolkata',
    7: 'Chennai',
    8: 'Jaipur',
    9: 'Bangalore',
    10: 'Ahmedabad'
}

location_options = [
    {'label': name, 'value': value}
    for value, name in location_mapping.items()
]

cols = [
    'Location',
    'Kilometers_Driven',
    'Fuel_Type',
    'Transmission',
    'Owner_Type',  # Add Owner_Type to the list of columns
    'Mileage',
    'Engine',
    'Seats',
    'Age',
    'Brand'
]

options = [
    {'label': c, 'value': c}
    for c in cols
]

Brand_mapping = {
    0: 'Maruti',
    1: 'Hyundai',
    2: 'Honda',
    3: 'Audi',
    4: 'Nissan',
    5: 'Toyota',
    6: 'Volkswagen',
    7: 'Tata',
    8: 'Land',
    9: 'Mitsubishi',
    10: 'Renault',
    11: 'Mercedes-benz',
    12: 'Bmw',
    13: 'Mahindra',
    14: 'Ford',
    15: 'Porsche',
    16: 'Datsun',
    17: 'Jaguar',
    18: 'Volvo',
    19: 'Chevrolet',
    20: 'Skoda',
    21: 'Mini',
    22: 'Fiat',
    23: 'Jeep',
    24: 'Smart',
    25: 'Ambassador',
    26: 'Isuzu',
    27: 'Force',
    28: 'Bentley',
    29: 'Lamborghini'
}

brand_options = [
    {'label': name, 'value': value}
    for value, name in Brand_mapping.items()
]

transmission_mapping = {
    0: 'Manual',
    1: 'Automatic'
}

transmission_options = [
    {'label': name, 'value': value}
    for value, name in transmission_mapping.items()
]

owner_type_mapping = {
    0: 'First',
    1: 'Second',
    2: 'Third',
    3: 'Fourth & Above'
}

owner_type_options = [
    {'label': name, 'value': value}
    for value, name in owner_type_mapping.items()
]

fuel_type_options = [
    {'label': 'CNG', 'value': 0},
    {'label': 'Diesel', 'value': 1},
    {'label': 'Petrol', 'value': 2},
    {'label': 'LPG', 'value': 3},
    {'label': 'Electric', 'value': 4}
]

inputs_dash = html.Div(
    className="row g-3 mb-3",
    children=[
        html.Div([
            html.Label('Location'),
            dcc.Dropdown(
                id='input-location',
                options=location_options,
                value=df['Location'].iloc[0]
            )
        ]),
        html.Div([
            html.Label('Brand'),
            dcc.Dropdown(
                id='input-brand',
                options=brand_options,
                value=df['Brand'].iloc[0]
            )
        ]),
        *[
            html.Div([
                html.Label(col),
                dcc.Input(id=f'input-{col.lower().replace("_", "")}', type='number', value=df[col].iloc[0])
            ]) if col != 'Seats' and col != 'Transmission' else (
                html.Div([
                    html.Label(col),
                    dcc.Slider(
                        id=f'input-{col.lower().replace("_", "")}',
                        min=1,
                        max=10,
                        step=1,
                        value=df[col].iloc[0],
                        marks={i: str(i) for i in range(1, 11)}
                    )]) if col == 'Seats' else
                html.Div([
                    html.Label(col),
                    dcc.Dropdown(
                        id=f'input-{col.lower().replace("_", "")}',
                        options=transmission_options if col == 'Transmission' else [],
                        value=transmission_options[0]['value'] if col == 'Transmission' else None
                    )
                ])
            ) for col in cols if col not in ['Location', 'Brand', 'Fuel_Type', 'Owner_Type']
        ],
        html.Div([
            html.Label('Fuel Type'),
            dcc.Dropdown(
                id='input-fueltype',
                options=fuel_type_options,
                value=fuel_type_options[0]['value'],
                multi=False
            )
        ]),
        html.Div([
            html.Label('Owner Type'),
            dcc.Dropdown(
                id='input-ownertype',
                options=owner_type_options,
                value=owner_type_options[0]['value']
            )
        ]),
    ]
)

layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.H1('Car Price Prediction'),
                html.Div(''),
            ]
        ),
        inputs_dash,
        html.Button('Predict', id='Predict'),
        html.Div(
            id='output-container',
            className="row",
            children=[
                html.Div(id='kpis-output'),
                dcc.Graph(
                    id='shap-waterfall-plot',
                    style={'width': '100%', 'height': '500px'}  # Adjust the style for full-width and fixed height
                )
            ]
        ),
    ]
)

@callback(
    [Output('kpis-output', 'children'),
     Output('shap-waterfall-plot', 'figure')],
    [Input('Predict', 'n_clicks')],
    [
        *[State(f'input-{col.lower().replace("_", "")}', 'value') for col in cols],
        State('input-location', 'value'),
        State('input-fueltype', 'value'),
        State('input-transmission', 'value'),
        State('input-ownertype', 'value'),
        State('input-brand', 'value')
    ]
)
def predict(n_clicks, *args):
    if not n_clicks or n_clicks == 0:
        raise PreventUpdate

    # Use the provided input values for prediction
    data_new = pd.DataFrame({col: [val] for col, val in zip(cols, args[:-5])})
    data_new['Location'] = args[-5]
    data_new['Fuel_Type'] = args[-4]
    data_new['Transmission'] = args[-3]
    data_new['Owner_Type'] = args[-2]
    data_new['Brand'] = args[-1]

    # Perform the prediction using the machine learning model
    prediction = model.predict(data_new)

    # Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data_new)

    # Calculate the base value manually
    base_value = explainer.expected_value

    # Create waterfall plot using Plotly
    features = data_new.columns
    waterfall_trace = go.Waterfall(
        orientation='v',
        measure=['absolute'] + ['relative'] * (len(features) - 2) + ['total'],
        x=features,
        textposition='outside',
        y=[base_value] + list(shap_values.flatten()) + [prediction[0]],
        connector={'line': {'color': 'rgb(63, 63, 63)'}},
        decreasing={'marker': {'color': '#FF0051'}},
        increasing={'marker': {'color': '#008BFB'}},
	text=[f'{val:.2f}' for val in [base_value] + list(shap_values.flatten()) + [prediction[0]]]  # Display values
    )

    waterfall_layout = go.Layout(
        title="SHAP Waterfall Plot",
        showlegend=False
    )

    waterfall_fig = go.Figure(data=[waterfall_trace], layout=waterfall_layout)

    # Display the prediction result and the waterfall plot
    return [
        html.Div(
            f'Predicted Car Purchase amount: {format(prediction[0]* 1000, ".2f")} €',
            style={'color': 'green', 'padding': '10px', 'border': '2px solid green'}
        ),
        waterfall_fig
    ]

if __name__ == '__main__':
    dash.run_server(debug=True)
