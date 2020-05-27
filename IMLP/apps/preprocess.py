import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from app import app, project
import pandas as pd

# dataframe object with no value for default datatable content
from dash.exceptions import PreventUpdate

df = pd.DataFrame()

# few basic styles for tabs component
tabs_styles = {
    'height': '60px', 'width': '300px'
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

# Header bar
navbar = dbc.NavbarSimple(
    brand="Interactive ML Platform",
    color="success",
    brand_style={'font-size': '20px'},
    children=[
        dcc.Link(dbc.Button(
            "Exploratory Data Analysis (EDA)",
            id="eda_btn",
            className="mb-3", outline=True,
            color="dark", style={'width': '100%', 'font-size': '10px'}), href="/eda")
    ],
    dark=True, style={
        'width': '100%',
        'height': '7rem',
        'verticalAlign': 'middle'
    }
)

# Breakline
breakline = html.Br()

# Component to take dataset input
upload_dataset = dcc.Upload(
    id='upload-data',
    children=html.Div([breakline, breakline, breakline, breakline, breakline, breakline, breakline, breakline,
                       html.A('Drag and Drop or ',
                              style={'font-size': '20px', 'vertical-align': 'middle', 'align': 'center'}), html.Br(),
                       html.A('Select Files',
                              style={'font-size': '20px', 'color': 'blue', 'text-decoration': 'underline',
                                     'vertical-align': 'middle', 'align': 'center'})
                       ], style={'width': '100%', 'vertical-align': 'middle', 'height': '100%', 'align': 'center', }),
    style={
        'width': '100%',
        'height': '400px',
        'lineHeight': '20px',
        'textAlign': 'center',
        'margin': '10px', 'vertical-align': 'middle'
    })

update_btn_tooltip = dbc.Tooltip("Clicking this button will update the data and this step is not reversible!!",
                                 target="update_dataset_btn",
                                 ),

missing_value_collapse = html.Div(
    [
        dbc.Button(
            "Missing Values",
            id="missing-value-button",
            className="mb-3",
            color='primary', style={'width': '100%'}
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                dcc.Dropdown(id="placeholders", multi=True, placeholder='Select placeholders', style=dict(
                    width='100%',
                    verticalAlign="middle")), breakline,
                dbc.Button(
                    "Find Missing Values",
                    id="check-missing-value-button", outline=True,
                    className="mb-3", n_clicks=0,
                    color='success', style={'width': '100%'}
                ), breakline,
                dcc.Dropdown(id="missing-value-action-dropdown", multi=False,
                             placeholder='Select Action for Missing Values', style=dict(
                        width='100%',
                        verticalAlign="middle")), breakline,
                html.Div(
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    "APPLY",
                                    id="apply_btn", color='success',
                                    outline=True,
                                    className="mb-3", n_clicks=0,
                                    style={'width': '100%'})
                            ],
                            id='apply_col', style={'width': 'auto'}),
                        dbc.Col([
                            dbc.Button(
                                "REVERT",
                                id="cancel_btn", color='danger',
                                className="mb-3", n_clicks=0,
                                outline=True,
                                style={'width': '100%'})
                        ], id='cancel_col', style={'width': 'auto'}),
                        dbc.Col([
                            dbc.Button(
                                "UPDATE DATASET",
                                id="update_dataset_btn", color='danger',
                                className="mb-3", n_clicks=0,
                                outline=True, block=True,
                                style={'width': '100%'}),
                        ], id='update_col', style={'width': 'auto'}),
                    ],
                    id='apply_or_cancel', style={'display': 'none'}), breakline,
            ])),
            id="missing_value",
        ),
    ], style={'width': '100%'}
)

