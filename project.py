from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from collections import Counter
#import matplotlib.pyplot as plt
from datetime import datetime, date, time
from itertools import chain

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import numpy as np
colors = px.colors.sequential.RdBu



df = pd.read_csv('Frontend.csv', sep=',')


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)


#----------уникальные города-------------------
all_town = df['area_name'].unique()
#print(all_town)

#----------подсчет вакансий по городам---------
array = df['area_name']
c = Counter(array)
#print(c)

df2= pd.DataFrame()
df2['HTML']=df['html_descriprion']
df2['HTML5']=df['html5']
df2['JS']=df['js']
df2['JavaScript']=df['javascript']
df2['css']=df['css']
df2['scss']=df['scss']
df2['c_sharp']=df['c_sharp']
df2['python']=df['python']
df2['php']=df['php']
df2['sql']=df['sql']
df2['ui_ux']=df['ui_ux']

new_df = pd.DataFrame({'skills': ['CSS', 'HTML', 'JavaScript', 'JS', 'HTML5', 'SCSS', 'SQL', 'PHP', 'Python', 'UI/UX', 'C#'], 'quantity': [1643, 1449, 1202, 1160, 683, 315, 273, 250, 149, 89, 53]})


state_list = new_df['skills'].unique()

#----------выделение месяца из даты-----------
df['month'] = pd.DatetimeIndex(df['published_at']).month.astype(str) + '-' + pd.DatetimeIndex(df['published_at']).year.astype(str)
df['published_at'] = pd.to_datetime(df['month'], format='mixed')

agg_func_math_to = {'salary_to': ['mean'],} 
agg_func_math_from = {'salary_from': ['mean'],}
counts_to=df.groupby(df['published_at']).agg(agg_func_math_to).round(2)
counts_from=df.groupby(df['published_at']).agg(agg_func_math_from).round(2)

MAINSTYLE = {
    "background-color": "#b4c4cc"
}

SIDESTYLE = {
    "position": "fixed",
    "top": 10,
    "left": 10,
    "bottom": 10,
    "width": "16rem",
    "padding": "2rem 1rem",
    "border-radius": "20px",
    "background-color": "#ffffff",
    "border": "5px solid",
    "border-color": "#d8e8e4"
}


CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([   
        html.H2("Разделы", className="display-4", 
                style={'color': 'Black',
                    'padding-left': '16px',
                    'font-size': '40px',
                    'font-weight': 'bold',
                    'font-family': 'Arial'
                    }),
            html.Hr(style= {    "border": "none",
                    "background-color": "grey",
                    "color": "grey",
                    "height": "2px",
                    "border-radius": "10px"}),    
            dbc.Nav([
                    dbc.NavLink("Диаграммы по вакансиям", href="/page1", active="exact", style = {"border-radius": "50px", "background-color": "#010920", "font-size": '14px', "height": "100%", "margin-bottom": "5px", "text-align": "center", "vertical-align": "middle"}),
                    dbc.NavLink("Диаграммы по заработным платам", href="/page2", active="exact",style = {"border-radius": "50px", "background-color": "#010920", "font-size": '14px', "height": "100%", "margin-bottom": "5px", "text-align": "center", "vertical-align": "middle"}),
                    dbc.NavLink("Диаграмма по навыкам", href="/page3", active="exact",style = {"border-radius": "50px", "background-color": "#010920", "font-size": '14px', "height": "100%", "margin-bottom": "5px", "text-align": "center", "vertical-align": "middle"}),
                ],
                vertical=True,pills=True),
        ],
        style=SIDESTYLE,
    ),
    html.Div(id="page-content", children=[], style=CONTSTYLE)
], style=MAINSTYLE)

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def pagecontent(pathname):
    if pathname == "/page1":
        return[

    html.Div([
    html.H1("Диаграммы по вакансиям на должность Frontend-разработчик с сайта hh.ru", style={"font-size": '34px', "padding-top": "20px", "text-align": "center", "vertical-align": "middle", 'font-weight': 'bold', "height": "auto", "width": "1380px"}),

    ], style = {
            "margin": 0,
            "margin-bottom": '20px',   
            "border-radius": "20px",
            "background-color": "#ffffff",
            'font-family': 'Arial',
            "height": "80px",
            "text-align": "center",
            "vertical-align": "middle",
            "width": "1380px"
    }),

    



    html.H3("Общее количество выложенных вакансий по месяцам", style= {"position": "absolute", "z-index": "1", "margin": "15px 0px 0px 80px"}),
    html.Div(
    dcc.Graph(figure=px.histogram(x=df['published_at'].sort_values(ascending=True), histfunc='count', 
                labels={'x':'month'},
                opacity=0.5,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                text_auto=True).update_layout(bargap=0.05, xaxis_title = "", yaxis_title = "Количество вакансий")),style= {"height": "490px", "background": "white", "border-radius": "20px", "padding-top": "20px"}),
    html.Div([
    html.Div([
            dcc.Dropdown(
                id = 'crossfilter-cont',
                options = [{'label': i, 'value': i} for i in all_town],
                # значение континента, выбранное по умолчанию
                value = ['Москва', 'Санкт-Петербург', 'Минск', 'Новосибирск', 'Краснодар', 'Казань'],
                # возможность множественного выбора
                multi = True,
            style= {"border-radius": "20px", "width": "1380px", 
                    "text-align": "left",
                    "vertical-align": "middle",
                    "padding": "10px 0px 10px 0px"})
        ],
        style = {'width': '48%', 'display': 'inline-block'})]),
    html.H3("Процент вакансий по городам и", style = {"position": "absolute", "z-index": "1", "margin": "20px 0px 0px 855px", 'font-size': '20px', "width": "500px"}),
    html.H3("средняя заработная плата по городам", style = {"position": "absolute", "z-index": "1", "margin": "40px 0px 0px 855px", 'font-size': '20px', "width": "500px"}),
            html.Div(
            dcc.Graph(id = 'pie'),
            style = {'width': '50%', 'display': 'inline-block', "background": "white", "border-radius": "20px 0px 0px 20px", "padding-top": "20px", "height": "490px"}
        ),
        html.Div(
            dcc.Graph(id = 'line'),
            style = {'width': '50%', 'display': 'inline-block', "background": "white", "border-radius": "0px 20px 20px 0px", "padding-top": "20px", "height": "490px"}
        ),
    
        ]
    elif pathname == "/page2":
        return[
            html.Div(
            html.H1("Диаграммы по заработным планам на должность Frontend-разработчик", style={"font-size": '34px', "padding-top": "20px", "text-align": "center", "vertical-align": "middle", 'font-weight': 'bold', "height": "auto", "width": "1380px"})
            , style = {
            "margin": 0,
            "margin-bottom": 20,   
            "border-radius": "20px",
            "background-color": "#ffffff",
            'font-family': 'Arial',
            "height": "80px",
            "text-align": "center",
            "vertical-align": "middle",
            "width": "1380px",}),

            html.H3("Диаграмма с минимальной и максимальной заработной платой", style= {"position": "absolute", "z-index": "1", "margin": "15px 0px 0px 80px"}),
            html.Div(
            dcc.Graph(figure = px.line().add_scatter(line= dict(color = '#60afc5'),
                        name='Максимальная заработная плата',
                        mode='lines+markers', 
                        line_shape='spline', 
                        x=counts_to.index, 
                        y=list(chain.from_iterable(counts_to.values))).add_scatter(line= dict(color = '#8c74a4'),
                        name='Минимальная заработная плата',
                        mode='lines+markers',
                        line_shape='spline', 
                        x=counts_to.index, 
                        y=list(chain.from_iterable(counts_from.values))).update_layout(xaxis_title = "", yaxis_title = "Заработная плата")),
            style = {"height": "490px", "background": "white", "border-radius": "20px", "padding-top": "20px"}),
            html.Div(style= {"height": "300px"}),

        ]

    elif pathname == "/page3":
        return[
            html.Div(
            html.H1("Диаграмма по навыкам на должность Frontend-разработчик", style={"font-size": '34px', "padding-top": "20px", "text-align": "center", "vertical-align": "middle", 'font-weight': 'bold', "height": "auto", "width": "1380px"})
            , style = {
            "margin": 0,
            "margin-bottom": 0,   
            "border-radius": "20px",
            "background-color": "#ffffff",
            'font-family': 'Arial',
            "height": "80px",
            "text-align": "center",
            "vertical-align": "middle",
            "width": "1380px",}),


        dcc.Dropdown(
            id="bar-polar-app-x-dropdown",
            value=state_list[:11],
            options=state_list,
            multi=True,
        style= {"border-radius": "20px", "width": "1380px", 
                    "text-align": "left",
                    "vertical-align": "middle",
                    "padding": "10px 0px 10px 0px",
                    },
        ),

        dcc.Graph(id="bar-polar-app-x-graph",
                style = { "background": "white", "border-radius": "20px", "padding": "20px 0px 20px 0px", "height": "490px"}),
        html.Div(style={ "height": "150px"})
        
        ]
    

@app.callback(
    Output("bar-polar-app-x-graph", "figure"),
    Input("bar-polar-app-x-dropdown", "value"),
)

def update_graph(skills):
    filtred_df = new_df[new_df['skills'].isin(skills)]
    fig = px.bar_polar(filtred_df,
        r=filtred_df['quantity'], theta = filtred_df['skills'], color = filtred_df['skills'], template="ggplot2",  color_continuous_midpoint = px.colors.sequential.Agsunset,  color_continuous_scale=px.colors.sequential.Agsunset, direction = 'counterclockwise', color_discrete_sequence = px.colors.sequential.Agsunset
    ).update_layout(legend_title = 'Навыки')
    return fig

@app.callback(
    Output('pie', 'figure'),
    Input('crossfilter-cont', 'value')
)

def updated_diagramm(area_name):

    filtered_data = df[df['area_name'].isin(area_name)]
    counts= filtered_data['area_name'].value_counts()
    figure = px.pie(filtered_data, 
                    names=counts.index, 
                    values=counts.values, 
                    color_discrete_sequence=px.colors.sequential.PuBu_r).update_traces(textposition='inside').update_traces(textposition='inside', textinfo='percent+label').update_layout(plot_bgcolor='white',margin=dict(l=20, r=20, t=20, b=20)).update_yaxes(showline=False,showgrid=False).update_xaxes(showline=False,showgrid=False)
    return figure

@app.callback(
    Output('line', 'figure'),
    Input('crossfilter-cont', 'value')
)

def updated_diagramm2(area_name):
    filtered_data = df[df['area_name'].isin(area_name)]
    figure = px.line(filtered_data, x="area_name", y="salary_AVG", color="area_name", symbol='area_name', hover_name= 'employer_name', color_discrete_sequence=px.colors.qualitative.Safe).update_layout(xaxis_title = "", yaxis_title = "Средня заработная плата", legend_title = 'Города')
    return figure

app.config['suppress_callback_exceptions'] = True




if __name__ == '__main__':
    app.run_server(debug=True)
