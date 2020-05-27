import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app, project
from dash.exceptions import PreventUpdate

graphs = [
    {"label": "Bar Graph", "value": "1"},
    {"label": "Line Graph", "value": "2"},
    {"label": "Pie Graph", "value": "3"},
]

# Header bar
navbar = dbc.NavbarSimple(
    brand="Interactive ML Platform",
    brand_style={'font-size':'20px'},
    color="success",
    dark=True, style={
        'width': '100%',
        'height': '7rem',
        'text-size':'15px',
        'verticalAlign': 'middle'
    }
)

interpreter = html.Iframe(src="https://repl.it/repls/PurpleHeavyRuntimes?lite=true",
            style={'width': "100%",
                   'height': "1000",
                   'frameborder': "0",
                   'marginwidth': "0",
                   'marginheight': "0", 'allowfullscreen': 'true'},
            id='interpreter',
            height=500),

interpreter_collapse = html.Div(
                    [
                        dbc.Button(
                            "Use Python Terminal for EDA",
                            id="interpreter-btn",
                            className="mb-3",
                            color='primary', style={'width': '100%'}
                        ),
                        dbc.Collapse(interpreter,id='interpreter_collapse')])


layout = html.Div([
    navbar,
    html.Div([
    html.H1('Exploratory Data Analysis (EDA)', style={'text-align': 'center'}),
    dbc.Card( dbc.CardBody([
        dcc.Dropdown(id='graphs_list', searchable=False, placeholder="Select the graph", value='GRAPH'),
        html.Label(
        [
            "Multi dynamic Dropdown",
            dcc.Dropdown(id="columns", multi=True),
        ]),
                   html.Button('Display Graph', id='display', n_clicks=0),
                   html.Div(id='graph',children=''),html.Br(),interpreter_collapse]),outline=True, color='success',
style={'padding': '20px 30px 20px'}
    )], style={'columnCount': 1, 'text-align': 'center','padding': '20px 30px 20px'})])



@app.callback(Output('interpreter_collapse','is_open'),
              [Input('interpreter-btn','n_clicks')],
              [State("interpreter_collapse", "is_open")])
def open_details(n,is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("graphs_list", "options"),
    [Input('graphs_list', 'value')])
def update_multi_options(value):
    global graph_name
    graph_name = value
    return [
        graph for graph in graphs
    ]


@app.callback(
    Output("columns", "options"),
    [Input("columns", "search_value"), Input('columns', 'value'), Input('graphs_list', 'value')],
)
def update_options(a, b, c):
    return [{'label': i, 'value': i} for i in project.dataset.df.columns]


@app.callback(
    Output('graph', 'children'),
    [Input('display', 'n_clicks'), Input('columns', 'value')])
def update_output(n_clicks, values):
    if n_clicks is not None and values is not None:
        if n_clicks >= 1 and len(values) >= 2:
            if graph_name == "1":
                fig = px.bar(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig)
            elif graph_name == "2":
                fig = px.line(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig)
            elif graph_name == "3":
                fig = px.pie(project.dataset.df, values=values[0], names=values[1], title='')
                return dcc.Graph(figure=fig)
    else:
        raise PreventUpdate

