import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
from app import app, project
import traceback
from dash.exceptions import PreventUpdate
from dash import no_update

from numpy import unique

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

# gif to show training info
gif = html.Div("TRAINING RESULTS SHOWN HERE...", id='gif', style={'padding': '10px 30px 10px'})
datatable = html.Div(id='tablex', style={'padding': '10px 30px 10px'})
x_axis_dropdown = dcc.Dropdown(id='x_axis', searchable=False, placeholder="Select the X-Axis",
                                       style=dict(
                                           width='100%',
                                           verticalAlign="middle"
                                       ))
y_axis_dropdown = dcc.Dropdown(id='y_axis', searchable=False, placeholder="Select the Y-Axis",
                                       style=dict(
                                           width='100%',
                                           verticalAlign="middle"
                                       ))

clustering_graph = dcc.Graph(id='cluster-plot',style={'width':'100%','height':'50rem'})

clustering_graph_div = html.Div(children=[x_axis_dropdown, y_axis_dropdown, clustering_graph],id='clustering_graph_div',style={'display':'none'})

#
# Cardbody component to compile dataset upload and view into single component
gif_display = dbc.Card(
    dbc.CardBody(
        [gif,datatable,breakline,clustering_graph_div], style={'height': '57rem'}
    ), outline=True, color="info",style={'padding': '10px 25px 40px', 'height': '57rem','overflowY': 'scroll'}

)

start_training_btn = dbc.Button("Start Training", id='start_training', n_clicks=0, color='success',
                                style={'width': '100%'})
algorithm_name = html.Div(id='algorithm_name_info')
split_ratio = html.Div(id='split_ratio_info')
feature_columns = html.Div(id='feature_columns_info')
target_column = html.Div(id='target_column_info')

hyperparameter_header = dbc.Card([dbc.CardHeader("Model Details"),
                                  dbc.CardBody([
                                      dbc.Row(algorithm_name, style={'padding': '10px'}),
                                      dbc.Row(split_ratio, style={'padding': '10px'}),
                                      dbc.Row(feature_columns, style={'padding': '10px'}),
                                      dbc.Row(target_column, style={'padding': '10px'}),
                                      dbc.Row(html.Button('Edit', id='edit', n_clicks=0), justify="center")
                                  ])],
                                 color='info',
                                 outline=True,
                                 id='parameter_details_card',
                                 )

hyperparameters = html.Div(id='hyperparameters_div', style={'text-aling': 'center'})

hyperparameters_card = dbc.Card([dbc.CardHeader("Configure Hyperparameters"),
                                 dbc.CardBody([hyperparameters, html.Br(), start_training_btn],
                                              style={'padding': '10px 10px 10px'})],
                                color='info', outline=True)

display_contents = html.Div(children=[hyperparameter_header, html.Br(), hyperparameters_card, html.Br()])

# Component to show page footer
page_footer = html.Div(children=[breakline, breakline, breakline],
                       style={'width': '100%', 'height': '40%', 'background-color': 'black'})

learning_type_tooltip = html.Div(
    [
        html.A(href='https://scikit-learn.org/stable/user_guide.html',target="_blank",className="fas fa-question-circle fa-lg", id="learning_type_tooltip"),
        dbc.Tooltip("There are two types of learning. Supervised learning requires labelled dataset whereas "
                    "Unsupervised learning uses unlabelled dataset and performs clustering.",
                    target="learning_type_tooltip"),
    ])

algorithm_name_tooltip = html.Div(
    [
        html.A(href='https://scikit-learn.org/stable/user_guide.html',target="_blank",className="fas fa-question-circle fa-lg", id="algorithm_name_tooltip"),
        dbc.Tooltip("Various algorithms work differently and give different accuracy. Try them and find out which one "
                    "suits your requirement.", target="algorithm_name_tooltip"),
    ])

feature_columns_tooltip = html.Div(
    [
        html.A(href='https://scikit-learn.org/stable/glossary.html',target="_blank",className="fas fa-question-circle fa-lg", id="feature_columns_tooltip"),
        dbc.Tooltip("Select all the columns that you want the Algorithm to use for training", target="feature_columns_tooltip"),
    ])

target_column_tooltip = html.Div(
    [
        html.A(href='https://scikit-learn.org/stable/glossary.html',target="_blank",className="fas fa-question-circle fa-lg", id="target_column_tooltip"),
        dbc.Tooltip("Select the column name that you want to the model to predict after training.", target="target_column_tooltip"),
    ])

