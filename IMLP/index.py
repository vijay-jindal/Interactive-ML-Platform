import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import homepage, preprocess, eda

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
# TODO: check for project instance if it exists at each endpoint using getattr or hasattr
def display_page(pathname):
    if pathname == '/':
        return homepage.layout
    elif pathname == '/preprocess':
        return preprocess.layout
    elif pathname == '/eda':
        return eda.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
