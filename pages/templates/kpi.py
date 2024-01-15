from dash import html


def generate_kpi(name: str, value: int):

    content = html.Div(
        className="col-xl-3 col-md-6 mb-4",
        children=[
            html.Div(
                className="card shadow h-100 py-2",
                children=[
                    html.Div(
                        className="card-body",
                        children=[
                            html.Div(
                                className="row no-gutters align-items-center",
                                children=[
                                    html.Div(
                                        className="text-xs font-weight-bold text-uppercase mb-1",
                                        children=name
                                    ),
                                    html.Div(
                                        className="h5 mb-0 font-weight-bold text-gray-800",
                                        children=value
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    return content