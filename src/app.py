import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Reading data using pandas
df_new = pd.read_excel('DatosGraficarConInfrasonidos.xlsx',sheet_name = 'Hoja1')
df2 = pd.read_excel('senales_infrasonido_2020_2022.xlsx',sheet_name = 'Hoja1')
df2 = df2[df2['Energía MJ '] < 124 ]
df_is = pd.read_excel('senalesinfrasonidoactualizadas.xlsx',sheet_name = 'Señales infrasonido 2020 - 2022')

# Reading SO2 new file
dtype_dict = {'FECHA': str, 'Max': float, 'Prom': float}

df_so2 = pd.read_excel('DATOS SO2 MAXIMOS Y PROMEDIOS DIARIOS 2010 a 2022 PARA MULTIPARÁMETRICA (2).xlsx',sheet_name = 'Datos Max y Prom 2010-2022', na_values='-', dtype=dtype_dict)
df_so2['FECHA'] = pd.to_datetime(df_so2['FECHA'], errors='coerce')
fechas_null = np.where(df_so2['FECHA'].isnull())[0]
df_so2['FECHA'].iloc[fechas_null] = [df_so2['FECHA'][fecha-1] + pd.Timedelta(days=1) for fecha in fechas_null]
df_so2 = df_so2[df_so2['FECHA']>=df_is['Fecha/ Hora UTC'][0]]


# column_options = [{'label': 'Energía MJ', 'value': 'Energía MJ '},
#                   {'label': 'Presión Máxima Pa', 'value': 'Presión Máxima Pa'},
#                   {'label': 'Presión Reducida Pa', 'value': 'Presión Reducida Pa'}]
column_options = [{'label': 'Energía MJ', 'value': 'Energía MJ'},
                  {'label': 'Presión Máxima Pa', 'value': ' Presión max (Pa)'},
                  {'label': 'Presión Reducida Pa', 'value': 'Presión red (Pa)'}]
column_names = ['Energía MJ ', 'Presión Máxima Pa', 'Presión Reducida Pa']

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div(children=[
    html.Div(children=[
    html.Img(src='https://www2.sgc.gov.co/Style%20Library/themes/Intranet/images/logo-b.png')], 
             style={'height':145, 'width':250, 'background-color':'lightgray', 'display':'inline-block', 'border':'0px dotted red'}),
    html.Div(children=[
    html.H1("Datos de infrasonido VNR 2020 - 2022")],
            style={'display':'inline-block', 'width':'70%', 'border':'0px dotted red', 'font-family':  'ABCDiatype', 'justify-content': 'center'})],
             style={'border':'0px dotted red','display': 'table', 'width':'100%', 'justify-content': 'center' }),
    html.Div(children=[
        html.Div(children=[
    # Add a dropdown with identifier
    dcc.Dropdown(id='choose_col',
        # Set the available options with noted labels and values
        options = column_options,
            style={'width':'200px',  'margin':'auto', 'display':'inline-block'})],
                 style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center' }
                 )],
            style={'height':40, 'width':250, 'background-color':'lightgray'}),
    html.Div(children=[
        dcc.Graph(id='infrasonido')]),
     html.Div(children=[
        dcc.Graph(id='infrasonido_so2')])
])

@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='infrasonido', component_property='figure'),
    Output(component_id='infrasonido_so2', component_property='figure'),
    Input(component_id='choose_col', component_property='value')
)

def update_plot(selection):

    column = 'Energía MJ'
    if selection:
         column = selection

    figred = go.Figure()

    figred = make_subplots(rows=1, cols=1,
                       subplot_titles=( column + " Vs. Altura (m)",),
                       specs=[[{"secondary_y": True}]])

    figred.update_annotations(font_size=22)

    figred.add_trace(go.Scatter(x=df_new['Fecha'].to_numpy(), y=df_new['Altura (m)'].to_numpy(),
                            name='Altura (m)', mode='markers', marker=dict(color="LightSkyBlue", size=15, opacity=0.4)), secondary_y=False,
                 row=1, col=1)

    figred.add_trace(go.Scatter(x=df_is['Fecha/ Hora UTC'].to_numpy(), y=df_is[column].to_numpy(),
                            mode='lines',
                            name=column, marker=dict(color="MediumPurple")), secondary_y=True,
                 row=1, col=1)

    figred.update_layout(dict(yaxis2={'anchor': 'x', 'overlaying': 'y', 'side': 'left'},
                          yaxis={'anchor': 'x', 'domain': [0.0, 1.0], 'side': 'right'}),
                      font=dict(family="Open Sans, verdana, arial, sans-serif", size=18),
                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Set y-axes titles
    figred.update_yaxes(title_text="Altura (m)", secondary_y=False)
    figred.update_yaxes(title_text=column, secondary_y=True)
    
    figred2 = go.Figure()

    figred2 = make_subplots(rows=1, cols=1, 
                     subplot_titles=(column + " Vs. SO<sup>2</sup> (Ton/día)",),
                     specs=[[{"secondary_y": True}]])

    figred2.update_annotations(font_size=22)

    figred2.add_trace(go.Scatter(x=df_so2['FECHA'].to_numpy(), y=df_so2['Max'].to_numpy(),
                    name='SO<sup>2</sup> (Ton/día)', mode='markers', marker=dict(color="rgb(169,245,196)", size=15, opacity=0.4)), secondary_y=False,
                    row=1, col=1)

    figred2.add_trace(go.Scatter(x=df_is['Fecha/ Hora UTC'].to_numpy(), y=df_is[column].to_numpy(),
                    mode='lines',
                    name='Presión reducida (Pa)', marker=dict(color="MediumPurple")), secondary_y=True,
                    row=1, col=1)

    figred2.update_layout(dict(yaxis2={'anchor': 'x', 'overlaying': 'y', 'side': 'left'},
                  yaxis={'anchor': 'x', 'domain': [0.0, 1.0], 'side':'right'}),
                    font=dict( family="Open Sans, verdana, arial, sans-serif", size=18 ),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Set y-axes titles
    figred2.update_yaxes(title_text='SO<sup>2</sup> (Ton/día)', secondary_y=False)  
    figred2.update_yaxes(title_text=column, secondary_y=True)

    return (figred, figred2)
        

if __name__ == '__main__':
    app.run_server(debug=True)
