from app import app, project
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
from app import app, project
import pandas as pd

# few basic styles for tabs component
from dash.exceptions import PreventUpdate

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

# gif to show training info
gif = html.Div("TRAINING HAPENNING...", id='gif')

# Cardbody component to compile dataset upload and view into single component
gif_display = dbc.Card(
    dbc.CardBody(
        [gif], style={'height': '57rem'}
    ), outline=True, color="info"
)
start_training_btn = dbc.Button("Start Training",id='start_training',n_clicks=0,color='success')

hyperparameters = html.Div([start_training_btn], id='hyperparameters_div',)


# Component to show page footer
page_footer = html.Div(children=[breakline, breakline, breakline],
                       style={'width': '100%', 'height': '40%', 'background-color': 'black'})

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
                                    dbc.Col(dbc.Card(hyperparameters, outline=True, color="info",
                                                     style={'padding': '10px 25px 40px', 'height': '57rem',
                                                            'overflowY': 'scroll'}), width=4, align="center"),
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

@app.callback(Output('hyperparameters_div', 'children'),
              [Input('hyperparameters_div', 'style')])
def create_hyperparameter_fields(style):
    children = []
    hyperparameter_list = project.model.get_params()
    for k, v in hyperparameter_list.items():
        children.append(html.Td(k))
        if 'string' in v['param_values'] and len(v['param_values']['string']) > 0:
            options = [html.Option(i) for i in v['param_values']['string']]
            children.append(dcc.Input(type="text",id={'type': 'hyperparameter','name': k }, list=k+'_datalist', value=v['default']))
            children.append(html.Datalist(options, id=k+'_datalist'))
        else:
            children.append(dcc.Input(type="text", id={'type': 'hyperparameter','name': k }, value=v['default']))
    children.append(start_training_btn)
    return children


@app.callback(Output('gif','children'),
              [Input('start_training','n_clicks')],
              [State({'type': 'hyperparameter', 'name': ALL}, 'value'),
               State({'type': 'hyperparameter', 'name': ALL}, 'id')])
def get_values(click, values,ids):
    output =[]
    if click>0:
        output_dict = dict()
        for i in range(0, len(values)):
            output_dict[ids[i]['name']]=str(values[i])
        set_params_response = project.model.set_params(output_dict)
        if set_params_response == 1:
            return html.Label(project.model.model_train())
        else:
            return html.Label(f"{set_params_response}")
        print(output_dict)
    else:
        raise PreventUpdate