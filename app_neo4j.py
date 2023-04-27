import dash
from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import dash_cytoscape as cyto

from neo4j_utils import find_faculty_connections

# Dash constructor (Initialize the app)
app = Dash(__name__)

cyto.load_extra_layouts()


# # Define Dash app layout
# app.layout = html.Div([
#     cyto.Cytoscape(
#         id='cytoscape-graph',
#         elements=elements,
#         layout={'name': 'klay'},
#         style={'width': '100%', 'height': '500px'},
#         stylesheet=[
#             {
#                 'selector': 'node',
#                 'style': {
#                     'label': 'data(label)',
#                     'text-valign': 'center',
#                     'text-halign': 'center',
#                     'text-wrap': 'wrap',
#                     'text-max-width': '150px',
#                     'text-size': 3  # Set font size to 10 pixels
#                 }
#             },
#             {
#                 'selector': 'edge',
#                 'style': {
#                     'label': 'data(label)',
#                     'width': 2,
#                     'line-color': '#ccc'
#                 }
#             }
#         ]
#     )
# ])

# Define Dash app layout
app.layout = html.Div([
    # Add input fields
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
])


# Add a callback function to fetch the results based on user input
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('submit-button', 'n_clicks'),
    [State('input-origin-faculty', 'value'),
     State('input-origin-institute', 'value'),
     State('input-dest-faculty', 'value'),
     State('input-dest-institute', 'value')]
)
def update_graph(n_clicks, origin_faculty, origin_institute, dest_faculty, dest_institute):
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
