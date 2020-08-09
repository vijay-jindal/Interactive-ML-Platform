import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

from app import app, project
from apps import homepage, preprocess, eda, model

from dash.exceptions import PreventUpdate

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return homepage.layout
    elif pathname == '/preprocess':
        if hasattr(project, 'name'):
            return preprocess.layout
        else:
            return dcc.Location(pathname="/",id='redirect')
    elif pathname == '/eda':
        if hasattr(project, 'dataset'):
            return eda.layout
        else:
            return dcc.Location(pathname="/",id='redirect')
    elif pathname == '/model':
        if hasattr(project,'dataset'):
            return model.layout
        else:
            return dcc.Location(pathname="/",id='redirect')
    elif pathname is not None and "/downloads/" in pathname:
        raise PreventUpdate
    else:
        return dcc.Location(pathname="/", id='redirect')


if __name__ == '__main__':
    app.run_server(debug=False)
