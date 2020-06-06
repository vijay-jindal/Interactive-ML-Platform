import dash
from dash import no_update
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

upload_dataset_tooltip = html.Div(
    [
        dbc.Tooltip("Upload a csv file as the dataset", target="upload-data"),
    ],
)

# Component to take dataset input
upload_dataset = dcc.Upload(
    id='upload-data',
    children=html.Div([upload_dataset_tooltip,breakline, breakline, breakline, breakline, breakline, breakline, breakline, breakline,
                       html.A('Drag and Drop a csv file or ',
                              style={'font-size': '20px', 'vertical-align': 'middle', 'align': 'center'}), html.Br(),
                       html.A('Select CSV Files',
                              style={'font-size': '20px', 'color': 'blue', 'text-decoration': 'underline',
                                     'vertical-align': 'middle', 'align': 'center'})
                       ], style={'width': '100%', 'vertical-align': 'middle', 'height': '100%', 'align': 'center'}),
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

update_dataset_button_missing = dbc.Button(
    "UPDATE DATASET",
    id="update_dataset_btn_missing", color='danger',
    className="mb-3", n_clicks=0,
    outline=True, block=True,
    style={'width': '100%', 'display': 'none'})

missing_value_tooltip = html.Div(
    [
        dbc.Tooltip("Missing values are the data points in the dataset which either do not contain any value or "
                    "contains a value which represents no value.", target="missing-value-button"),
        dbc.Tooltip("Click this button to find and highlight rows with missing values.", target="check-missing-value-button"),
        dbc.Tooltip(
            "Click this button to view the changes in the dataset, this will not have any affect on the actual dataset.",
            target="apply_btn"),
        dbc.Tooltip("Clicking this button will only undo any temporary changes done to the dataset in this stage.",
                    target="cancel_btn"),
        dbc.Tooltip("Once this button is clicked the data will be permanently updated and cannot be recovered.",
                    target="update_missing_col")
    ],
)

missing_value_collapse = html.Div(
    [missing_value_tooltip,
        dbc.Button(
            "Missing Values",
            id="missing-value-button",
            className="mb-3", disabled=True,
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
                             placeholder='Select an Action for Missing Values', style=dict(
                        width='100%',
                        verticalAlign="middle")), breakline,
                dcc.Dropdown(id="missing-value-fill-strategy-dropdown", multi=False,
                             placeholder='Select a strategy to Impute', style={
                        'width': '100%', 'display': 'none'}), breakline,
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
                            id='apply_col', style={'width': 'auto', 'display': 'none'}),
                        dbc.Col([
                            dbc.Button(
                                "REVERT",
                                id="cancel_btn", color='danger',
                                className="mb-3", n_clicks=0,
                                outline=True,
                                style={'width': '100%'})
                        ], id='cancel_col', style={'width': 'auto', 'display': 'none'}),
                        dbc.Col(update_dataset_button_missing, id='update_missing_col', style={'width': 'auto'}),
                    ],
                    id='apply_or_cancel', style={'display': 'block'}), breakline,
            ])),
            id="missing_value_collapse",
        ), breakline
    ], style={'width': '100%'}
)

update_dataset_button_columns = dbc.Button(
    "UPDATE DATASET",
    id="update_dataset_btn_columns", color='danger',
    className="mb-3", n_clicks=0,
    outline=True, block=True,
    style={'width': '100%', 'display': 'none'})


duplicate_column_tooltip = html.Div(
    [
        dbc.Tooltip("Duplicate columns in the datatset are the columns which have the same name and the same values "
                    "and must be removed since they do not contribute to better accuracy..",
                    target="duplicate-columns-button"),
        dbc.Tooltip("Click this button to find and highlight duplicate columns.",
                    target="find-duplicate-columns"),
        dbc.Tooltip(
            "Click this button to view the changes in the dataset, this will not have any affect on the actual dataset.",
            target="column_apply_btn"),
        dbc.Tooltip("Clicking this button will only undo any temporary changes done to the dataset in this stage.",
                    target="column_cancel_btn"),
        dbc.Tooltip("Once this button is clicked the data will be permanently updated and cannot be recovered.",
                    target="update_dataset_btn_columns")
    ],
)

