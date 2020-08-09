import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
from app import app,project

# Project name input modal
from dash.exceptions import PreventUpdate

# Header bar
navbar = dbc.NavbarSimple(
    brand="Interactive ML Platform",
    brand_style={'font-size':'25px','textAlign':'center'},
    color="success",
    dark=True, style={
        'width': '100%',
        'height': '15rem',
        'text-size':'20px',
        'verticalAlign': 'middle'
    }
)

modal = dbc.Modal(
    [
        dbc.ModalHeader("Project Name"),
        dbc.ModalBody([dbc.Input(id='project_name_input',
                                 placeholder="Enter Project Name",
                                 autoComplete="off",
                                 bs_size="lg",style={'font-size':'20px'},className="mb-3"),
                       ]),
        dbc.ModalFooter(
            [dcc.Link(dbc.Button("Create Project",disabled=True,
                        id="create_project_btnx", className="ml-auto", n_clicks=0,color='success'), id='link',style={'color':'green'},
                      href='')]),
    ],size="lg",
    id="project_info_modal",
)
breakline = html.Br()
# Component to show page footer
page_footer = html.Div(children=[breakline, breakline, breakline],
                       style={'position': 'fixed','left': 0, 'bottom': 0, 'width': '100%','background-color': 'green'
})

# component to compile all the elements into single element
layout = html.Div(
    [
        dbc.Row(navbar),
        dbc.Col(
            [
                dbc.Row([dbc.Col(),dbc.Col([
                    dbc.Row(breakline),
                    dbc.Row(dbc.Button("Create Project", className="mr-1",
                                       id='create_project_btn', outline=True, color='success', size='lg',
                                       style={'align': 'center', 'width': '100%'}, n_clicks=0)),
                    html.Br(),
                    dbc.Row(dbc.Button("Open Existing Project", className="mr-1",
                                       id='open_project_btn', outline=True, color='success', size='lg',
                                       style={'align': 'center', 'width': '100%'})),

                ], width=7),dbc.Col()]),
                dbc.Row(modal)],style={'padding': '10px 55px 20px','align':'center','width':'100%'}),
                dbc.Row(page_footer)
    ])


# Open the Modal and takes project name input
@app.callback(Output('project_info_modal', 'is_open'),
              [Input('create_project_btn', 'n_clicks')])
def create_project(n_click):
    if n_click > 0:
        return True

@app.callback([Output('project_name_input', 'invalid'),Output('create_project_btnx','disabled'),Output('link','href')],
              [Input('project_name_input','value')])
def project_name(project_name):
    # project name validation. If fails, shows a valid or invalid remark on the component
    if project_name is None:
        raise PreventUpdate
    elif len(project_name) == 0:
        return [],True,''
    else:
        return False,False,'/preprocess'

@app.callback(Output('create_project_btnx','color'),
              [Input('create_project_btnx','n_clicks')],[State('project_name_input','value')])
def create_project(click,project_name):
    if click > 0 and project_name is not None:
        project.create(project_name)
        return 'success'
    else:
        raise PreventUpdate