duplicate_column_collapse = html.Div(
    [
        dbc.Button(
            "Duplicate Columns",
            id="duplicate-column-button",
            className="mb-3",
            color='primary', style={'width': '100%'}
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([breakline,
                                   dcc.Dropdown(id="duplicate-columns", multi=True, placeholder='Select columns',
                                                style=dict(
                                                    width='100%',
                                                    verticalAlign="middle")), breakline,
                                   dbc.Button(
                                       "Find Duplicate columns",
                                       id="find-duplicate-columns",
                                       className="mb-3", n_clicks=0,
                                       color='success', style={'width': '100%'}
                                   ), breakline,
                                   dcc.Dropdown(id="duplicate-column-action-dropdown", multi=False,
                                                placeholder='Select Action for Duplicate Columns', style=dict(
                                           width='100%',
                                           verticalAlign="middle")), breakline,

                                   ])),
            id="duplicate_columns",
        ),
    ], style={'width': '100%'}
)

finish_preprocessing_button = dbc.Button(
    "FINISH PREPROCESSING",
    id="finish-preprocessing-button",
    className="mb-3",
    color='success', style={'width': '100%'}
),

# Tabs to do perform various preprocessing steps independently by the user
process_tabs = dcc.Tabs(id='preprocess_tabs', value='tab-1', children=[
    dcc.Tab(label='Pre-process functions', value='tab-1', children=
    [
    ])
], style={
    'height': '80px', 'width': '330px'
}),

# Datatable to show the dataset to the user
# TODO: Pagination page number text box width to be increased
datatable_before_apply = dash_table.DataTable(id='table1', css=[{'selector': '.row', 'rule': 'margin: 0'},
                                                                {"selector": ".show-hide", "rule": "display: none"}],
                                              columns=[{"name": i, "id": i} for i in df],
                                              data=df.to_dict('records'),
                                              page_size=13,
                                              page_action="native",
                                              page_current=0,
                                              style_table={'overflowX': 'auto', 'display': 'block'})
# Cardbody component to compile all preprocessing elements into single component
preprocess_flow = [
    dbc.CardBody(
        [
            dbc.Row(html.Div("Preprocessing Steps")),
            dbc.Row(dbc.CardBody([
            dbc.Row(breakline),
            dbc.Row(missing_value_collapse),
            dbc.Row(duplicate_column_collapse),
            dbc.Row(finish_preprocessing_button)
            ])
),
        ])]

# Cardbody component to compile dataset upload and view into single component
dataset_input_display = dbc.Card(
    dbc.CardBody(
        [upload_dataset, datatable_before_apply], style={'height': '57rem'}
    ), outline=True, color="info"
)

# Component to show page footer
page_footer = html.Div(children=[breakline, breakline, breakline],
                       style={'width': '100%', 'height': '40%', 'background-color': 'black'})

toast_div1 = html.Div(id='toast1')
toast_div2 = html.Div(id='toast2')

finish_warning_modal = dbc.Modal(
    [
        dbc.ModalHeader("Preprocessing Error"),
        dbc.ModalBody([dbc.Label("One or more fields have NOT been selected"),
                       ]),
        dbc.ModalFooter(
            [dbc.Button("Close", id="close", className="ml-auto"), ]),
    ],
    id="preprocessing_modal",
)

# component to compile all the elements into single element
layout = html.Div(
    [
        dbc.Row(navbar),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("DATA PRE-PROCESSING",
                                       style={'font-family': 'Times New Roman', 'font-size': '15px', 'color': 'white',
                                              'background-color': 'green'}),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(dataset_input_display, width=8),
                                    dbc.Col(dbc.Card(preprocess_flow, outline=True, color="info",
                                                     style={'padding': '10px 25px 40px', 'height': '57rem',
                                                            'overflowY': 'scroll'}), width=4, align="center"),
                                ]
                            )
                        )
                    ], outline=True, color='success'
                ),
                style={'padding': '10px 40px 20px'}
            )
        ), dbc.Row(toast_div1), dbc.Row(toast_div2), html.Div(id='linkx'),

    ],
)


# CALLBACKS

def construct_toast(header, message, status):
    toast = dbc.Toast(
        message,
        id="toastx",
        header=header,
        is_open=True,
        dismissable=True,
        icon=status,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )
    return toast


