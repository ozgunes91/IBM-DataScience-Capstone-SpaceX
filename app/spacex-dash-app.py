# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the app
app = dash.Dash(__name__)

# -------------------------------------------------------------------------
# GÖREV 1: Dropdown input bileşeni
# -------------------------------------------------------------------------
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + \
    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),

    html.Br(),

    # Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites,
                 value='ALL',
                 placeholder="Buradan Bir Lansman Yeri Seçin",
                 searchable=True),

    html.Br(),

    # ---------------------------------------------------------------------
    # GÖREV 2: Pie chart (başarı oranları)
    # ---------------------------------------------------------------------
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # ---------------------------------------------------------------------
    # GÖREV 3: RangeSlider (payload seçimi)
    # ---------------------------------------------------------------------
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000',
                           7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    html.Br(),

    # ---------------------------------------------------------------------
    # GÖREV 4: Scatter chart (payload vs. başarı)
    # ---------------------------------------------------------------------
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# -------------------------------------------------------------------------
# Callback 1 – Pie chart
# -------------------------------------------------------------------------
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success vs. Failure for {selected_site}')
    return fig

# -------------------------------------------------------------------------
# Callback 2 – Scatter chart
# -------------------------------------------------------------------------
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(port=8060)
