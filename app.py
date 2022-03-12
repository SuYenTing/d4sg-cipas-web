import dash
import dash_bootstrap_components as dbc

# WEB初始化設定
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0'}]
)
# 網站名稱
app.title = 'D4SG資料英雄計畫:黨產會專案'

# For Heroku Deploy
server = app.server