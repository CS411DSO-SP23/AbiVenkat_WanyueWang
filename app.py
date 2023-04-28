import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

from mysql_utils import get_top_universities, get_coauthored_count, get_faculty_krc
from neo4j_utils import find_faculty_connections
from mongodb_utils import insert_faculty, delete_faculty, get_favorites
from dash import callback_context
cyto.load_extra_layouts()

# Dash constructor (Initialize the app)
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# App layout
app.layout = dbc.Container([
    html.Link(rel='stylesheet', href='/assets/style.css'),
    html.Br(),
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
                            dbc.FormText("Enter a keyword to search for universities and faculty members."),
                            html.Br(),
                            html.Br(),
                            dbc.Label("Keyword:", html_for="keyword-input"),
                            dbc.Input(id="keyword-input", type="text", placeholder="Enter keyword"),
                            dbc.Button("Submit", id="submit-button-widget1", color="primary", className="mt-2")
                        ])
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div(id="results-widget1")
                    ])
                ]),
            ], className="widget", style={"height": "700px"}),

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
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(id="results-widget2"),
            ], className="widget", style={"height": "700px"})
        ], width=6)
    ]),

    # Widget 3: Faculty KRC Scores
    html.Div([
        html.H2("Explore Faculty KRC Information"),
        dbc.Row([
            dbc.Col([
                dbc.FormText("Enter a faculty name to see their keyword releveant citation scores for each of their keywords"),
                html.Br(),
                html.Br(),
                html.Label('Faculty Name'),
                dbc.Input(id='faculty_name_krc', type='text', value='', style={'max-width' :  '600px'}),
                dbc.Button("Submit", id="submit-button-widget5", color="primary"),
                
            ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Div(id="krc_graph")
            ])
            
        ])
        ]),
    ],className="widget", style={"height": "auto"}),

    # Widget 4 & 5: Insert and Delete Favorite Faculty
    html.Div([
                html.H2("Curate A List of Your Favorite Professors"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Faculty Name To Add"),
                        dbc.Input(id="faculty_insert", type="text", placeholder="Enter faculty name"),
                    ]),
                    dbc.Col([
                        dbc.Label("Faculty Name To Delete"),
                        dbc.Input(id="faculty_delete", type="text", placeholder="Enter university name"),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Note"),
                        dbc.Input(id="note", type="text", placeholder="(Optional) Note about faculty member"),
                        dbc.Button("Add", id="add-button-widget4", color="primary"),
                    ]),
                    dbc.Col([
                        dbc.Button("Delete", id="delete-button-widget5", color="primary"),
                    ])
                ]),
                
                html.Br(),
                html.Div(id="results_widget45"),
            ], className="widget", style={"height": "auto"})
        ,

    # Widget 6: Faculty Connections
    html.Div([
        html.H2("Discover Connections to Your Ideal Faculty Candidate"),
        dbc.Row([
            dbc.Col([
                html.Label('Origin Faculty Name (optional):'),
                dbc.Input(id='input-origin-faculty', type='text', value='')
            ]),
            dbc.Col([
                html.Label('Destination Faculty Name:'),
                dbc.Input(id='input-dest-faculty', type='text', value='')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Origin Institute:'),
                dbc.Input(id='input-origin-institute', type='text', value='')
            ]),
            dbc.Col([
                html.Label('Destination Institute:'),
                dbc.Input(id='input-dest-institute', type='text', value='')
            ])
        ]),
        dbc.Button("Submit", id="submit-button-widget6", color="primary"),
        # html.Button('Submit', id='submit-button', n_clicks=0),
        cyto.Cytoscape(
            id='cytoscape-graph',
            elements=[],
            layout={'name': 'klay'},
            style={'width': '100%', 'height': '400px'},
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'text-valign': 'top',
                        'text-halign': 'center',
                        'text-wrap': 'wrap',
                        'text-max-width': '150px',
                        'font-size': 5,
                        'width': 10,
                        'height': 10,
                        'background-color': '#4682B4'
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
    ], className="widget", style={"height": "auto"})

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
    Input('submit-button-widget6', 'n_clicks'),
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


@app.callback(
    Output('krc_graph', 'children'),
    Input('submit-button-widget5', 'n_clicks'),
    [State('faculty_name_krc', 'value')],
    prevent_initial_call=True
)
def draw_krc_graph(n_clicks, faculty_name):
    df = get_faculty_krc(faculty_name)
    return html.Div(
            dcc.Graph(
                id='bar chart',
                figure={
                    "data": [
                        {
                            "x": df["keyword_name"],
                            "y": df["KRC"],
                            "type": "bar",
                            "marker": {"color": "#0B3D91"},
                        }
                    ],
                    "layout": {
                        'title': 'KRC Scores for ' + faculty_name,
                        "xaxis": {"title" : {"text": "Keywords", "standoff"  : "10"}, "automargin":  True},
                        "yaxis": {"title": "KRC"},
                        'plot_bgcolor': 'rgb(217,227,241)',
                        'paper_bgcolor': 'rgb(217,227,241)',
                        'height' : '600'
                    },
                },
            )
    )



@app.callback(
    Output('results_widget45', 'children'),
    Input('add-button-widget4', 'n_clicks'),
    Input('delete-button-widget5', 'n_clicks'),
    [State('faculty_insert', 'value'),
     State('note', 'value'),
     State('faculty_delete','value')],
    prevent_initial_call=True
)
def update_favorites_table(add_btn, delete_btn, fac_insert, note, fac_delete):
    if callback_context.triggered_id=="add-button-widget4" and fac_insert is not None:
        if note is not None:
            insert_faculty(fac_insert, note)
        else:
            insert_faculty(fac_insert)
    elif callback_context.triggered_id=="delete-button-widget5" and fac_delete is not None:
        delete_faculty(fac_delete)
    
    return dbc.Table.from_dataframe(get_favorites(), striped=True, bordered=True, hover=True, size='lg')
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