split_ratio_tooltip = html.Div(
    [
        html.A(href='https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html',target="_blank",className="fas fa-question-circle fa-lg", id="split_ratio_tooltip"),
        dbc.Tooltip("This is the ratio in which the dataset will be divided into training and testing data.", target="split_ratio_tooltip"),
    ])

# dropdown to take input of learning type
learning_type_dropdown = dcc.Dropdown(id='learning_type', searchable=False, placeholder="Select the Learning type",
                                      style=dict(
                                          width='100%',
                                      ))
# dropdown to take input of algorithm name
algorithm_type_dropdown = html.Div(dcc.Dropdown(id='algorithm_name', searchable=False, placeholder="Select the Algorithm",
                                       style=dict(
                                           width='100%',
                                           verticalAlign="middle"
                                       )),
                                   id='algorithm-type-div',
                                   style=dict(
                                       width='100%',
                                       verticalAlign="middle"
                                   ))
# Label to tell user to select split ratio
split_ratio_label = html.Label('Select the Split Ratio',
                               style=dict(
                                   width='100%',
                                   verticalAlign="middle"
                               ))
# Slider to select the percentage of test sata
split_ratio_slider = html.Div(dcc.Slider(id='split_ratio', min=0, max=100, step=5, value=20),
                              style={'height': '10px', 'width': '100%'},id='split-ratio-div'),
# Div to show the train and test percentage
split_ratio_value = html.Div(id='split_ratio_value', style=dict(
    width='100%',
    verticalAlign="middle", textAlign="center"
))

# dropdown to select features
features_dropdown = dcc.Dropdown(id="feature_column", multi=True, placeholder='Select Feature Columns', style=dict(
    width='100%',
    verticalAlign="middle"))

# dropdown to select target feature
target_dropdown = dcc.Dropdown(id='target_column', searchable=False, placeholder="Select the Target Column", style=dict(
    width='100%',
    verticalAlign="middle"
))

confirm_algorithm_btn = dbc.Button(
    "CONFIRM DETAILS",
    id="confirm-details-button",
    className="mb-3",
    color='success', style={'width': '100%'}
),

# Tabs to do perform various preprocessing steps independently by the user
model_page_contents = html.Div(children=[
    dbc.CardBody(
        [
            dbc.Row(breakline),
            dbc.Row([dbc.Col(learning_type_dropdown, width=10),dbc.Col(learning_type_tooltip, width=2)]),
            dbc.Row(breakline),
            dbc.Row([dbc.Col(algorithm_type_dropdown, width=10), dbc.Col(algorithm_name_tooltip, width=2)]),
            dbc.Row(breakline),
            dbc.Row([dbc.Col(features_dropdown, width=10), dbc.Col(feature_columns_tooltip, width=2)]),
            dbc.Row(breakline),
            dbc.Row([dbc.Col(target_dropdown, width=10), dbc.Col(target_column_tooltip, width=2)]),
            dbc.Row(breakline),
            dbc.Row([dbc.Col(split_ratio_label, width=10)]),
            dbc.Row([dbc.Col(split_ratio_slider, width=10), dbc.Col(split_ratio_tooltip, width=2)]),
            dbc.Row(breakline),
            dbc.Row([dbc.Col(split_ratio_value, width=10)]),
            dbc.Row(breakline),
            dbc.Row(confirm_algorithm_btn)
        ], id='algorithm_select_display', style={'display': 'block'}),
    dbc.CardBody([display_contents], id='hyperparameter_select_display', style={'display': 'none'}),
    dbc.CardBody(dbc.Row([dbc.Col(dbc.Button("Save Model",id="save_model_btn",n_clicks = 0)),dbc.Col(dcc.Link(dbc.Button("Download Model",n_clicks = 0,disabled=True,id="download_model_btn"), id='download_link', href='', refresh=True))])
    , id='save_download_model',style={'display': 'none'})
], style={
    'height': '80px', 'width': '330px'})

xaxis_dropdown = dcc.Dropdown(id='xaxis')
yaxis_dropdown = dcc.Dropdown(id='yaxis')

