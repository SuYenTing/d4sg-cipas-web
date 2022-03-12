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
with open('./data/recommendDocs.pickle', 'rb') as f:
    recommendDocsDict = pickle.load(f)

# 主頁面內容
page_similarity = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("以文找文"))
        ])
    ]),

    # 文章列表
    dbc.Row([
        dbc.Col([
            html.Span('請選取史料故事:'),
            dash_table.DataTable(
                id='similarityStoriesTitleData',
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

    # 依使用者點選文章標題輸出文章內容
    dbc.Row([
        dbc.Col([
            dbc.Spinner(html.Div(id="similarityStoriesContent"), color="primary")
        ]),
    ], className='row mt-3 mb-3'),  

    # 依使用者點選文章產生推薦文章
    dbc.Row([
        dbc.Col([
            dbc.Spinner(html.Div(id="similarityRecommendContent"), color="primary")
        ]),
    ], className='row mt-3 mb-3'),  
])


# WEB後端運作
# 依使用者搜尋內容輸出對應結果
@app.callback(
    Output("similarityStoriesContent", "children"),
    Output("similarityRecommendContent", "children"),
    Input("similarityStoriesTitleData", "active_cell"),
    prevent_initial_call=True,
    )
def tokenizeStoriesRun(active_cell):

    print(active_cell)

    # 讀取使用者點擊的文章
    # 文章原始連結
    articleUrl = storiesData['網址'][active_cell['row']]
    # 文章標題
    articleTitle = storiesData['文章標題'][active_cell['row']]
    # 原文內容
    articleContent = storiesData['內文'][active_cell['row']]

    # 輸出原始文章內容
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
            ]),
        ], className='row mt-3 mb-3')
    ])

    # 輸出相似文章
    recommendDocs = recommendDocsDict[active_cell['row']]
    recommendDocs = recommendDocs[1:]  # 相似度第一篇為原文故剔除
    recommendContent = list()
    for elem in recommendDocs:
        iRecommendContent = html.A(
            html.P(
                storiesData['文章標題'][elem]),
                id='searchLink',
                href=storiesData['網址'][elem],
                target="_blank"
            )
        recommendContent.append(iRecommendContent)

    recommendContent = html.Div([
        html.Hr(),
        html.H4('相關文章：'),
    ] + recommendContent)

    return articleContent, recommendContent