@app.callback(Output("toast1", "children"),
              [Input('upload-data', 'filename')], [State('upload-data', 'contents')])
def show_toast(filename, contents):
    if filename is None:
        return None
    elif hasattr(project, "dataset") and contents is not None:
        df_info = project.dataset.info()
        return construct_toast("Dataset Info", "Dataset has been uploaded.\n {}".format(df_info), "info")


apply_cancel = 0
place_values = []
missing_val_click = 0
start = 0


# this is an important callback which makes the apply and cancel button appear or disappear
# this callback updates the apply_cancel variable to let the next callback know which button is clicked.
# this callback is triggered when the dropdown for the missing value action is altered.
# this style of dropdown for missing values is changed at every button click in the preprocess stage and hence it
# keeps updating cancel and apply button all the time.
@app.callback([Output('cancel_col', 'style'), Output('apply_col', 'style')],
              [Input('missing-value-action-dropdown', 'options')])
def apply_action(click):
    global apply_cancel
    if apply_cancel == 0:
        # CANCEL
        # print("Apply value is cancel",start,apply_cancel)
        apply_cancel = 1
        return {'display': 'none'}, {'display': 'block'}
    elif apply_cancel == 1:
        # APPLY
        # print("Apply value is apply",start,apply_cancel)
        apply_cancel = 0
        return {'display': 'block'}, {'display': 'none'}


# callback to take dataset from user and display it in the datatable
@app.callback([Output("table1", "data"),
               Output("table1", "columns"),
               Output("upload-data", "style"),
               Output("table1", "style_data_conditional"),
               Output("table1", "hidden_columns"),
               Output("toast2", "children"),
               Output('missing-value-action-dropdown', 'options'),
               Output('missing-value-action-dropdown', 'style')],
              [Input('upload-data', 'contents'),
               Input('check-missing-value-button', 'n_clicks'),
               Input('apply_btn', 'n_clicks'), Input('cancel_btn', 'n_clicks')],
              [State('upload-data', 'filename'),
               State('placeholders', 'value'), State("table1", "data")])
