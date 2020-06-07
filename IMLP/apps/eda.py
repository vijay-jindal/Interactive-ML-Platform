import dash
from dash import no_update
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
    {"label": "Scatter Graph", "value": "4"},
    {"label": "Box Graph", "value": "5"},
    {"label": "Histogram Graph", "value": "6"}]

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

interpreter = html.Iframe(src="http://localhost:5000",
            style={'width': "100%",
                   'height': "1000",
                   'frameborder': "0",
                   'marginwidth': "0",
                   'marginheight': "0", 'allowfullscreen': 'true'},
            id='interpreter',
            height=500),
#
interpreter_collapse = html.Div(
                    [
                        dbc.Button(
                            "Use Python Terminal for EDA",
                            id="interpreter-btn",
                            className="mb-3",
                            color='primary', style={'width': '100%'}
                        ),
                        dbc.Collapse(id='interpreter_collapse')])

graph_list = dcc.Dropdown(id='graphs_list', searchable=False, placeholder="Select the graph", value='GRAPH', style={'width':'100%'})
column_list = dcc.Dropdown(id="columns", multi=True, style={'width':'100%'})
display_graph_btn = html.Button('Display Graph', id='display', n_clicks=0, style={'width':'100%'}),
breakline = html.Br()
eda_page_contents = dbc.Card(children=[
    dbc.CardBody(
        [
            dbc.Row(breakline),
            dbc.Row(graph_list),
            dbc.Row(breakline),
            dbc.Row(column_list),
            dbc.Row(breakline),
            dbc.Row(display_graph_btn),
            dbc.Row(breakline),
            dbc.Row(interpreter_collapse),
        ], id='algorithm_select_display', style={'display': 'block','padding': '10px 25px 40px'})]),

# component to compile all the elements into single element
layout = html.Div(
    [
        dbc.Row(navbar),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("EXPLORATORY DATA ANALYSIS",
                                       style={'font-family': 'Times New Roman', 'font-size': '15px', 'color': 'white',
                                              'background-color': 'green'}),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Card([html.Div(id='graph',children='')],outline=True, color="info",
                                                     style={'padding': '10px 25px 40px', 'height': '50rem','overflowY': 'scroll'}
                                                     ),width=8),
                                    dbc.Col(dbc.Card(eda_page_contents, outline=True, color="info",
                                                     style={'padding': '10px 25px 40px', 'height': '50rem',
                                                            'overflowY': 'scroll'}
                                                     ), width=4, align="center"),
                                ]
                            )
                        )
                    ], outline=True, color='success'
                ),
                style={'padding': '10px 40px 20px'}
            )
        ),

    ],
)


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
    [Output('graph', 'children'),Output('interpreter_collapse','is_open')],
    [Input('display', 'n_clicks'),Input('interpreter-btn','n_clicks')],
    [State("interpreter_collapse", "is_open"),State('columns', 'value')])
def update_output(n_clicks, click, is_open, values):

    component_clicked_id = ""
    ctx = dash.callback_context
    if not ctx.triggered:
        print('Nothing clicked yet.')
        raise PreventUpdate
    else:
        component_clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if component_clicked_id == "interpreter-btn":
        if click:
            return interpreter, not is_open
        return no_update, is_open

    if component_clicked_id == "display":
        if len(values) >= 2:
            if graph_name == "1":
                fig = px.bar(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
            elif graph_name == "2":
                fig = px.line(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
            elif graph_name == "3":
                fig = px.pie(project.dataset.df, values=values[0], names=values[1], title='')
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
            elif graph_name == "4":
                fig = px.scatter(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
            elif graph_name == "5":
                fig = px.box(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
            elif graph_name == "6":
                fig = px.histogram(project.dataset.df, x=values[0], y=values[1])
                return dcc.Graph(figure=fig,style={'width':'100%','height':'100%'}), no_update
    else:
        raise PreventUpdate
    raise PreventUpdate

