import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app,project

# Project name input modal
modal = dbc.Modal(
    [
        dbc.ModalHeader("Project Name"),
        dbc.ModalBody([dbc.Input(id='project_name_input',placeholder="Enter Project Name", debounce=True),
                       ]),
        dbc.ModalFooter(
            [dbc.Button("Cancel", id="close", className="ml-auto"),
             dbc.Button("Create Project",href='/preprocess',
                        id="create_project_btnx", className="ml-auto", n_clicks=0)]),
    ],
    id="project_info_modal",
)

# component to compile all the elements into single element
layout = html.Div(
    [
        dbc.Col(
            [
                dbc.Row(html.H1("IMLP", style={'align': 'center','width':'100%'})),
                dbc.Row(html.H2("This is a Interactive Machine Learning"
                                    "Platform", id='project_description',
                                    style={'align': 'center','width':'100%'})),
                dbc.Row(html.Button("Create Project",
                                        id='create_project_btn',
                                        style={'align': 'center','width':'100%'}, n_clicks=0)),
                html.Br(),
                dbc.Row(html.Button("Open Exisiting Project",
                                        id='open_project_btn',
                                        style={'align': 'center','width':'100%'})),
                dbc.Row(modal)],style={'padding': '10px 55px 20px','align':'center','width':'100%'}),
    ])


# Open the Modal and takes project name input
@app.callback(Output('project_info_modal', 'is_open'),
              [Input('create_project_btn', 'n_clicks')])
def create_project(n_click):
    if n_click > 0:
        return True


# Takes the project name from the modal input and makes instance of Project
@app.callback(Output('project_name_input', 'invalid'),
              [Input('create_project_btnx', 'n_clicks'),Input('project_name_input', 'value')])
def project_name_in(n_clicks, project_name):
    if n_clicks > 0:
        # project name validation. If fails, shows a valid or invalid remark on the component
        if project_name is None or len(project_name)==0:
            return True
        else:
            project.create(project_name)
            return False
