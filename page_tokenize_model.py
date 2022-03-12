# 史料斷詞器
import dash_bootstrap_components as dbc
import pandas as pd
import re
from dash import html
from dash import Input, Output, State
from app import app, server
from ckiptagger import construct_dictionary, WS, POS, NER

# 載入CKIP模型
wsModel = WS("./model/ckiptagger/data", disable_cuda=True)
posModel = POS("./model/ckiptagger/data", disable_cuda=True)
nerModel = NER("./model/ckiptagger/data", disable_cuda=True)

# 載入自定義字典
customDict = pd.read_csv('./data/customDict.csv')
customDict = {elem: 1 for elem in customDict['word']}
customDict = construct_dictionary(customDict)

# Frontend
page_tokenize_model = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("史料斷詞器")),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.P("請輸入一篇史料文章讓CKIP模型來斷詞:"),
            dbc.Textarea(
                id="tokenizeModelText",
                value="1958年2月10日，時任中國國民黨（下稱國民黨）中央委員會第五組主任的上官業佑，向國民黨總裁蔣中正呈上一份簽呈，報告處理軍人之友社（下稱軍友社）、大陸災胞救濟總會（編按：即今日之「中華救助總會」，下稱救總）以及婦聯會（編按：即今日之「中華民國婦女聯合會」，原名「中華婦女反共抗俄聯合會」，下稱婦聯會）之預算改列為正式預算等相關事宜。", 
                maxlength=1000, 
                rows=5,
                className="mb-3"),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button("開始斷詞", id="tokenizeModelSubmit", color="primary")
        ])
    ], className="row mt-3 mb-3"),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.P("CKIP模型斷詞成果："),
            dbc.Spinner(html.Div(id="tokenizeModelOutput"), color="primary"),
        ]),
    ]),
])

# Backend
# 依使用者輸入文章進行實體辨識
@app.callback(
    Output("tokenizeModelOutput", "children"),
    Input("tokenizeModelSubmit", "n_clicks"), 
    State("tokenizeModelText", "value"),
    # prevent_initial_call=True,
    )
def tokenizeModelRun(n_clicks, tokenizeModelText):

    # 讀取使用者輸入文章
    doc = tokenizeModelText
    # 移除空格跳行字元
    doc = re.sub('\s', '', doc)

    # 執行CKIP斷詞
    wsModelResult = wsModel(
        [doc],
        sentence_segmentation=True,
        segment_delimiter_set={",", "。", ":", "?", "!", ";"},
        coerce_dictionary=customDict,
        )
    # 執行CKIP詞性標註
    posModelResult = posModel(wsModelResult)
    # 執行CKIP實體辨識
    entityModelResult = nerModel(wsModelResult, posModelResult)

    # 篩選關注實體
    targetEntity = ['DATE', 'ORG', 'PERSON', 'EVENT', 'FAC', 'GPE', 'LOC', 'WORK_OF_ART']
    entityColor = {
        'DATE': '#ffb549',
        'ORG': '#dd2a7b', 
        'PERSON': '#515bd4', 
        'EVENT': '#8134af', 
        'FAC': '#8134af', 
        'GPE': '#8134af', 
        'LOC': '#8134af', 
        'WORK_OF_ART':'#8134af'
    }
    entityModelResult = {elem for elem in entityModelResult[0] if elem[2] in targetEntity}

    # 整理輸出結果
    outputText = list()
    normalWord = ''
    ix = 0
    while ix < len(doc):

        # 判斷該字位置是否有符合實體辨識結果
        entity = [elem for elem in entityModelResult if elem[0] == ix]

        if entity:

            # 紀錄先前的一般字詞
            outputText.append(html.Span(normalWord))
            normalWord = ''

            # 紀錄實體辨識字詞
            entityEndSite = entity[0][1]
            entityType = entity[0][2]
            entityStr = doc[ix:entityEndSite]
            outputText.append(html.Span(entityStr, style={'color': entityColor[entityType]}))
            outputText.append(html.Span(entityType, style={'font-size': 'x-small', 'color': entityColor[entityType]}))
            ix = entityEndSite
        else:
            # 若未符合則紀錄一般字詞
            normalWord = f'{normalWord}{doc[ix]}'
            ix += 1

    outputText.append(html.Span(normalWord))

    return outputText