import base64
import datetime
import io
import os

import dash
from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash import dash_table
# import dash_table

from did import DiD

import pandas as pd

did = None
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
PAGE_SIZE = 5

if os.path.isfile('assets/did.png'):
    os.remove('assets/did.png')


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        global did
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

            did = DiD(df)
            # print(did.create_first_model())
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            did = DiD(df)
            # print(did.create_first_model())
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5("File Uploaded: "+ filename),
        html.H6("Upload DateTime"+str(datetime.datetime.fromtimestamp(date))),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=PAGE_SIZE,
            page_current = 0
    ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-data-upload'),
    # html.Div([
    #     html.H5("model summary: "),
    #
    #     dash_table.DataTable(
    #         id = 'descriptive_stats_tbl',
    #         data=[]
    # )
    # ]),
    html.H5("Select Model To Use"),
    html.Div([
            dcc.Dropdown(
                id='model_selection',
                options=[{'label': i, 'value': i} for i in ['DiD']],
                value=' '
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    # html.Div(id='model_raw_output')
    html.Br(),
    html.Img(id="model_img", src=app.get_asset_url('did.png'))

])



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback([Output("model_img", "src")],
              [Input('model_selection', 'value')] )
def descriptive_stats(value):
    if did:
        if value == "DiD":
            model_summary = did.create_first_model()
            print(model_summary.as_text())
            image = did.model_summary_result(model_summary)
            print(dir(model_summary))
            return image
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)