# 史料斷詞
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
from dash import html, dash_table, dcc, Input, Output, State
from app import app, server

# 讀取史料故事文章與斷詞結果
storiesData = pd.read_excel('./data/storiesData.xls')
storiesData['文章編號'] = range(1, len(storiesData)+1)
storiesData = storiesData.rename(columns={'標題': '文章標題'})
with open('./data/tokenizeStoriesData.pickle', 'rb') as f:
    tokenizeContent = pickle.load(f)

# 主頁面內容
page_tokenize = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("史料斷詞"))
        ])
    ]),

    # 文章列表
    dbc.Row([
        dbc.Col([
            html.Span('請選取史料故事:'),
            dash_table.DataTable(
                id='tokenizeStoriesTitleData',
                data=storiesData.to_dict('records'), 
                columns=[{"name": "文章編號", "id": "文章編號"}, {"name": "文章標題", "id": "文章標題"}], 
                page_action='none',
                fixed_rows={'headers': True},
                style_cell_conditional=[
                    {'if': {'column_id': '文章編號'}, 'textAlign': 'center', 'minWidth': '80px'},
                    {'if': {'column_id': '文章標題'}, 'textAlign': 'left'}
                    ],
                style_table={'height': '300px'},
                ),
        ]), 
    ]),

    html.Hr(),

    # 依使用者點選目標輸出對應內容
    dbc.Row([
        dbc.Col([
            dbc.Spinner(html.Div(id="tokenizeStoriesContent"), color="primary")
        ]),
    ], className='row mt-3 mb-5'),  
])


# WEB後端運作
# 依使用者搜尋內容輸出對應結果
@app.callback(
    Output("tokenizeStoriesContent", "children"),
    Input("tokenizeStoriesTitleData", "active_cell"),
    prevent_initial_call=True,
    )
def tokenizeStoriesRun(active_cell):

    # 讀取使用者點擊的文章
    # 文章原始連結
    articleUrl = storiesData['網址'][active_cell['row']]
    # 文章標題
    articleTitle = storiesData['文章標題'][active_cell['row']]
    # 原文內容
    articleContent = storiesData['內文'][active_cell['row']]
    # 斷詞結果
    webContent = tokenizeContent[active_cell['row']]

    # 輸出結果
    articleContent = html.Div([

        dbc.Row([
            dbc.Col([
                html.Center([html.H4(articleTitle)])
            ]),
        ], className='row mt-3'),

        dbc.Row([
            dbc.Col([
                dbc.Button("開啟網站文章原頁面", href=articleUrl, target="_blank")
            ]),
        ], className='row mt-3'),    

        dbc.Row([
            dbc.Col([
                html.Center([html.H4('原文內容')]),
                html.Div(articleContent, style={'whiteSpace': 'pre-wrap'}),
            ], className='col-6 border'),
            dbc.Col([
                html.Center([html.H4(f'斷詞結果')]),
                html.Div(webContent, style={'whiteSpace': 'pre-wrap'}),
            ], className='col-6 border'),
        ], className='row mt-3 mb-5')
    ])

    return articleContent