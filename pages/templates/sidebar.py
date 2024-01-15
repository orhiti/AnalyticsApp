from dash import html, dcc

def generate_sidebar(pages):
    content = html.Ul(
        id="accordionSidebar",
        className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion",
        children=[
            html.Hr(className="sidebar-divider my-0"),
            html.Div(
                children=[
                    html.Li(
                        className="nav-item",
                        children=[
                            dcc.Link(
                                className="nav-link",
                                children=f"{page['name']} - {page['path']}",
                                href=page["relative_path"]
                            )
                        ]
                    ) for page in pages
                ]
            ),
        ]
    )
    return content
