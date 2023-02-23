import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html

# Reading data using pandas
df_new = pd.read_excel('DatosGraficarConInfrasonidos.xlsx',sheet_name = 'Hoja1')
df2 = pd.read_excel('senales_infrasonido_2020_2022.xlsx',sheet_name = 'Hoja1')
df2 = df2[df2['Energía MJ '] < 124 ]

fig3 = go.Figure()

fig3 = make_subplots(rows=1, cols=1, 
                     subplot_titles=("Presión Máxima Pa Vs. Altura (m)",),
                     specs=[[{"secondary_y": True}]])

fig3.update_annotations(font_size=22)

fig3.add_trace(go.Scatter(x=df_new['Fecha'].to_numpy(), y=df_new['Altura (m)'].to_numpy(),
                    name='Altura (m)', mode='markers', marker=dict(color="LightSkyBlue", size=15, opacity=0.4)), secondary_y=False,
                    row=1, col=1)

fig3.add_trace(go.Scatter(x=df2['Fecha'].to_numpy(), y=df2['Presión Máxima Pa'].to_numpy(),
                    mode='lines',
                    name='Presión Máxima Pa', marker=dict(color="MediumPurple")), secondary_y=True,
                    row=1, col=1)

fig3.update_layout(dict(yaxis2={'anchor': 'x', 'overlaying': 'y', 'side': 'left'},
                  yaxis={'anchor': 'x', 'domain': [0.0, 1.0], 'side':'right'}),
                   font=dict( family="Open Sans, verdana, arial, sans-serif", size=18 ))

# Set y-axes titles
fig3.update_yaxes(title_text="Altura (m)", secondary_y=False)
fig3.update_yaxes(title_text="Presión Máxima Pa", secondary_y=True)


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
        dcc.Graph(id='infrasonido',figure=fig3)])
])

# app.layout = html.Div(children=[
#     html.Div(style={'height': 250, 'width': 250, 'background-color': 'red'}),
#     html.Div(children=[
#         html.H1("This box"),
#         html.H2("Another Title"),
#         dcc.Graph(id='infrasonido',figure=fig3)],
#         style={'background-color': 'lightblue'})
# ])


if __name__ == '__main__':
    app.run_server(debug=True)
