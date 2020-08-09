# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def generate_table(dataframe, max_rows=10):
    print('Generate the table!')
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    # "Amount": [4, 1, 2, 2, 4, 5],
    "Amount": [3, 2, 4, 5, 1, 2],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


# Gantt chart
gantt_df = pd.DataFrame([
    dict(Task="Person", Start='2020-07-26 14:24:00.000000', Finish='2020-07-26 14:24:50.230000'),
    dict(Task="Person", Start='2020-07-26 14:26:00.245000', Finish='2020-07-26 14:26:30.876411'),
    dict(Task="Person", Start='2020-07-26 14:27:15.320000', Finish='2020-07-26 14:27:25.430000'),
    dict(Task="Person", Start='2020-07-26 14:28:25.430000', Finish='2020-07-26 14:28:55.900000'),
    dict(Task="Person", Start='2020-07-26 14:29:00.000000', Finish='2020-07-26 14:29:45.000000'),
    dict(Task="Stoplight", Start='2020-07-26 14:24:00.000000', Finish='2020-07-26 14:25:00.000000'),
    dict(Task="Stoplight", Start='2020-07-26 14:28:47.220000', Finish='2020-07-26 14:29:25.430000'),
    dict(Task="Bicycle", Start='2020-07-26 14:28:00.430000', Finish='2020-07-26 14:29:00.200000'),
    dict(Task="Bicycle", Start='2020-07-26 14:29:10.000000', Finish='2020-07-26 14:29:20.760000')
])

gantt_fig = px.timeline(gantt_df, x_start="Start", x_end="Finish", y="Task", color="Task")

gantt_fig.update_xaxes(
    rangeslider_visible=True,
    tickformatstops = [
        dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
        dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ]
)

gantt_fig.update_layout(clickmode='event')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash w/Hot-Reload'),

    html.Div(children='''
    Dash: A web application framework for Python. It makes nice dashboards.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df2),

    dcc.Graph(
        id='timeline',
        figure=gantt_fig
    )

])

if __name__ == "__main__":
    app.run_server(debug=True)