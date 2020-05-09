from app import app, project
import dash_html_components as html
from dash.dependencies import Input, Output, State

layout = [html.Div(id='test')]

@app.callback(Output('test','children'),
              [Input('test','style')])
def testx(l):
    return html.Label(f"{project.model.test_size}")