# component to compile all the elements into single element
layout = html.Div(
    [
        dbc.Row(navbar),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("MODEL GENERATION AND TRAINING",
                                       style={'font-family': 'Times New Roman', 'font-size': '15px', 'color': 'white',
                                              'background-color': 'green'}),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(gif_display, width=8),
                                    dbc.Col(dbc.Card(model_page_contents, outline=True, color="info",
                                                     style={'padding': '10px 25px 40px', 'height': '57rem',
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


@app.callback(Output('details_collapse', 'is_open'),
              [Input('model-details-btn', 'n_clicks')],
              [State("details_collapse", "is_open")])
def open_details(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output('hyperparamters_collapse', 'is_open'),
              [Input('hyperparameters-details-btn', 'n_clicks')],
              [State("hyperparamters_collapse", "is_open")])
def open_details(n, is_open):
    if n:
        return not is_open
    return is_open


confirm_click = 0


@app.callback([Output('algorithm_name_info', 'children'),
               Output('split_ratio_info', 'children'),
               Output('feature_columns_info', 'children'),
               Output('target_column_info', 'children'),
               Output('hyperparameters_div', 'children'),
               Output('hyperparameter_select_display', 'style'),
               Output('algorithm_select_display', 'style'),
               Output('save_download_model', 'style'),
               Output('start_training', 'children')],
              [Input('confirm-details-button', 'n_clicks'), Input('edit', 'n_clicks')],
              [State('learning_type', 'value'), State('algorithm_name', 'value')
                  , State('split_ratio', 'value'), State('feature_column', 'value'),
               State('target_column', 'value')]
              )
def fill_model_details(confirm_clickx, edit_clickx, learning_type, algorithm_name, split_ratio, feature_column_names,
                       target_column_name):
    global confirm_click

    if confirm_click != confirm_clickx:
        confirm_click = confirm_clickx
        if (None and '') not in [learning_type, algorithm_name, split_ratio, feature_column_names, target_column_name]:
            if learning_type == 'Supervised':
                project.create_model(learning_type,algorithm_name)
                project.dataset.set_features(feature_column_names)
                project.dataset.set_target(target_column_name)
                project.model.set_split_ratio(float(split_ratio / 100))
                hyperparamters_components = create_hyperparameter_fields()
                algo, split, f_col, t_col = display_algorithm_info()
                return algo, split, f_col, t_col, hyperparamters_components, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, "START TRAINING"
        elif (None and '') not in [learning_type, algorithm_name,feature_column_names]:
            if learning_type == 'Unsupervised':
                project.create_model(learning_type,algorithm_name)
                project.dataset.set_features(feature_column_names)
                hyperparamters_components = create_hyperparameter_fields()
                algo, f_col = display_algorithm_info()
                return algo, None, f_col, None, hyperparamters_components, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, "START CLUSTERING"
        else:
            raise PreventUpdate
    else:
        return [], [], [], [], None, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, no_update


def display_algorithm_info():
    if hasattr(project, 'model'):
        if project.model.learning_type == "Supervised":
            a_name = project.model.classifier_name
            s_ratio = project.model.test_size
            f_columns = project.dataset.X
            t_column = project.dataset.y

            algo = dbc.Row([
                dbc.Col(html.B(html.Label("Algorithm :")), width='auto'),
                dbc.Col(dbc.Badge("" + a_name, pill=True, color="primary", className="mr-1"), width='auto')
            ])

            split = dbc.Row([
                dbc.Col(html.B(html.Label("Split Ratio :")), width='auto'),
                dbc.Col(dbc.Badge("" + str(s_ratio), pill=True, color="primary", className="mr-1"), width='auto')
            ])

            feature_badges = []
            for i in f_columns:
                feature_badges.append(dbc.Badge("" + i, pill=True, color="primary", className="mr-1"))

            f_col = dbc.Row([
                dbc.Col(html.B(html.Label("Feature columns :")), width='auto'),
                dbc.Col(feature_badges, width='auto')
            ])

            t_col = dbc.Row([
                dbc.Col(html.B(html.Label("Target Column :")), width='auto'),
                dbc.Col(dbc.Badge("" + t_column.name, pill=True, color="primary", className="mr-1"), width='auto')
            ])

            return [algo], [split], [f_col], [t_col]
        elif project.model.learning_type == "Unsupervised":
            a_name = project.model.clusterer_name
            f_columns = project.dataset.X

            algo = dbc.Row([
            dbc.Col(html.B(html.Label("Algorithm :")), width='auto'),
            dbc.Col(dbc.Badge("" + a_name, pill=True, color="primary", className="mr-1"), width='auto')
            ])

            feature_badges = []
            for i in f_columns:
                feature_badges.append(dbc.Badge("" + i, pill=True, color="primary", className="mr-1"))

            f_col = dbc.Row([
            dbc.Col(html.B(html.Label("Feature columns :")), width='auto'),
            dbc.Col(feature_badges, width='auto')
            ])

            return [algo], [f_col]

def create_hyperparameter_fields():
    if hasattr(project, 'model'):
        children = []
        hyperparameter_list = project.model.get_params()
        for k, v in hyperparameter_list.items():
            target_id = "{}_tooltip".format(k)
            tooltip_message = "{}".format(v['tooltip_message'])
            tooltip = html.Div(
                [
                    html.A(href=v['link'], target="_blank",
                           className="fas fa-question-circle fa-lg", id=target_id),
                    dbc.Tooltip(tooltip_message, target=target_id),
                ],
            )

            children.append(html.Div(
                dbc.Row([dbc.Col(html.Label(k)), dbc.Col(tooltip)], style={'width': '100%', 'padding': '10px'})))
            if 'string' in v['param_values'] and len(v['param_values']['string']) > 0:
                options = [html.Option(i) for i in v['param_values']['string']]
                children.append(
                    dcc.Input(type="text", id={'type': 'hyperparameter', 'name': k}, list=k + '_datalist',
                              value=v['default'], style={'padding': '10px'}),
                )
                children.append(html.Datalist(options, id=k + '_datalist', style={'width': '100%', 'padding': '10px'}))
                children.append(html.Br())
            else:
                children.append(
                    dcc.Input(type="text", id={'type': 'hyperparameter', 'name': k}, value=v['default'],
                              style={'padding': '10px'}),
                )
                children.append(html.Br())

        return children
    else:
        return html.Div("Please Select the algorithm and dataset attributes.")


@app.callback([Output('gif', 'children'),
               Output('tablex', 'children'),
               Output('x_axis', 'options'),
               Output('y_axis','options'),
               Output('cluster-plot','figure'),
               Output('clustering_graph_div','style')],
              [Input('start_training', 'n_clicks'),
               Input('x_axis','value'),
               Input('y_axis','value')],
              [State({'type': 'hyperparameter', 'name': ALL}, 'value'),
               State({'type': 'hyperparameter', 'name': ALL}, 'id')])
def get_values(click,x_axis,y_axis ,values, ids):
    if hasattr(project, 'model'):
        output = []
        if click > 0:
            output_dict = dict()
            for i in range(0, len(values)):
                output_dict[ids[i]['name']] = str(values[i])
            set_params_response = project.model.set_params(output_dict)
            try:
                if set_params_response == 1:
                    if project.model.learning_type == "Supervised":
                        a, b, c = project.model.model_train()
                        print(a, b, c)
                        c.insert(0, 'index', c.index)
                        return [html.B(html.Label("The Accuracy of the Model is " + str(a)))], \
                               dash_table.DataTable(columns=[{"name": i, "id": i} for i in c],
                                                    data=c.to_dict('records'),
                                                    style_cell={'textAlign': 'left'},), no_update,no_update,no_update, {'display':'none'}
                    elif project.model.learning_type == "Unsupervised":
                        labels = project.model.model_train()
                        df = project.dataset.get_features()
                        df['Assigned Cluster'] = labels

                        import plotly.graph_objects as go

                        clusters = unique(df['Assigned Cluster'].to_numpy()) # get clusters from parameters of model
                        fig = go.Figure()

                        if x_axis is not None and y_axis is not None:
                            for cluster in clusters:
                                data = df[df["Assigned Cluster"] == cluster]
                                fig.add_scatter(x=data[x_axis], y=data[y_axis], mode="markers", name=f"C{str(cluster)}")
                            fig.update_layout(title="Clusters", xaxis_title=x_axis, yaxis_title=y_axis)
                        else:
                            for cluster in clusters:
                                data = df[df["Assigned Cluster"] == cluster]
                                fig.add_scatter(x=data[data.columns[0]], y=data[data.columns[1]], mode="markers",
                                                name=f"C{str(cluster)}")
                            fig.update_layout(title="Clusters", xaxis_title=data.columns[0], yaxis_title=data.columns[1])

                        return [html.B(html.Label("Model Fitting Complete"))],dash_table.DataTable(columns=[{"name": i, "id": i} for i in df],
                                         data=df.to_dict('records'),
                                         css=[{'selector': '.row', 'rule': 'margin: 0'},
                                              {"selector": ".show-hide", "rule": "display: none"},
                                              {"selector": "input.current-page", "rule": "width: 50px"}],
                                         page_size=12,
                                         page_action="native",
                                         page_current=0,
                                         style_table={'overflowX': 'auto', 'display': 'block'}),[{'label': i, 'value': i} for i in df],[{'label': i, 'value': i} for i in df], fig, {'display': 'block'}

                else:
                    return html.Label(f"{set_params_response}"), html.Label('.'),no_update,no_update,no_update, {'display':'none'}
            except Exception as e:
                return [html.B(html.Label("Training process failed : " + str(e)))], [], no_update, no_update,no_update, {'display':'none'}
            traceback.print_exc()
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


# Callback to set the learning type and algorithm name options
@app.callback(
    [Output("algorithm_name", "options"), Output("learning_type", "options"), Output("target_column","disabled"), Output("target_column", "value"), Output("split_ratio","disabled")],
    [Input('learning_type', 'value')])
def update_learning_and_algorithm_list(value):
    if value is None or value == "Supervised":
        return [[algorithm for algorithm in algorithms["Supervised"]],
                [{"label": learning_type, "value": learning_type} for learning_type in learning_types], False, None, False]
    elif value == "Unsupervised":
        return [
            [algorithm for algorithm in algorithms[value]],
            [{"label": learning_type, "value": learning_type} for learning_type in learning_types], True, None, True]
    else:
        return [
            [algorithm for algorithm in algorithms[value]],
            [{"label": learning_type, "value": learning_type} for learning_type in learning_types], no_update, no_update, no_update]

# Callback to show the percentage of training and testing data based on the slider movement
@app.callback(
    Output('split_ratio_value', 'children'),
    [Input('split_ratio', 'value'), Input('split_ratio','disabled')])
def update_output(value,state):
    if value is not None and state is False:
        return 'Testing : {}% and Training : {}%'.format(value, 100 - value)
    elif state is True:
        return ''
    else:
        raise PreventUpdate


# Callback to take all columns from the dataset and display it in features dropdown.
# Also, removes the column which is already selected in target dropdown
@app.callback(
    Output("feature_column", "options"),
    [Input("feature_column", "search_value"), Input('target_column', 'value')],
)
def update_options(search_value, value):
    columns = project.dataset.df.columns
    if value is None:
        if (len(columns) == 0):
            return []
        else:
            return [{'label': i, 'value': i} for i in columns]
    else:
        return [{'label': i, 'value': i} for i in columns if i != value]


# Callback to take all columns from the dataset and display it in target dropdown.
# Also, removes the columns which are already selected in features dropdown
@app.callback(
    Output("target_column", "options"),
    [Input('feature_column', 'value'), Input('target_column', 'value')],
)
def update_options(value, target_value):
    columns = project.dataset.df.columns
    target_columns = []
    if value is None:
        if len(columns) == 0:
            return []
        else:
            return [{'label': i, 'value': i} for i in columns]

    for column in columns:
        if column not in value:
            target_columns.append(column)

    return [{'label': i, 'value': i} for i in target_columns]

@app.callback(
    [Output('download_link','href'), Output('download_model_btn','disabled')],
    [Input('save_model_btn','n_clicks')]
)
def save_model(n_clicks):
    if n_clicks > 0 and hasattr(project,'model'):
        project.save_model()
        return "/downloads/{}".format("model-" + project.date_created.strftime("%Y%m%d%H%M%S") + ".sav"),False
    else:
        raise PreventUpdate

# List of learning types
learning_types = ['Supervised', 'Unsupervised']

# Dictionary of algorithms
algorithms = {"Supervised":
    [
        {"label": "Random Forest Classifier", "value": "RF"},
        {"label": "SVM Classifier", "value": "SVM"},
        {"label": "Decision Tree classifier", "value": "DT"},
        {"label": "Naive Bayes classifier", "value": "NB"}
    ],
    "Unsupervised":
        [
            {"label": "K-means Clustering", "value": "KM"},
            {"label": "Mean Shift Clustering", "value": "MS"},
        ]}