duplicate_column_collapse = html.Div(
    [duplicate_column_tooltip,
        dbc.Button(
            "Duplicate Columns",
            id="duplicate-columns-button",
            className="mb-3", disabled=True,
            color='primary', style={'width': '100%'}
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([breakline,
                                   dbc.Button(
                                       "Find Duplicate columns",
                                       id="find-duplicate-columns", outline=True,
                                       className="mb-3", n_clicks=0,
                                       color='success', style={'width': '100%'}
                                   ), breakline,
                                   html.Div(
                                       [
                                           dbc.Col(
                                               [
                                                   dbc.Button(
                                                       "REMOVE DUPLICATE COLUMNS",
                                                       id="column_apply_btn", color='success',
                                                       outline=True,
                                                       className="mb-3", n_clicks=0,
                                                       style={'width': '100%'})
                                               ],
                                               id='column_apply_col', style={'width': 'auto', 'display': 'none'}),
                                           html.Div(id='duplicate_column_pos', style={'display': 'none'}),
                                           dbc.Col([
                                               dbc.Button(
                                                   "REVERT",
                                                   id="column_cancel_btn", color='danger',
                                                   className="mb-3", n_clicks=0,
                                                   outline=True,
                                                   style={'width': '100%'})
                                           ], id='column_cancel_col', style={'width': 'auto', 'display': 'none'}),
                                           dbc.Col(update_dataset_button_columns, id='update_column_col',
                                                   style={'width': 'auto'}),

                                       ],
                                       id='column_apply_or_cancel', style={'display': 'block'})])),
            id="duplicate_columns_collapse",
        ), breakline
    ], style={'width': '100%'}
)

update_dataset_button_rows = dbc.Button(
    "UPDATE DATASET",
    id="update_dataset_btn_rows", color='danger',
    className="mb-3", n_clicks=0,
    outline=True, block=True,
    style={'width': '100%', 'display': 'none'})

duplicate_rows_tooltip = html.Div(
    [
        dbc.Tooltip("Duplicate Rows are the rows which have the same value for all the columns and may or may not "
                    "contribute to improved accuracy.", target="duplicate-rows-button"),
        dbc.Tooltip("Click this button to find and highlight duplicate rows.",
                    target="find-duplicate-rows"),
        dbc.Tooltip(
            "Click this button to view the changes in the dataset, this will not have any affect on the actual dataset.",
            target="row_apply_btn"),
        dbc.Tooltip("Clicking this button will only undo any temporary changes done to the dataset in this stage.",
                    target="row_cancel_btn"),
        dbc.Tooltip("Once this button is clicked the data will be permanently updated and cannot be recovered.",
                    target="update_dataset_btn_rows")

    ],
)

duplicate_rows_collapse = html.Div(
    [duplicate_rows_tooltip,
        dbc.Button(
            "Duplicate Rows",
            id="duplicate-rows-button",
            className="mb-3", disabled=True,
            color='primary', style={'width': '100%'}
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([breakline,
                                   dbc.Button(
                                       "Find Duplicate rows",
                                       id="find-duplicate-rows",
                                       className="mb-3", n_clicks=0, outline=True,
                                       color='success', style={'width': '100%'}
                                   ), breakline,
                                   html.Div(
                                       [
                                           dbc.Col(
                                               [
                                                   dbc.Button(
                                                       "REMOVE DUPLICATE ROWS",
                                                       id="row_apply_btn", color='success',
                                                       outline=True,
                                                       className="mb-3", n_clicks=0,
                                                       style={'width': '100%'})
                                               ],
                                               id='row_apply_col', style={'width': 'auto', 'display': 'none'}),
                                           dbc.Col([
                                               dbc.Button(
                                                   "REVERT",
                                                   id="row_cancel_btn", color='danger',
                                                   className="mb-3", n_clicks=0,
                                                   outline=True,
                                                   style={'width': '100%'})
                                           ], id='row_cancel_col', style={'width': 'auto', 'display': 'none'}),
                                           dbc.Col(update_dataset_button_rows, id='update_row_col',
                                                   style={'width': 'auto'}),
                                       ],
                                       id='row_apply_or_cancel', style={'display': 'block'}),
                                   ])),
            id="duplicate_rows_collapse",
        ), breakline,
    ], style={'width': '100%'}
)

