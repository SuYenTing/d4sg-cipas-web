# 首頁
import dash_bootstrap_components as dbc
from dash import html

# 主頁面內容
page_index = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Center(html.H3("首頁"))
        ])
    ])
])