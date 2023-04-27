import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd

from mysql_utils import get_coauthored_count

# Dash constructor (Initialize the app)
app = Dash(__name__)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Faculty Name"),
            dbc.Input(id="faculty-name-input", type="text", placeholder="Enter faculty name"),
        ]),
        dbc.Col([
            dbc.Label("University Name"),
            dbc.Input(id="university-name-input", type="text", placeholder="Enter university name"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Start Year"),
            dbc.Input(id="start-year-input", type="number", placeholder="Enter start year", value=0),
        ]),
        dbc.Col([
            dbc.Label("End Year"),
            dbc.Input(id="end-year-input", type="number", placeholder="Enter end year", value=2023),
        ]),
    ]),
    dbc.Button("Submit", id="submit-button", color="primary"),
    html.Hr(),
    html.Div(id="results"),
])


@app.callback(
    Output("results", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("faculty-name-input", "value"),
        State("university-name-input", "value"),
        State("start-year-input", "value"),
        State("end-year-input", "value"),
    ]
)
def display_results(n_clicks, faculty_name, university_name, start_year, end_year):
    if n_clicks and faculty_name and university_name:
        if start_year is None:
            start_year = 0
        if end_year is None:
            end_year = 2023

        coauthored_count = get_coauthored_count(faculty_name, university_name, start_year, end_year)

        if coauthored_count:
            faculty, count = coauthored_count[0]['name'], coauthored_count[0]['coauthored_papers']
            return f"{faculty} co-authored {count} papers from {start_year} to {end_year}."
        else:
            return "No results to display."
    else:
        return "Please enter all required information."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)