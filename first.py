# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from highcharts_core.chart import Chart
from highcharts_stock.options import HighchartsStock

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Function to generate random walk data
def generate_random_walk(n=1000):
    np.random.seed(42)  # For reproducibility
    steps = np.random.choice([-1, 1], size=n)  # Random steps
    walk = np.cumsum(steps)  # Cumulative sum to get the walk
    return walk

# Generate random walk data
data = generate_random_walk()

# Create a DataFrame for the random walk data
df = pd.DataFrame({'Step': range(len(data)), 'Value': data})

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Random Walk Simulation"),
            dcc.Graph(id='random-walk-graph')
        ])
    ])
])

# Define the callback to update the graph
@app.callback(
    Output('random-walk-graph', 'figure'),
    Input('random-walk-graph', 'id')
)
def update_graph(_):
    # Create a Highcharts chart
    chart = Chart()
    chart.add_data_set(df.to_dict(orient='list'), 'line', 'Random Walk')
    chart.set_title('Random Walk Simulation')
    chart.set_x_axis('Step')
    chart.set_y_axis('Value')

    # Convert the Highcharts chart to a plotly figure
    figure = {
        'data': chart.to_dict()['series'],
        'layout': {
            'title': 'Random Walk Simulation',
            'xaxis': {'title': 'Step'},
            'yaxis': {'title': 'Value'}
        }
    }
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
