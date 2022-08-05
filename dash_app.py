from api.lottery_api.get_lottery_numbers import updateLotteryInfoDB, readFromDB
from dash import Dash, html, dcc, Input, Output, callback, dash_table

updateLotteryInfoDB()
df = readFromDB("SELECT DrawDate, Number1, Number2, Number3, Number4, Number5, Number6, Number7, CurGpAnnuity, CurGpCash, NextGpAnnuity, NextGpCash FROM lottery_info where game_id = 17")
app = Dash(__name__, title='Lottery Monitor')
server = app.server
app.config.suppress_callback_exceptions = True
app.layout = html.Div(children=[
    html.H1(children='Megamillions Info',
            style={
                    'textAlign': 'center',
    }),
    html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        # columns=[
        #     {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        # ],
        columns=[
            {'name': 'DrawDate', 'id': 'DrawDate', 'type': 'datetime'},
            {'name': 'Number1', 'id': 'Number1', 'type': 'numeric'},
            {'name': 'Number2', 'id': 'Number2', 'type': 'numeric'},
            {'name': 'Number3', 'id': 'Number3', 'type': 'numeric'},
            {'name': 'Number4', 'id': 'Number4', 'type': 'numeric'},
            {'name': 'Number5', 'id': 'Number5', 'type': 'numeric'},
            {'name': 'Powerball', 'id': 'Number6', 'type': 'numeric'},
            {'name': 'Multiplier', 'id': 'Number7', 'type': 'numeric'},
            {'name': 'CurGpAnnuity', 'id': 'CurGpAnnuity', 'type': 'numeric'},
            {'name': 'CurGpCash', 'id': 'CurGpCash', 'type': 'numeric'},
            {'name': 'NextGpAnnuity', 'id': 'NextGpAnnuity', 'type': 'numeric'},
            {'name': 'NextGpAnnuity', 'id': 'NextGpAnnuity', 'type': 'numeric'}
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        # column_selectable="single",
        # row_selectable="multi",
        # row_deletable=True,
        # selected_columns=[],
        # selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 25,
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(210, 210, 210)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',   
            'fontWeight': 'bold'
        },
        style_table={
            'overflowX': 'auto'
        }
    ),
    html.Div(id='datatable-interactivity-container'),
    ], style={
        'width':'95%',
        'textAlign': 'center',
        'margin-left': 'auto',
        'margin-right': 'auto'
    }),
    html.Div(children=[dcc.Markdown( 
                   " © 2022 [Beau-Malroney](https://beau-malroney.github.io/)  All Rights Reserved.")], 
                   style={
                    'textAlign': 'center'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)