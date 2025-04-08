#imports para o Dash(interface web) e análise de dados
import dash
from dash import html, dcc, Output, Input, State, dash_table
import pandas as pd
import plotly.express as px
import base64
import io

#inicializando app com dash
app = dash.Dash(__name__)

#layout da página principal com Dash
app.layout = html.Div([
    html.H1("📡 Monitoramento de Interferência em Sites de Telecom", style={'textAlign': 'center', 'marginBottom': '20px'}),

    #componente: upload CSV
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Arraste ou selecione um arquivo CSV']),
        style={
            'width': '60%', 'margin': 'auto', 'height': '60px',
            'lineHeight': '60px', 'borderWidth': '2px',
            'borderStyle': 'dashed', 'borderRadius': '10px',
            'textAlign': 'center', 'backgroundColor': '#f9f9f9', 'cursor': 'pointer'
        },
        multiple=False
    ),

    #resumo das estastísticas
    html.Div(id='stats-summary', style={'width': '80%', 'margin': '30px auto'}),

    #filtros: dropdown de estado e checklist de interferência
    html.Div([
        html.Div([
            html.Label('Filtrar por Estado:'),
            dcc.Dropdown(id='dropdown-estado')
        ], style={'width': '40%', 'display': 'inline-block', 'paddingRight': '20px'}),

        html.Div([
            dcc.Checklist(
                options=[{'label': 'Mostrar apenas alta interferência (> -110 dBm)', 'value': 'filtrar'}],
                id='checklist-interferencia',
                value=[]
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'width': '80%', 'margin': 'auto'}),

    #gráfico da interferência
    dcc.Graph(id='grafico'),

    #tabela com dados do CSV
    html.H3("Tabela de Sites", style={'textAlign': 'center'}),
    html.Div(id='tabela-dados', style={'width': '90%', 'margin': 'auto'})
])

#DataFrame que armazena os dados do CSV
df_global = pd.DataFrame()

#callback que vai atualizando tudo com base nos dados:
@app.callback(
    [Output('dropdown-estado', 'options'),
     Output('dropdown-estado', 'value'),
     Output('grafico', 'figure'),
     Output('tabela-dados', 'children'),
     Output('stats-summary', 'children')],
    [Input('upload-data', 'contents'),
     Input('dropdown-estado', 'value'),
     Input('checklist-interferencia', 'value')],
    [State('upload-data', 'filename')]
)
def atualizar_dashboard(contents, estado_sel, checklist_val):
    global df_global
    if contents is not None:
        # Converte o conteúdo base64 em texto e carrega no pandas
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        df.columns = df.columns.str.lower()  # Normaliza os nomes das colunas

        # Verificação de colunas obrigatórias no CSV
        if 'nome_do_site' not in df or 'valor_interferencia' not in df:
            return [], None, {}, html.Div("CSV inválido."), html.Div()

        # Cria coluna 'estado' a partir dos dois primeiros caracteres do nome do site
        df['estado'] = df['nome_do_site'].str[:2]
        df_global = df.copy()

    if df_global.empty:
        return [], None, {}, html.Div(), html.Div()

    #aplica os filtros:
    df = df_global.copy()
    if estado_sel:
        df = df[df['estado'] == estado_sel]

    if 'filtrar' in checklist_val:
        df = df[df['valor_interferencia'] > -110]

    #gráfico de barras(Plotfy)
    fig = px.bar(
        df,
        x='nome_do_site',
        y='valor_interferencia',
        labels={'valor_interferencia': 'Interferência (dBm)', 'nome_do_site': 'Site'},
        color='valor_interferencia',
        color_continuous_scale='plasma'
    )
    fig.update_layout(
        yaxis=dict(range=[-120, -100])  # Define escala do eixo Y para padronizar visualização
    )

    #criação da tabela de dados:
    tabela = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10
    )

    #estatísticas:
    media = df_global['valor_interferencia'].mean()
    max_val = df_global['valor_interferencia'].max()
    min_val = df_global['valor_interferencia'].min()
    total = len(df_global)
    acima_limite = len(df_global[df_global['valor_interferencia'] > -110])
    perc = (acima_limite / total) * 100 if total > 0 else 0
    por_estado = df_global.groupby('estado').size().reset_index(name='quantidade')

    #resumo estatístico:
    stats = html.Div([
        html.H3("Resumo Estatístico", style={'textAlign': 'center'}),
        html.Ul([
            html.Li(f"Média de interferência: {media:.2f} dBm"),
            html.Li(f"Interferência máxima (pior): {max_val} dBm"),
            html.Li(f"Interferência mínima (melhor): {min_val} dBm"),
            html.Li(f"{perc:.1f}% dos sites têm interferência acima de -110 dBm"),
            html.Li("Quantidade de sites por estado: " + ", ".join([f"{row['estado']} ({row['quantidade']})" for _, row in por_estado.iterrows()]))
        ])
    ], style={'backgroundColor': '#f3f3f3', 'padding': '20px', 'borderRadius': '10px'})

    #preenche as opções do dropdown de estados com base nos dados únicos
    estados = [{'label': uf, 'value': uf} for uf in sorted(df_global['estado'].unique())]
    return estados, estado_sel, fig, tabela, stats

if __name__ == '__main__':
    app.run(debug=True)
