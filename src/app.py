import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State

df = pd.read_csv('profile_data1.csv')
app = Dash(__name__)
server = app.server

dtable = dash_table.DataTable(
    style_data={
        'whiteSpace': 'normal',
    },
    data=df.to_dict('records'),
    columns=[{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'upworkUrl' else {'id': x, 'name': x} for x in
             df.columns],
    # columns = [
    #     {'id' : 'No', 'name' : 'No'},
    #     {'id' : 'name', 'name' : 'Name'},
    #     {'id' : 'city', 'name' : 'City'},
    #     {'id' : 'title', 'name' : 'Title'},
    #     {'id' : 'description', 'name' : 'Description'},
    #     {'id' : 'totalEarnings', 'name' : 'Total Earnings', 'type' : 'numeric', 'format' : money},
    #     {'id' : 'totalHoursBilled', 'name' : 'Total Hours Billed'},
    #     {'id' : 'earningPerHour', 'name' : 'Earning Per Hour', 'type' : 'numeric', 'format' : money},
    #     {'id' : 'totalPortfolio', 'name' : 'Total Portfolio'},
    #     {'id' : 'upworkUrl', 'name' : 'Upwork Url', 'presentation' : 'markdown'}
    # ],
    style_cell={'textAlign': 'left'},
    style_header={'backgroundColor': '#F88379', 'color': 'black', 'fontWeight': 'bold', 'textAlign': 'center',
                  'border': '1px solid black'},
    filter_action="native",
    style_table={"overflowX": "auto"},
    sort_action="native",
    sort_mode="multi"
)
download_button = html.Button("Download Filtered CSV", style={"marginTop": 20})
download_component = dcc.Download()

app.layout = html.Div(
    [
        download_component,
        download_button,
        dtable,
    ]
)


@app.callback(
    Output(download_component, "data"),
    Input(download_button, "n_clicks"),
    State(dtable, "derived_virtual_data"),
    prevent_initial_call=True,
)
def download_data(n_clicks, data):
    dff = pd.DataFrame(data)
    return dcc.send_data_frame(dff.to_csv, "filtered_csv.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
