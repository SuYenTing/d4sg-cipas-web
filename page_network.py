# 網絡關係圖
import dash_bootstrap_components as dbc
import pickle
from dash import dcc
from dash import html
from dash import Input, Output, State
from app import app


# 讀取預先繪製好的圖
saveFigName = f'./data/networkPlot.pickle'
with open(saveFigName, 'rb') as handle:
    networkFigDict = pickle.load(handle)

# 主頁面內容
page_network = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("網絡關係圖"))
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.P("請選擇要關注的史料類別:"),
            dbc.Select(
                id='networkType',
                options=[
                    {'label': elem, 'value': elem} for elem in [
                        '全部','中國國民黨','中華救助總會','婦聯會','救國團','民眾服務社', 
                        '中央日報社','三中案','革實院','黨營事業','世亞盟','松山油漆廠']
                    ],
                value='全部'
            )
        ]),

        dbc.Col([
            html.P("請選擇要繪製的關係:"),
            dbc.Select(
                id='networkRelation',
                options=[
                    {'label': '組織', 'value': 'ORG'}, 
                    {'label': '人名', 'value': 'PERSON'}
                    ], 
                value='ORG'
            )
        ])
    ], className='row mt-3'),

    dbc.Row([
        dbc.Spinner(dcc.Graph(id='networkFig'), color="primary")
    ], className='row mt-3')
])

# Backend
# 依使用者輸入文章進行實體辨識
@app.callback(
    Output("networkFig", "figure"),
    Input("networkType", "value"), 
    Input("networkRelation", "value"), 
    # prevent_initial_call=True,
    )
def networkPlot(networkType, networkRelation):
    return networkFigDict[networkType][networkRelation]

