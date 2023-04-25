import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd

from mysql_utils import get_top_universities

# Dash constructor (Initialize the app)
app = Dash(__name__)

# App layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("University and Faculty Information")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Form([
                dbc.Label("Keyword:", html_for="keyword-input"),
                dbc.Input(id="keyword-input", type="text", placeholder="Enter keyword"),
                dbc.FormText("Enter a keyword to search for universities and faculty members."),
                dbc.Button("Submit", id="submit-button", color="primary", className="mt-2")
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id="results")
        ])
    ]),
], fluid=True)


@app.callback(
    Output("results", "children"),
    [Input("submit-button", "n_clicks")],
    [dash.dependencies.State("keyword-input", "value")]
)
def display_results(n_clicks, keyword):
    if n_clicks and keyword:
        # Call the get_top_universities function with the given keyword
        df = get_top_universities(keyword)

        # Check if the DataFrame is not empty
        if not df.empty:
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        else:
            return "No results to display."
    else:
        return "No results to display."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)