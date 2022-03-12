# 史料搜尋
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
from dash import html, dash_table, dcc, Input, Output, State
from app import app, server
import re


# 清洗資料函數
def cleanText(text):
    # 移除數字, 空格(含跳行), 英文句點, 英文逗點
    # text = re.sub('\d|\s|\.|\,', '', text)
    # 移除空格(含跳行)
    text = re.sub('\s', '', text)
    # 移除 資料來源 / 本文參考 / 全文參考 / 引自 (含)以後的字元
    matchSite = re.search('資料來源|本文參考|全文參考|引自', text)
    if matchSite:
        text = text[:matchSite.span()[0]]
    return text


# 讀取史料故事文章, 詞頻矩陣, 相似文章
storiesData = pd.read_excel('./data/storiesData.xls')
# 清洗史料故事文章內容
for i in range(len(storiesData)):
    storiesData['內文'][i] = cleanText(storiesData['內文'][i])

# Frontend
page_search = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("史料搜尋"))
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.P("請輸入想搜尋的關鍵字: "),
            dbc.Input(id="searchText", placeholder="", type="text"),
        ]),
        dbc.Col([
            dbc.Button("查詢", id="searchSubmit", color="primary", style={'margin-top': '40px'})
        ])
    ], className="row mt-3 mb-3"),

    html.Hr(),

    dbc.Spinner(html.Div(id="searchOutput"), color="primary"),
])

# Backend
# 依使用者輸入查詢內容返回文章
@app.callback(
    Output("searchOutput", "children"),
    Input("searchSubmit", "n_clicks"), 
    State("searchText", "value"),
    prevent_initial_call=True,
    )
def tokenizeModelRun(n_clicks, searchText):

    # 尋找相關文章
    searchIdx = list()
    for i in range(len(storiesData)):
        if searchText in storiesData['內文'][i]:
            searchIdx.append(i)

    if searchIdx:

        # 取前10名文章呈現
        searchIdx = searchIdx[0:10]

        # 迴圈整理前端程式碼
        searchOutput = list()
        for i in searchIdx:

            searchContent = dbc.Row([
                dbc.Col([
                    html.A(
                        html.H4(storiesData['標題'][i]), 
                        id='searchLink',
                        href=storiesData['網址'][i], 
                        target="_blank"),
                    html.Span(storiesData['內文'][i][0:300]+' ......'),  # 只呈現前300字
                    html.Hr()
                ])
            ], className="row mt-3 mb-3")
            searchOutput.append(searchContent)

    else:
        searchOutput = dbc.Row([
            dbc.Col([
                html.Span(['我們從史料文章中找不到與 ']),
                html.Span([searchText], style={'color': 'blue'}),
                html.Span([' 相關的文章，請試試看別的關鍵字']),
            ])
        ])
        
    return searchOutput

