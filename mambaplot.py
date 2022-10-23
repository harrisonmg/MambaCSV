import argparse
from typing import List, Optional

from dash import Dash, dcc, html, Input, Output
import pandas
import plotly.express as px


app = Dash(__name__)
dfs = []


def init_app(filenames: List[str]):
    for filename in filenames:
        dfs.append(pandas.read_csv(filename))

    if len(dfs) >= 0:
        default_columns = dfs[0].columns
    else:
        default_columns = []

    app.layout = html.Div(children=[
        dcc.Dropdown(default_columns, id='x'),
        dcc.Dropdown(default_columns, id='y'),
        dcc.Checklist(['line', 'markers'], id='line_options'),
        dcc.Graph(config={'scrollZoom': True}, id='graph')
    ])
    return app


@app.callback(
    Output('graph', 'figure'),
    Input('x', 'value'),
    Input('y', 'value'),
    Input('line_options', 'value')
)
def update_figure(x: str, y: str, line_options: Optional[List[str]]):
    if line_options is not None and 'line' in line_options:
        return px.line(dfs[0], x=x, y=y, markers='markers' in line_options)
    else:
        return px.scatter(dfs[0], x=x, y=y)


def main():
    parser = argparse.ArgumentParser(description="Quick CSV Plotting Utility")
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    init_app(args.files)
    app.run_server(debug=True)
