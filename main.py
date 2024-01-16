import sys
print(sys.executable)

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

from pages.templates.sidebar import generate_sidebar

#initiat Dash app

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
server = app.server
@jit(nopython=False)

app.layout = html.Div(
    id="wrapper",
    children=[                              #add new pages in order to rejester we need to call regter method
        generate_sidebar(pages=dash.page_registry.values()),
        html.Div(
            id="content-wrapper",
            className="d-flex flex-column",
            children=[
                html.Div(
                    id='content',
                    children=[
                        html.Div(
                            className="container-fluid",
                            children=[
                                dash.page_container #page containrs comes from 3 files 
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
