import pandas as pd
import requests
import json
import local_headers
from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)

symbol= "AAPL"
period= "1mo" # 1d 5d 1mo 3mo 6mo 1y 5y 10y ytd max
region= "US"
interval = "1d"
url = f"https://yfapi.net/v8/finance/chart/{symbol}?range={period}&region={region}&interval={interval}&lang=en&events=div%2Csplit"

querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}

headers = local_headers.headers

print(url)
response = requests.request("GET", url, headers=headers)

json_txt = json.loads(response.text)

df = pd.DataFrame()
df = pd.DataFrame.from_dict(json_txt["chart"]["result"][0]["indicators"]["quote"][0])
df["date"] = pd.to_datetime(json_txt["chart"]["result"][0]["timestamp"], unit="s")
df["symbol"] = symbol

fig = px.line(df, x="date", y="close")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)