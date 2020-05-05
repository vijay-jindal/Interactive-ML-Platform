import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px
import base64
import datetime
import io


df = pd.read_csv('winequality-white.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
learning_type = ""
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tabs_styles = {
    'height': '60px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
                html.Div(className="row",
                         children=[html.Div(className="five columns",
                                            children=[
                                                    html.H1('Data Pre-processing', style={'text-align': 'center'}),
                                                    dcc.Dropdown(id='learning_type', searchable=False, placeholder="Select the Learning type"),
                                                    html.Br(),
                                                    dcc.Dropdown(id='algorithm_name', searchable=False, placeholder="Select the Algorithm"),
                                                    html.Br(),
                                                    html.Label('Select the Split Ratio', style={'text-align': 'center'}),
                                                    dcc.Slider(
                                                        id='split_ratio',
                                                        min=0,
                                                        max=100,
                                                        step=5,
                                                        value=20,
                                                    ),
                                                    html.Div(id='split_ratio_value'),
                                                    html.Br(),
                                                dcc.Tabs(id='preprocess_tabs', value='tabs', children=[
                                                    dcc.Tab(label='Missing Values', value='tab-1',style=tab_style, selected_style=tab_selected_style, children=
                                                            [html.Div(children=[
                                                                html.Br(),
                                                                dcc.Dropdown(id="d1", multi=True,
                                                                             placeholder='Select'),
                                                                html.Br(),
                                                                dcc.Dropdown(id="d2", multi=True,
                                                                             placeholder='Select'),]),
                                                             html.Br(),
                                                             ]),
                                                    dcc.Tab(label='Duplicate Columns(Value)', value='tab-2',style=tab_style, selected_style=tab_selected_style),
                                                    dcc.Tab(label='Duplicate Rows', value='tab-3',style=tab_style, selected_style=tab_selected_style),
                                                    dcc.Tab(label='Normalization', value='tab-4', style=tab_style,
                                                            selected_style=tab_selected_style),

                                                ],style=tabs_styles),

                                                html.Br(),
                                                dcc.Dropdown(id="feature_column", multi=True,placeholder='Select Feature Columns'),
                                                    html.Br(),
                                                    dcc.Dropdown(id='target_column', searchable=False,placeholder="Select the Target Column")]),
                                                    html.Div(className="seven columns",
                                                             children=[
                                                                dash_table.DataTable(
                                                                    id='table',
                                                                    columns=[{"name": i, "id": i} for i in df.columns],
                                                                    data=df.to_dict('records'),page_size=20,style_table={'overflowY': 'auto','overflowX': 'auto','overflowY': 'auto'})]),
                                   ]),
                ], style={'columnCount': 1, 'text-align': 'center'})

@app.callback(
dash.dependencies.Output("learning_type", "options"),
[Input('learning_type', 'value')])
def update_learning_types(value):
    return [
        {"label": learning_type, "value": learning_type} for learning_type in learning_types
]


@app.callback(
    dash.dependencies.Output("algorithm_name", "options"),
    [Input('algorithm_name', 'value'),Input('learning_type', 'value')])
def update_algorithm_types(value1,value2):
    if value2 is None:
        return []
    else:
        return [
        algorithm for algorithm in algorithms[value2]
    ]

@app.callback(
    dash.dependencies.Output('split_ratio_value', 'children'),
    [dash.dependencies.Input('split_ratio', 'value')])
def update_output(value):
    return 'Testing : {}% and Training : {}%'.format(value,100-value)

@app.callback(
    dash.dependencies.Output("feature_column", "options"),
    [dash.dependencies.Input("feature_column", "search_value"), Input('target_column', 'value')],
)
def update_options(search_value, value):
    if value is None:
        return [{'label': i, 'value': i} for i in df.columns]
    else:
        return [{'label': i, 'value': i} for i in df.columns if i != value]

@app.callback(
    dash.dependencies.Output("target_column", "options"),
    [Input('feature_column', 'value')],
)
def update_options(value):
    target_columns =[]
    if value is None:
        return [{'label': i, 'value': i} for i in df.columns]

    for column in df.columns:
        if column not in value:
            target_columns.append(column)

    return [{'label': i, 'value': i} for i in target_columns]



learning_types = ['Supervised', 'Unsupervised']

algorithms = {"Supervised": [
    {"label": "Random Forest", "value": "RF"},
    {"label": "SVM", "value": "SVM"}], "Unsupervised": [{"label": "KNN", "value": "1"}]}

preprocess_functions = [{"label": "Missing Values Check", "value": "MVC"},
                        {"label": "Remove Duplicate Column(Values)", "value": "RDC"},
                        {"label": "Remove Duplicate Rows", "value": "RF"},
                        {"label": "Normalization", "value": "RF"},
                        {"label": "Random Forest", "value": "RF"},
                        {"label": "Random Forest", "value": "RF"}]

MVC_options = [{"label": "Remove Missing Values", "value": "RMV"},
               {"label": "Impute Missing Values", "value": "IMV"}]


if __name__ == '__main__':
    app.run_server(debug=True)