finish_preprocessing_tooltip = html.Div(
    [
        dbc.Tooltip("Clicking this button will ignore any step where update dataset button is not clicked and move to "
                    "the feature selection stage.", target="finish-preprocessing-button",)])

finish_preprocessing_button = dbc.Button(
    "FINISH PREPROCESSING",
    id="finish-preprocessing-button",
    className="mb-3",
    color='success', style={'width': '100%'}
),

# Datatable to show the dataset to the user
dataset_table = dash_table.DataTable(id='table1', css=[{'selector': '.row', 'rule': 'margin: 0'},
                                                       {"selector": ".show-hide", "rule": "display: none"},
                                                       {"selector": "input.current-page", "rule": "width: 30%"}],
                                     columns=[{"name": i, "id": i} for i in df],
                                     data=df.to_dict('records'),
                                     page_size=12,
                                     page_action="native",
                                     page_current=0,
                                     style_table={'overflowX': 'auto', 'display': 'block'})

# Cardbody component to compile all preprocessing elements into single component
preprocess_flow = [
    dbc.CardBody(
        [
            dbc.Row(html.Div("Preprocessing Steps")),
            dbc.Row(dbc.CardBody([finish_preprocessing_tooltip,
                dbc.Row(breakline),
                dbc.Row(missing_value_collapse),
                dbc.Row(duplicate_column_collapse),
                dbc.Row(duplicate_rows_collapse),
                dbc.Row(finish_preprocessing_button)
            ])
            ),
        ])]

# Cardbody component to compile dataset upload and view into single component
dataset_input_display = dbc.Card(
    dbc.CardBody(
        [upload_dataset, dataset_table], style={'height': '50rem'}
    ), outline=True, color="info"
)

# Component to show page footer
page_footer = html.Div(children=[breakline, breakline, breakline],
                       style={'width': '100%', 'height': '40%', 'background-color': 'black'})

toast_div = html.Div(id='toast')

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
                                                     style={'padding': '10px 25px 40px', 'height': '50rem',
                                                            'overflowY': 'scroll'}), width=4, align="center"),
                                ]
                            )
                        )
                    ], outline=True, color='success'
                ),
                style={'padding': '10px 40px 20px'}
            )
        ), dbc.Row(toast_div), html.Div(id='linkx'),

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


# callback to take dataset from user and display it in the datatable
@app.callback([Output("table1", "data"),
               Output("table1", "columns"),
               Output("upload-data", "style"),
               Output("table1", "style_data_conditional"),
               Output("table1", "hidden_columns"),
               Output("toast", "children"),
               Output('missing-value-action-dropdown', 'options'),
               Output('missing-value-action-dropdown', 'style'),
               Output('cancel_col', 'style'),
               Output('apply_col', 'style'),
               Output('missing-value-button', 'disabled'),
               Output('duplicate-columns-button', 'disabled'),
               Output('duplicate-rows-button', 'disabled'),
               Output('column_cancel_col', 'style'),
               Output('column_apply_col', 'style'),
               Output('row_cancel_col', 'style'),
               Output('row_apply_col', 'style'),
               Output('duplicate_column_pos', 'children'),
               Output('update_dataset_btn_missing', 'style'),
               Output('update_dataset_btn_columns', 'style'),
               Output('update_dataset_btn_rows', 'style'),
               Output("missing_value_collapse", "is_open"),
               Output("duplicate_columns_collapse", "is_open"),
               Output("duplicate_rows_collapse", "is_open"),
               Output("placeholders", "options"),
               Output("placeholders", "value"),
               Output("missing-value-fill-strategy-dropdown", "options"),
               Output("missing-value-fill-strategy-dropdown", "style"),
               Output('missing-value-action-dropdown', 'disabled'),
               Output("missing-value-fill-strategy-dropdown", "disabled"),
               Output('table1','page_current')],
              [Input('upload-data', 'contents'),
               Input('check-missing-value-button', 'n_clicks'),
               Input('apply_btn', 'n_clicks'),
               Input('cancel_btn', 'n_clicks'),
               Input('find-duplicate-columns', 'n_clicks'),
               Input('find-duplicate-rows', 'n_clicks'),
               Input('column_cancel_btn', 'n_clicks'),
               Input('column_apply_btn', 'n_clicks'),
               Input('row_cancel_btn', 'n_clicks'),
               Input('row_apply_btn', 'n_clicks'),
               Input('update_dataset_btn_missing', 'n_clicks'),
               Input('update_dataset_btn_columns', 'n_clicks'),
               Input('update_dataset_btn_rows', 'n_clicks'),
               Input("missing-value-button", "n_clicks"),
               Input("duplicate-columns-button", "n_clicks"),
               Input("duplicate-rows-button", "n_clicks"),
               Input('missing-value-action-dropdown', 'value'),
               Input("missing-value-fill-strategy-dropdown", "value")],
              [State('upload-data', 'filename'),
               State('placeholders', 'value'),
               State("table1", "data"),
               State('duplicate_column_pos', 'children'),
               State("missing_value_collapse", "is_open"),
               State("duplicate_columns_collapse", "is_open"),
               State("duplicate_rows_collapse", "is_open")])