def update_output(content, missing_clicks, apply_click, cancel_click, name, value, datatableData):
    global place_values
    global missing_val_click
    global apply_cancel
    global start

    if not project:
        df = pd.DataFrame()
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {'display': 'block',
                                                                                   'vertical-align': 'middle',
                                                                                   'width': '100%', 'height': '470px',
                                                                                   'lineHeight': '20px',
                                                                                   'textAlign': 'center'}, construct_toast(
            "ERROR",
            "Please Enter a project name and upload dataset",
            "danger"), None, None, [], {
                   'display': 'none'}

    if value is not None:
        # if the placeholders change, find missing values
        if set(place_values) != set(value):
            place_values = value
            # print("Missing values button clicked",place_values)
            missing_val_click = missing_clicks
            df = project.dataset.df
            apply_cancel = 0
            df['missing-values'] = project.dataset.missing_value_indicator(value)
            style_data_conditional = [{
                'if': {'filter_query': '{missing-values} eq "true"'},
                'backgroundColor': '#3D9970',
                'color': 'white'
            }]
            return df.to_dict('records'), \
                   [{"name": i, "id": i} for i in df.columns], \
                   {'display': 'none'}, style_data_conditional, ['missing-values'], \
                   construct_toast("Dataset Info",
                                   "Found {} missing values.\nRows with missing values are highlighted.".format(
                                       len(df[df['missing-values'] == "true"].index)),
                                   "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}

        # if placeholders do not change, check if apply or cancel button is clicked.
        # start is used to see, if the dataset is uploaded or not.
        # the count of missing values is checked. If they are equal, missing value button is not clicked.
        elif missing_val_click == missing_clicks and start == 1:
            # if apply_cancel =1 , it is always apply button clicked
            if apply_cancel == 1:
                # print("Apply button clicked",apply_cancel)
                df1 = pd.DataFrame(datatableData)
                df = df1[df1['missing-values'] == "false"].drop(columns='missing-values')
                return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                    'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                    "Deleted {} rows with missing values.".format(
                                                                        len(df1[df1[
                                                                                    'missing-values'] == "true"].index)),
                                                                    "danger"), \
                       [{"label": action, "value": action} for action in missing_value_actions], \
                       {'width': '100%', 'display': "block"}

            # if apply_cancel = 0 , it is always cancel button clicked.
            elif apply_cancel == 0:
                # print("Cancel button clicked",apply_cancel)
                df = pd.DataFrame(project.dataset.df)
                return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                    'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                    "Restored {} rows with missing values.".format(
                                                                        len(df[df['missing-values'] == "true"].index)),
                                                                    "danger"), \
                       [{"label": action, "value": action} for action in missing_value_actions], \
                       {'width': '100%', 'display': "block"}

        else:
            place_values = value
            # print("Missing values button clicked",place_values)
            missing_val_click = missing_clicks

            df = project.dataset.df
            apply_cancel = 0
            df['missing-values'] = project.dataset.missing_value_indicator(value)
            style_data_conditional = [{
                'if': {'filter_query': '{missing-values} eq "true"'},
                'backgroundColor': '#3D9970',
                'color': 'white'
            }]
            return df.to_dict('records'), \
                   [{"name": i, "id": i} for i in df.columns], \
                   {'display': 'none'}, style_data_conditional, ['missing-values'], \
                   construct_toast("Dataset Info",
                                   "Found {} missing values.\nRows with missing values are highlighted.".format(
                                       len(df[df['missing-values'] == "true"].index)),
                                   "danger"), [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}


    elif content is not None and start == 0:
        # print("Content is not empty")
        project.upload_dataset(content, name),
        df = project.dataset.df
        start = 1
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
            'display': 'none'}, None, None, None, [], {'display': 'none'}
    else:
        # print("Content is empty")
        start = 0
        df = pd.DataFrame()
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {'display': 'block',
                                                                                   'vertical-align': 'middle',
                                                                                   'width': '100%', 'height': '470px',
                                                                                   'lineHeight': '20px',
                                                                                   'textAlign': 'center'}, None, None, None, [], {
                   'display': 'none'}


@app.callback(
    [Output("missing_value", "is_open"), Output("placeholders", "options")],
    [Input("missing-value-button", "n_clicks")],
    [State("missing_value", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open, [{"label": placeholder, "value": placeholder} for placeholder in placeholders]
    return is_open, [{"label": placeholder, "value": placeholder} for placeholder in placeholders]


@app.callback(Output('apply_or_cancel', 'style'),
              [Input('missing-value-action-dropdown', 'value')])
def show_buttons(value):
    if value is None:
        return {'display': 'none'}
    elif (value == 'Remove Rows With Missing Values'):
        return {'display': 'block'}
    elif (value == 'Fill Missing Values'):
        return {'display': 'none'}


@app.callback(Output('update_dataset_btn', 'color'),
              [Input('update_dataset_btn', 'n_clicks')],
              [State('table1', 'data')])
def update_dataset(update, content):
    # print(update,content)
    if update is not None and content is not None:
        if update > 0:
            project.dataset.df = pd.DataFrame(content)
            # print(project.dataset.df)
            return 'success'
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



@app.callback(Output('linkx', 'children'),
              [Input('finish-preprocessing-button', 'n_clicks')])
              # [State('learning_type', 'value'), State('algorithm_name', 'value')
              #     , State('split_ratio', 'value'), State('feature_column', 'value'),
              #  State('target_column', 'value')])
def finish_preprocessing(click):
    if click is not None and click > 0:
        return dcc.Location(pathname="/model", id="someid_doesnt_matter")
    else:
        raise PreventUpdate

placeholders = ['', '.', '?', '-1']
missing_value_actions = ['Remove Rows With Missing Values', 'Fill Missing Values']