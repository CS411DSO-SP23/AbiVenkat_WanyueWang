import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

from mysql_utils import get_top_universities, get_coauthored_count
from neo4j_utils import find_faculty_connections

cyto.load_extra_layouts()

# Dash constructor (Initialize the app)
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# App layout
app.layout = dbc.Container([
    html.Link(rel='stylesheet', href='/assets/style.css'),
    html.H1("FacultyFinder+"),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            # Widget 1: Top Universities and Faculty Members
            html.Div([
                html.H2("Discover Leading Institutions and Experts Based on Your Interest"),
                dbc.Row([
                    dbc.Col([
                        dbc.Form([
                            dbc.Label("Keyword:", html_for="keyword-input"),
                            dbc.Input(id="keyword-input", type="text", placeholder="Enter keyword"),
                            dbc.FormText("Enter a keyword to search for universities and faculty members."),
                            dbc.Button("Submit", id="submit-button-widget1", color="primary", className="mt-2")
                        ])
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div(id="results-widget1")
                    ])
                ]),
            ], className="widget", style={"height": "600px"}),

        ], width=6),


        dbc.Col([
            # Widget 2: Co-authored Papers
            html.Div([
                html.H2("Uncover Collaboration Potential Based on Co-Authorship History"),
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
                dbc.Button("Submit", id="submit-button-widget2", color="primary"),
                html.Div(id="results-widget2"),
            ], className="widget", style={"height": "600px"})
        ], width=6)
    ]),

    # TODO: Add the layout of widgets 3-5 here

    # Widget 6: Faculty Connections
    html.Div([
        html.H2("Discover Connections to Your Ideal Faculty Candidate"),
        html.Div([
            html.Label('Origin Faculty Name (optional):'),
            dcc.Input(id='input-origin-faculty', type='text', value=''),
            html.Label('Origin Institute:'),
            dcc.Input(id='input-origin-institute', type='text', value=''),
            html.Label('Destination Faculty Name:'),
            dcc.Input(id='input-dest-faculty', type='text', value=''),
            html.Label('Destination Institute:'),
            dcc.Input(id='input-dest-institute', type='text', value=''),
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]),
        cyto.Cytoscape(
            id='cytoscape-graph',
            elements=[],
            layout={'name': 'klay'},
            style={'width': '100%', 'height': '500px'},
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'text-wrap': 'wrap',
                        'text-max-width': '150px',
                        'text-size': 3  # Set font size to 10 pixels
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'label': 'data(label)',
                        'width': 2,
                        'line-color': '#ccc'
                    }
                }
            ]
        )
    ], className="widget", style={"height": "600px"})

], fluid=True)

# Callbacks
@app.callback(
    Output("results-widget1", "children"),
    [Input("submit-button-widget1", "n_clicks")],
    [dash.dependencies.State("keyword-input", "value")]
)
def display_results_widget1(n_clicks, keyword):
    if n_clicks and keyword:
        df = get_top_universities(keyword)

        if not df.empty:
            return html.Div([
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            ], className='scrollable-table')
        else:
            return "No results to display."
    else:
        return "No results to display."

@app.callback(
    Output("results-widget2", "children"),
    [Input("submit-button-widget2", "n_clicks")],
    [
        State("faculty-name-input", "value"),
        State("university-name-input", "value"),
        State("start-year-input", "value"),
        State("end-year-input", "value"),
    ]
)
def display_results_widget2(n_clicks, faculty_name, university_name, start_year, end_year):
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

@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('submit-button', 'n_clicks'),
    [State('input-origin-faculty', 'value'),
     State('input-origin-institute', 'value'),
     State('input-dest-faculty', 'value'),
     State('input-dest-institute', 'value')]
)
def display_results_widget6(n_clicks, origin_faculty, origin_institute, dest_faculty, dest_institute):
    nodes_df, edges_df = find_faculty_connections(origin_faculty, origin_institute, dest_faculty, dest_institute)

    nodes_elements = [
        {"data": {"id": str(row["id"]), "label": row["label"]}}
        for _, row in nodes_df.iterrows()
    ]

    edges_elements = [
        {"data": {"source": str(row["source"]), "target": str(row["target"])}}
        for _, row in edges_df.iterrows()
    ]

    return nodes_elements + edges_elements

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
