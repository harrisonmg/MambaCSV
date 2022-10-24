import argparse

from dash import ALL, Dash, dcc, html, MATCH, no_update, Input, Output
import pandas
import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__)
dataframes = {}
series_counter = 0


def create_series_layout(index=None, dataframe_names=None, default_dataframe=None):
    global series_counter
    if index is None:
        index = series_counter
        series_counter += 1

    if dataframe_names is None:
        dataframe_names = []

    if default_dataframe is None:
        columns = []
    else:
        columns = dataframes[default_dataframe].columns

    return html.Div(children=[
        dcc.Dropdown(id={'type': 'series-dataframe', 'index': index},
                     options=dataframe_names, value=default_dataframe),
        dcc.Dropdown(id={'type': 'series-x', 'index': index},
                     options=columns),
        dcc.Dropdown(id={'type': 'series-y', 'index': index},
                     options=columns),
        dcc.Checklist(id={'type': 'series-options', 'index': index},
                      options=['scatter', 'line'], value=['scatter'])
    ])


def init_app(filenames):
    global series_counter
    series_layouts = []
    for i, filename in enumerate(filenames):
        dataframes[filename] = pandas.read_csv(filename)
        series_layouts.append(create_series_layout(series_counter + i, filenames, filename))

    series_counter = i

    app.layout = html.Div(children=[
        html.Div(id='series-div', children=series_layouts),
        dcc.Graph(id='graph', config={'scrollZoom': True})
    ])
    return app


@app.callback(
    Output({'type': 'series-x', 'index': MATCH}, 'options'),
    Output({'type': 'series-y', 'index': MATCH}, 'options'),
    Input({'type': 'series-dataframe', 'index': MATCH}, 'value')
)
def update_series_dropdowns(dataframe):
    if dataframe is None:
        return ((), ())
    else:
        return (dataframes[dataframe].columns,) * 2


@app.callback(
    Output('graph', 'figure'),
    Input({'type': 'series-dataframe', 'index': ALL}, 'value'),
    Input({'type': 'series-x', 'index': ALL}, 'value'),
    Input({'type': 'series-y', 'index': ALL}, 'value'),
    Input({'type': 'series-options', 'index': ALL}, 'value')
)
def update_figure(dataframe, x, y, options):
    figure = go.Figure()
    for index, (dataframe, x, y, options) in enumerate(zip(dataframe, x, y, options)):
        if dataframe is None or (x is None and y is None):
            continue

        if options is None:
            options = []

        color = px.colors.qualitative.Plotly[index]

        if 'line' in options:
            figure.add_traces(
                list(
                    px.line(
                        dataframes[dataframe],
                        x=x,
                        y=y,
                        color_discrete_sequence=[color],
                        markers='scatter' in options,
                    ).select_traces()
                )
            )
        elif 'scatter' in options:
            figure.add_traces(
                list(
                    px.scatter(
                        dataframes[dataframe],
                        x=x,
                        y=y,
                        color_discrete_sequence=[color],
                    ).select_traces()
                )
            )
    return figure


def main():
    parser = argparse.ArgumentParser(description="Quick CSV Plotting Utility")
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    init_app(args.files)
    app.run_server(debug=True)
