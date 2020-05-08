import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, project


graphs = [
    {"label": "Bar Graph", "value": "1"},
    {"label": "Line Graph", "value": "2"},
    {"label": "Pie Graph", "value": "3"},
]

layout = html.Div([
    html.H1('Data Visualization', style={'text-align': 'center'}),
    dcc.Dropdown(id='graphs_list', searchable=False, placeholder="Select the graph", value='GRAPH'),
    html.Label(
        [
            "Multi dynamic Dropdown",
            dcc.Dropdown(id="columns", multi=True),
        ]
    ),
    html.Button('Display Graph', id='display', n_clicks=0),
    html.Div(id='graph',
             children='')
], style={'columnCount': 1, 'text-align': 'center'})


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
def update_options(a,b,c):
    return [{'label': i, 'value': i} for i in project.dataset.df.columns]


@app.callback(
    Output('graph', 'children'),
    [Input('display', 'n_clicks'),Input('columns', 'value')])
def update_output(n_clicks, values):
    if n_clicks >= 1 and len(values)>=2:
        if graph_name == "1":
            fig = px.bar(project.dataset.df, x=values[0], y=values[1])
            return dcc.Graph(figure=fig)
        elif graph_name == "2":
            fig = px.line(project.dataset.df, x=values[0], y=values[1])
            return dcc.Graph(figure=fig)
        elif graph_name == "3":
            fig = px.pie(project.dataset.df, values=values[0], names=values[1], title='')
            return dcc.Graph(figure=fig)