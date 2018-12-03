
# coding: utf-8

# In[ ]:


#for the unit of measures you can either make a drop down table or mention it in the title

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
app = dash.Dash()



df = pd.read_csv(
    'C:\\Users\\PC\\Documents\\ESADE\\Cloud Computing\\Session 7\\CC 7\\CC 7\\nama_10_gdp\\nama_10_gdp_1_Data.csv')
df=df[df['UNIT']=='Current prices, million euro']


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = sorted(df['NA_ITEM'].unique())
available_countries = sorted(df['GEO'].unique())


app.layout = html.Div([
     html.H1(
        children='Final Project',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div([
        
        html.H2(
        children='Graph 1',
        style={
            'textAlign': 'center'}),
            
        html.H3(
        children='Indicators : ',
        style={
            'textAlign': 'left' }),
        
        html.Div([
            html.H4(
            children='Variable X : ',
            style={
            'textAlign': 'left' }),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Macro-economic Indicator 1'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H4(
            children='Variable Y : ',
            style={
            'textAlign': 'left' }),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Macro-economic Indicator 2'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic-1'),
    
    html.H2(children='\n'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
 
    
    
    html.Div([
        
        html.H2(
        children='\n\n\nGraph 2',
        style={
            'textAlign': 'center'}),
            
        html.H3(
        children='Indicators : ',
        style={
            'textAlign': 'left' }),
        
        html.Div([
            html.H4(
            children='Variable Y : ',
            style={
            'textAlign': 'left' }),
            dcc.Dropdown(
                id='yaxis-column-bis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Macro-economic Indicator'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H4(
            children='Country : ',
            style={
            'textAlign': 'left' }),
            dcc.Dropdown(
                id='graph_country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Country'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic-2'),
    
    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic-1', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph_1(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name) & (dff['GEO'] == str(i))]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name) & (dff['GEO'] == str(i))]['Value'],
            text=dff[(dff['NA_ITEM'] == yaxis_column_name) & (dff['GEO'] == str(i))]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }, name= i[:18]
        ) for i in available_countries ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic-2', 'figure'),
    [dash.dependencies.Input('yaxis-column-bis', 'value'),
     dash.dependencies.Input('graph_country', 'value')])
def update_graph_2(yaxis_column_bis_name, graph_country_name
                 ):
    dfg = df[df['GEO'] == graph_country_name]
    
    return {
        'data': [go.Scatter(
            x=dfg[dfg['NA_ITEM'] == yaxis_column_bis_name]['TIME'],
            y=dfg[dfg['NA_ITEM'] == yaxis_column_bis_name]['Value'],
            text=dfg[dfg['NA_ITEM'] == yaxis_column_bis_name]['Value'],
            mode='lines+markers'
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
            },
            yaxis={
                'title': yaxis_column_bis_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

