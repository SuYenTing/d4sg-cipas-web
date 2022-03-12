# D4SG黨產會網站
# navbar程式碼參考
# https://github.com/facultyai/dash-bootstrap-components/blob/main/examples/advanced-component-usage/Navbars.py

# 載入套件
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# 載入頁面
from app import app, server
from page_index import page_index
from page_tokenize import page_tokenize
from page_network import page_network
# from page_tokenize_model import page_tokenize_model
from page_search import page_search
from page_similarity import page_similarity

# this example that adds a logo to the navbar brand
app.layout = html.Div([

    # navbar
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("D4SG資料英雄計畫:黨產會專案", className="ml-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler-menu"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("史料斷詞成果", href="/page_tokenize", active="exact")),
                            dbc.NavItem(dbc.NavLink("網絡關係圖", href="/page_network", active="exact")),
                            # dbc.NavItem(dbc.NavLink("史料斷詞器", href="/page_tokenize_model", active="exact")),
                            dbc.NavItem(dbc.NavLink("史料搜尋", href="/page_search", active="exact")),
                            dbc.NavItem(dbc.NavLink("以文找文", href="/page_similarity", active="exact")),
                            dbc.NavItem(dbc.NavLink("數位專題", href="https://yihuai0806.github.io/cipas/index.html", active="exact", external_link=True, target="_blank")),
                            dbc.NavItem(dbc.NavLink("回到首頁", href="/", active="exact")),
                        ],
                        className="ml-2", navbar=True),
                    id="navbar-collapse-menu",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="mb-5",
    ),

    # page content
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# toggle the collapse on small screens
@app.callback(
    Output(f"navbar-collapse-menu", "is_open"),
    [Input(f"navbar-toggler-menu", "n_clicks")],
    [State(f"navbar-collapse-menu", "is_open")])
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# navbar link
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    if pathname == "/":
        return page_index
    elif pathname == "/page_tokenize":
        return page_tokenize
    elif pathname == "/page_network":
        return page_network
    # elif pathname == "/page_tokenize_model":
    #     return page_tokenize_model
    elif pathname == "/page_search":
        return page_search
    elif pathname == "/page_similarity":
        return page_similarity

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        dbc.Container([
            html.H1("404: Not found.", className="display-3"),
            html.Hr(className="my-2"),
            html.P(
                f"The pathname {pathname} was not recognised..."
                ),
            ], fluid=True, className="py-3",),
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    # app.run_server(debug=True, port=8050)
    app.run_server(host='0.0.0.0', debug=False, port=8050)
