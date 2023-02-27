import pandas as pd
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


column_options = [{'label': 'Energía MJ', 'value': 'Energía MJ '},
                  {'label': 'Presión Máxima Pa', 'value': 'Presión Máxima Pa'},
                  {'label': 'Presión Reducida Pa', 'value': 'Presión Reducida Pa'}]
column_names = ['Energía MJ ', 'Presión Máxima Pa', 'Presión Reducida Pa']

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div(children=[
    html.Img(src='https://www2.sgc.gov.co/Style%20Library/themes/Intranet/images/logo-b.png')], 
             style={'height':120, 'width':250, 'background-color':'lightgray'}),
    html.H1("Nueva visualización"),
    # Add a dropdown with identifier
    dcc.Dropdown(id='choose_col',
        # Set the available options with noted labels and values
        options = column_options,
            style={'width':'200px', 'margin':'0 auto'}),
    html.Div(children=[
        dcc.Graph(id='infrasonido')])
])

@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='infrasonido', component_property='figure'),
    Input(component_id='choose_col', component_property='value')
)
def update_plot(selection):
    column = 'Presión Máxima Pa'
    if selection:
        column = selection
    
    fig3 = go.Figure()

    fig3 = make_subplots(rows=1, cols=1, 
                     subplot_titles=( column + " Vs. Altura (m)",),
                     specs=[[{"secondary_y": True}]])

    fig3.update_annotations(font_size=22)

    fig3.add_trace(go.Scatter(x=df_new['Fecha'].to_numpy(), y=df_new['Altura (m)'].to_numpy(),
                    name='Altura (m)', mode='markers', marker=dict(color="LightSkyBlue", size=15, opacity=0.4)), secondary_y=False,
                    row=1, col=1)

    fig3.add_trace(go.Scatter(x=df2['Fecha'].to_numpy(), y=df2[column].to_numpy(),
                    mode='lines',
                    name=column, marker=dict(color="MediumPurple")), secondary_y=True,
                    row=1, col=1)

    fig3.update_layout(dict(yaxis2={'anchor': 'x', 'overlaying': 'y', 'side': 'left'},
                  yaxis={'anchor': 'x', 'domain': [0.0, 1.0], 'side':'right'}),
                   font=dict( family="Open Sans, verdana, arial, sans-serif", size=18 ))

# Set y-axes titles
    fig3.update_yaxes(title_text="Altura (m)", secondary_y=False)
    fig3.update_yaxes(title_text=column, secondary_y=True)  
    
    return fig3  
        

if __name__ == '__main__':
    app.run_server(debug=True)