def update_output(content, missing_clicks, apply_click, cancel_click, column_clicks, row_clicks, column_cancel_click,
                  column_apply_click, row_cancel_click, row_apply_click, update_missing, update_columns, update_rows,
                  n1, n2, n3, missing_action, strategy, name, value, datatableData, duplicate_col_pos, is_open1,
                  is_open2, is_open3):
    component_clicked_id = ""
    if hasattr(project,'dataset'):
        missing_values_identifier = project.dataset.identifier + 'missing-values'
        duplicate_rows_identifier = project.dataset.identifier + 'duplicate-rows'
    ctx = dash.callback_context
    if not ctx.triggered:
        print(len(ctx.outputs_list))
        raise PreventUpdate
    else:
        component_clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]
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
                   'display': 'none'}, {'display': 'none'}, {
                   'display': 'block'}, True, True, True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 0

    if component_clicked_id == "missing-value-button" and n1:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, not is_open1, False, False, [
            {"label": placeholder, "value": placeholder} for placeholder in
            placeholders], no_update, no_update, no_update, no_update, no_update, no_update
    elif component_clicked_id == "duplicate-columns-button" and n2:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, not is_open2, False, no_update, no_update, no_update, no_update, no_update, no_update,no_update
    elif component_clicked_id == "duplicate-rows-button" and n3:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, False, not is_open3, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "check-missing-value-button":
        if value is not None:
            df = pd.DataFrame(datatableData)
            if duplicate_rows_identifier in df.columns:
                df.drop(columns=duplicate_rows_identifier, inplace=True)
            df[missing_values_identifier] = project.dataset.missing_value_indicator(value)
            style_data_conditional = [{
                'if': {'filter_query': '{'+ missing_values_identifier +'} eq "true"'},
                'backgroundColor': '#3D9970',
                'color': 'white'
            }]
            if 'true' not in df[missing_values_identifier].to_list():
                return df.to_dict('records'), \
                       [{"name": i, "id": i} for i in df.columns], \
                       {'display': 'none'}, style_data_conditional, [missing_values_identifier], \
                       construct_toast("Dataset Info",
                                       "Found 0 missing values.",
                                       "danger"), \
                       [{"label": action, "value": action} for action in missing_value_actions], \
                       {'width': '100%', 'display': "none"}, {'display': 'none'}, {
                           'display': 'none'}, False, False, False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

            return df.to_dict('records'), \
                   [{"name": i, "id": i} for i in df.columns], \
                   {'display': 'none'}, style_data_conditional, [missing_values_identifier], \
                   construct_toast("Dataset Info",
                                   "Found {} missing values.\nRows with missing values are highlighted.".format(
                                       len(df[df[missing_values_identifier] == "true"].index)),
                                   "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}, {'display': 'none'}, {
                       'display': 'none'}, False, False, False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "missing-value-fill-strategy-dropdown":
        return no_update, no_update, no_update, no_update, no_update, no_update, \
               no_update, no_update, {'display': 'none'}, {'display': 'block'}, no_update, no_update, no_update, \
               no_update, no_update, no_update, no_update, no_update, {'display': 'none'}, \
               no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
               no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "missing-value-action-dropdown":
        if missing_action == missing_value_actions[0]:
            return no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, {'display': 'none'}, {'display': 'block'}, no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, {'display': 'none'}, \
                   no_update, no_update, no_update, no_update, no_update, no_update, no_update, [], {
                       'display': 'none'}, no_update, no_update, no_update

        elif missing_action == missing_value_actions[1]:
            return no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, {'display': 'none'}, {'display': 'none'}, no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, {'display': 'none'}, \
                   no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   [{"label": strategyx, "value": strategyx} for strategyx in missing_value_fill_strategy], \
                   {'display': 'block'}, no_update, no_update, no_update

    if component_clicked_id == "apply_btn":
        if missing_action == missing_value_actions[0]:
            df1 = pd.DataFrame(datatableData)
            df1[missing_values_identifier] = project.dataset.missing_value_indicator(value)
            df = df1[df1[missing_values_identifier] == "false"]
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, [missing_values_identifier], construct_toast("Missing rows delete",
                                                                              "Deleted {} rows with missing values.".format(
                                                                                  len(df1[df1[
                                                                                              missing_values_identifier] == "true"].index)),
                                                                              "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}, {'display': 'block'}, {'display': 'none'}, False, True, True, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, no_update, 0
        elif missing_action == missing_value_actions[1]:
            # functionality based on 'strategy', 'value' here

            df = pd.DataFrame(datatableData)
            if missing_values_identifier in df.columns:
                df.drop(columns=missing_values_identifier, inplace=True)
            df = project.dataset.missing_value_imputer(df, value, strategy)
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, no_update, construct_toast("Missing rows delete",
                                                                     "Imputing missing values.",
                                                                     "danger"), \
                   no_update, \
                   {'width': '100%', 'display': "block"}, {'display': 'block'}, {'display': 'none'}, False, True, True, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, True, 0

    if component_clicked_id == "cancel_btn":
        if missing_action == missing_value_actions[0]:
            df = pd.DataFrame(project.dataset.df.copy())
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                "Restored rows with missing values.",
                                                                "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}, {'display': 'none'}, {
                       'display': 'block'}, False, False, False, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, no_update, no_update
        elif missing_action == missing_value_actions[1]:
            df = pd.DataFrame(project.dataset.df.copy())
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                "Restored rows with missing values.",
                                                                "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "block"}, {'display': 'none'}, {
                       'display': 'block'}, False, False, False, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, False, no_update

    if component_clicked_id == "update_dataset_btn_missing":
        if missing_action == missing_value_actions[0]:
            df = pd.DataFrame(datatableData)
            if missing_values_identifier in df.columns:
                df.drop(columns=missing_values_identifier, inplace=True)
            if duplicate_rows_identifier in df.columns:
                df.drop(columns=duplicate_rows_identifier, inplace=True)
            project.dataset.df = df.copy()
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                "DATASET UPDATED. Removed all the rows with missing values.",
                                                                "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "none"}, {'display': 'none'}, {'display': 'none'}, False, False, False, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, no_update, no_update, not is_open1, not is_open2, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, False, no_update, no_update
        elif missing_action == missing_value_actions[1]:
            df = pd.DataFrame(datatableData)
            if missing_values_identifier in df.columns:
                df.drop(columns=missing_values_identifier, inplace=True)
            if duplicate_rows_identifier in df.columns:
                df.drop(columns=duplicate_rows_identifier, inplace=True)
            project.dataset.df = df.copy()
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, None, construct_toast("Missing rows delete",
                                                                "DATASET UPDATED. Removed all the rows with missing values.",
                                                                "danger"), \
                   [{"label": action, "value": action} for action in missing_value_actions], \
                   {'width': '100%', 'display': "none"}, {'display': 'none'}, {'display': 'none'}, False, False, False, \
                   no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, no_update, no_update, not is_open1, not is_open2, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, False, False, no_update

    if component_clicked_id == "find-duplicate-columns":
        # perform operations to determine duplicate columns and highlight them in the table
        df = pd.DataFrame(datatableData)
        if missing_values_identifier in df.columns:
            df.drop(columns=missing_values_identifier, inplace=True)
        if duplicate_rows_identifier in df.columns:
            df.drop(columns=duplicate_rows_identifier, inplace=True)

        statusx, positions = project.dataset.duplicate_column_check(df)
        if statusx:
            style_data_conditional = [{'if': {'column_id': df.columns[i]}, 'backgroundColor': 'pink'} for i in
                                      positions]
            toast = construct_toast("Duplicate Column info",
                                    "Found {} Duplicate Columns.".format(len(positions)),
                                    "danger")
            cancel_col_style = {'display': 'none'}
            apply_col_style = {'display': 'block'}

        else:
            style_data_conditional = None
            toast = construct_toast("Duplicate Column Info",
                                    "No Duplicate Columns found.",
                                    "info")
            cancel_col_style = {'display': 'none'}
            apply_col_style = {'display': 'none'}

        return no_update, no_update, no_update, style_data_conditional, no_update, toast, no_update, no_update, no_update, \
               no_update, no_update, no_update, no_update, cancel_col_style, apply_col_style, no_update, no_update, \
               positions, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "column_apply_btn":
        df = pd.DataFrame(datatableData)
        df.drop(df.columns[duplicate_col_pos], axis=1, inplace=True)
        toast = construct_toast("Duplicate Column Info",
                                "Removed duplicate columns.",
                                "danger")
        # update header
        return df.to_dict('record'), \
               [{"name": i, "id": i} for i in df.columns], \
               no_update, no_update, no_update, toast, no_update, no_update, no_update, no_update, True, False, True, {
                   'display': 'block'}, {'display': 'none'}, no_update, no_update, no_update, no_update, {
                   'display': 'block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 0

    if component_clicked_id == "column_cancel_btn":
        df = project.dataset.df.copy()
        toast = construct_toast("Duplicate Column Info",
                                "Restored the duplicate columns.",
                                "danger")
        return df.to_dict('record'), \
               [{"name": i, "id": i} for i in df.columns], \
               no_update, no_update, no_update, toast, no_update, no_update, no_update, no_update, False, False, False, {
                   'display': 'none'}, {'display': 'block'}, no_update, no_update, no_update, no_update, {
                   'display': 'none'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "update_dataset_btn_columns":
        df = pd.DataFrame(datatableData)
        project.dataset.df = df.copy()
        project.dataset.header = pd.Series(df.columns)
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
            'display': 'none'}, None, None, construct_toast("Duplicate column delete",
                                                            "DATASET UPDATED. Removed all the duplicate columns.",
                                                            "danger"), \
               [{"label": action, "value": action} for action in missing_value_actions], \
               {'width': '100%', 'display': "none"}, {'display': 'none'}, {'display': 'none'}, False, False, False, \
               {'display': 'none'}, {'display': 'none'}, no_update, no_update, no_update, \
               {'display': 'none'}, {
                   'display': 'none'}, no_update, no_update, not is_open2, not is_open3, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "find-duplicate-rows":
        # perform operations to determine duplicate rows and highlight them in the table
        df = pd.DataFrame(datatableData)
        if missing_values_identifier in df.columns:
            df.drop(columns=missing_values_identifier, inplace=True)
        if duplicate_rows_identifier in df.columns:
            df.drop(columns=duplicate_rows_identifier, inplace=True)
        df[duplicate_rows_identifier] = project.dataset.duplicate_rows_check(df)
        style_data_conditional = [{
            'if': {'filter_query': '{' + duplicate_rows_identifier + '} eq "True"'},
            'backgroundColor': '#3D9970',
            'color': 'white'
        }]
        if 'True' not in df[duplicate_rows_identifier].to_list():
            Toast = construct_toast("Duplicate rows info",
                                    "No Duplicate Rows Found.",
                                    "info")
            return df.to_dict('record'), \
                   [{"name": i, "id": i} for i in df.columns], \
                   no_update, style_data_conditional, [
                       duplicate_rows_identifier], Toast, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, {
                       'display': 'none'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

        else:
            Toast = construct_toast("Duplicate rows Found",
                                    "Duplicate Rows are highlighted.",
                                    "danger")

            return df.to_dict('record'), \
                   [{"name": i, "id": i} for i in df.columns], \
                   no_update, style_data_conditional, [
                       duplicate_rows_identifier], Toast, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, {
                       'display': 'none'}, {
                       'display': 'block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "row_apply_btn":
        df = pd.DataFrame(datatableData)
        df[duplicate_rows_identifier] = project.dataset.duplicate_rows_check(df)
        df = df.drop(columns=duplicate_rows_identifier).drop_duplicates()
        return df.to_dict('record'), \
               [{"name": i, "id": i} for i in df.columns], \
               no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, True, False, no_update, no_update, {
                   'display': 'block'}, {'display': 'none'}, no_update, no_update, no_update, {
                   'display': 'block'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 0

    if component_clicked_id == "row_cancel_btn":
        df = project.dataset.df.copy()
        return df.to_dict('record'), \
               [{"name": i, "id": i} for i in df.columns], \
               no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, False, False, no_update, no_update, {
                   'display': 'none'}, {'display': 'block'}, no_update, no_update, no_update, {
                   'display': 'none'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    if component_clicked_id == "update_dataset_btn_rows":
        df = pd.DataFrame(datatableData)
        if missing_values_identifier in df.columns:
            df.drop(columns=missing_values_identifier, inplace=True)
        if duplicate_rows_identifier in df.columns:
            df.drop(columns=duplicate_rows_identifier, inplace=True)
        project.dataset.df = df.copy()
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
            'display': 'none'}, None, None, construct_toast("Duplicate rows delete",
                                                            "DATASET UPDATED. Removed all the duplicate rows.",
                                                            "danger"), \
               [{"label": action, "value": action} for action in missing_value_actions], \
               {'width': '100%', 'display': "none"}, {'display': 'none'}, {'display': 'none'}, False, False, False, \
               no_update, no_update, {'display': 'none'}, {'display': 'none'}, no_update, {
                   'display': 'none'}, no_update, {
                   'display': 'none'}, no_update, no_update, not is_open3, no_update, no_update, no_update, no_update, no_update, no_update, 0

    if component_clicked_id == "upload-data":
        project.upload_dataset(content, name),
        df = project.dataset.df.copy()
        df_info = project.dataset.info()
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
            'display': 'none'}, None, None, construct_toast("Dataset Info",
                                                            "Dataset has been uploaded.\n {}".format(df_info),
                                                            "info"), [], {'display': 'none'}, {'display': 'none'}, {
                   'display': 'none'}, False, False, False, {'display': 'none'}, {'display': 'none'}, {
                   'display': 'none'}, {'display': 'none'}, no_update, {'display': 'none'}, {'display': 'none'}, {
                   'display': 'none'}, False, False, False, no_update, [], no_update, no_update, no_update, no_update, no_update
    else:
        df = pd.DataFrame()
        if hasattr(project, 'dataset'):
            df = project.dataset.df.copy()
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {
                'display': 'none'}, None, None, None, [], {'display': 'none'}, {'display': 'none'}, {
                       'display': 'block'}, False, False, False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, False, False, no_update, [], no_update, no_update, no_update, no_update, no_update

        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {'display': 'block',
                                                                                   'vertical-align': 'middle',
                                                                                   'width': '100%', 'height': '470px',
                                                                                   'lineHeight': '20px',
                                                                                   'textAlign': 'center'}, None, None, None, [], {
                   'display': 'none'}, {'display': 'none'}, {
                   'display': 'block'}, True, True, True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, False, False, False, no_update, [], no_update, no_update, no_update, no_update, no_update


@app.callback(Output('linkx', 'children'),
              [Input('finish-preprocessing-button', 'n_clicks')])
def finish_preprocessing(click):
    if click is not None and click > 0:
        return dcc.Location(pathname="/model", id="someid_doesnt_matter")
    else:
        raise PreventUpdate


placeholders = ['', '.', '?', '-1']
missing_value_actions = ['Remove Rows With Missing Values', 'Fill Missing Values']
missing_value_fill_strategy = ['mean', 'median', 'most_frequent', 'constant']
duplicate_column_options = ['Find based on Column names', 'Find based on Column values']
