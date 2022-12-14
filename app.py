import base64
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State, dash_table
from source import method1_songs
from source import method2_songs
import os

import pandas as pd
import io

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Music", className="display-4"),
        html.Hr(),
        html.P(
            "Music Recommendation In Buisiness Intelligence Class", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                html.Br(),
                dbc.NavLink("Recommend BySong", href="/method1", active="exact"),
                html.Br(),
                dbc.NavLink("Recommend ByPlaylist", href="/method2", active="exact"),
                html.Br(),
                dbc.NavLink("Review", href="/review", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

home_input = html.Div(
    [
        html.H2("Music Recommendation"),
        html.H4("Business Intelligence"),
        html.H5("Team : Linus, Tristan, SeuYoon"),
        html.Br(),
        html.Div(children=[
            html.Div(style={"margin":"10px"}, children=[
                html.H6("1. Recommendation By Songs"),
                html.P("We recommend music based on the song of 2017 which is kaggle dataset."),
                html.P("Use the cosine similarity method to recommend 5 different music based on the music user input."),
                html.H1("\n")
            ]),
            html.Div(style={"margin":"10px"}, children=[
                html.H6("2. Recommendation By Playlists"),
                html.P("We recommend music based on the Spotify user's liked-song-playlist."),
                html.P("Check how many songs overlap for each playlist and recommend 10 other songs on the playlist that overlap the most."),
                html.H1("\n")
            ]),
            html.Div(style={"margin":"10px"}, children=[
                html.H6("3. User Review Page"),
                html.P("In order to improve evaluation and better interface, "),
                html.P("we have received reviews from users and implemented them so that administrators can check them."),
                html.H1("\n")
            ])
        ])
    ]
)

#music_name_list = method1_songs.get_songs_name()

method1_input = html.Div(
    [
        html.Datalist(id="song_name_lists", children=[
            html.Option(value= song_name) for song_name in method1_songs.get_songs_name()
        ]),
        html.H3("Music Recommendation By Songs"),
        html.Br(),
        html.P("Input your favorite song, and find out what is the similar song!"),
        html.Br(),
        html.Div([
            html.H4("Music Input"),
            html.Br(),
            dcc.Input(id = "userSongInput", placeholder="Music Name",list="song_name_lists"),
            html.Button(id = 'submit_userSong', n_clicks=0, children='Go!'),
            ]),
        html.P(),
        html.Div(id="userInput")
    ]
)


method2_input = html.Div(
    [
        html.H3("Music Recommendation By Playlists"),
        html.Br(),
        html.P("Input your song playlist, and find out what is recommendation songs!"),
        html.Br(),
        html.Div([
            html.H4("Playlist Input"),
            html.Br(),
            html.Div(children=[
                html.Div(style={"float":"left", "margin":"10px"}, children=[
                    html.H6("Input your playlist csv file."),
                    html.P("1. Go to Exportify and Login your Spotify Account."),
                    "Go to ",
                    html.A("Exportify.net", href='https://exportify.net/', target="_blank"),
                    html.P("2. Select the playlist you want and Click the \"Export\" button."),
                    html.P("3. Input the playlist csv file."),
                    html.Br(),
                    dcc.Upload(
                        id='uploadCSV',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                    html.Div(id='output-data-upload'),
                ]),
                html.Div(style={"float":"left", "margin":"10px", "margin-top":"210px", "margin-left":"20px"}, children=[
                    html.Button(id="csvInput", n_clicks=0, children="Go!", style={"height":"60px"})
                ]),
                html.Div(id = "playListRec",style={"float":"left", "margin":"10px", "margin-left":"20px"})
            ]),
            ]),
    ]
)

review_input = html.Div(
    [
        html.H3("User Review Page"),
        html.Br(),
        html.H5("Let us know if you were satisfied with our service!"),
        html.Br(),
        html.Div(style={"float":"left", "margin" : "20px"},children=[
            html.P("1. How was the music recommendation by Songs?"),
            dcc.Input(id="song_review", placeholder="Tell us how was it!", style={"width":"500px", "height":"100px"}),
            html.H1("\n"),
            html.P("2. How was the music recommendation by Playlists?"),
            dcc.Input(id="playlist_review", placeholder="Tell us how was it!", style={"width":"500px", "height":"100px"}),
            html.H1("\n"),
            html.P("3. How was the interface of our web site?"),
            dcc.Input(id="interface_review", placeholder="Tell us how was it!", style={"width":"500px", "height":"100px"}),
            html.H1("\n"),
            html.Button(id="submit_review", n_clicks=0, children="Submit"),
            html.Div(id="hidden-div",style={"display":"none"})
        ]),
        html.Div(style={"float":"left", "margin":"20px"}, children=[
            html.P("If you are administrator, please input the password and check the user's review."),
            dcc.Input(id="password", type="password", placeholder="password", style={"margin-right":"10px"}),
            html.Button(id="pwd_button", n_clicks=0, children="Enter"),
            html.Div(id = "user_review_div")
        ])

    ]
)

def parse_contents(contents, filename, date):
    print("parse start")
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    #user_playList = df["Track Name"].tolist()
    #print(df["Track Name"].tolist())
    return html.Div([
        html.H6(filename),

        dash_table.DataTable(
            style_data={'whitespace':'normal',
            'height':'auto',
            'overflow':'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 1
            },
            data = df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in [df.columns[2], df.columns[3],df.columns[4]]]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:20] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def makePlayList(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return dict(zip(df["Spotify ID"], df["Track Name"]))

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print(pathname)
    if pathname == "/":
        return home_input
    elif pathname == "/method1":
        return method1_input
    elif pathname == "/method2":
        return method2_input
    elif pathname == "/review":
        return review_input
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

@app.callback(Output("userInput", "children"),
[Input("submit_userSong", "n_clicks")],
[State("userSongInput", "value")])
def updateUserInput(n_clicks,userInput):
    print(n_clicks)
    print(userInput)
    if(n_clicks > 0):
        result = method1_songs.get_recommend(userInput)
        htmlReturn = [html.Br(), html.H5("Recommend Songs : ")]
        i = 0
        for song in result:
            i += 1
            htmlReturn.append(html.P("{}. ".format(i) + song))

        return htmlReturn
    
@app.callback(Output('output-data-upload', 'children'),
              Input('uploadCSV', 'contents'),
              State('uploadCSV', 'filename'),
              State('uploadCSV', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip([list_of_contents], [list_of_names], [list_of_dates])]
        return children

@app.callback(Output("playListRec", "children"),
Input("csvInput", "n_clicks"),
State("uploadCSV", "contents"),
State("uploadCSV", "filename"))
def updatePlaylistInput(n_clicks, contents, filename):
    print(n_clicks)
    print(filename)
    if(n_clicks > 0):
        user_playList = makePlayList(contents, filename)
        result = method2_songs.recommend_songs(user_playList, filename)

        htmlReturn = [html.H5("Recommend Songs : ")]
        i = 0
        for song in result:
            i += 1
            htmlReturn.append(html.P("{}. ".format(i) + song))

        return htmlReturn

@app.callback(Output("hidden-div", "children"),
Input("submit_review", "n_clicks"),
State("song_review", "value"),
State("playlist_review", "value"),
State("interface_review", "value")
    )
def saveReview(n_clicks, song_review, playlist_review, interface_review):
    review_file = open(os.getcwd() + "/assets/review/review.csv", "a")
    print("review submit")
    if(n_clicks > 0):
        print(song_review + "," + playlist_review + "," + interface_review)
        review_file.write("\""+song_review+"\"" + "," + "\""+playlist_review +"\""+ "," + "\""+interface_review +"\""+ "\n")

@app.callback(Output("user_review_div", "children"),
Input("pwd_button", "n_clicks"),
State("password", "value")
)
def showReview(n_clicks, pwd_value):
    if(n_clicks> 0):
        if(pwd_value=="1217"):
            df = pd.read_csv(os.getcwd() + "/assets/review/review.csv")
            return (
                html.Table([html.Tr([html.Th(col) for col in df.columns])] + 
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(min(len(df), 10))]
            ) 
            )

if __name__ == "__main__":
    print("Run server ")
    app.run_server(debug=True)
    
    