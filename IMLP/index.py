import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, project
from apps import homepage, preprocess, eda, model

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
# TODO: check for project instance if it exists at each endpoint using getattr or hasattr
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
        if hasattr(project,'model'):
            return model.layout
        else:
            return dcc.Location(pathname="/",id='redirect')
    else:
        return dcc.Location(pathname="/", id='redirect')


if __name__ == '__main__':
    app.run_server(debug=False)
