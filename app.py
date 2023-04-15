import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State

from neo4j import GraphDatabase

from mysql_utils import get_university

# neo_db = db = GraphDatabase.driver('bolt://127.0.0.1:7687')

# Dash constructor (Initialize the app)
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Input(id='input'),
    html.Button('Search', id='search_button'),
    dash_table.DataTable(
        columns = [{'name': 'University Name', 'id': 'name'}, {'name': 'University Id', 'id': 'id'}],
        id='university_table'),
    dcc.Textarea(id='tid')
])

@callback(
    Output('university_table', 'data'),
    Output('tid', 'value'),
    State('input', 'value'),
    Input('search_button', 'n_clicks')
)

def update_table(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    result = get_university(input_value)
    print(result)
    return result, 'search result for :' + input_value

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)