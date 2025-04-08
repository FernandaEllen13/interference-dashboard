import pandas as pd
import pytest

#simulando dados de entrada
@pytest.fixture
def df_mock():
    return pd.DataFrame({
        'nome_do_site': ['SPABC01', 'MGBHZ02', 'RJRIO03', 'SPXYZ04', 'MGABC05'],
        'valor_interferencia': [-108, -112, -109, -115, -107]
    })

#T1 - verifica se o DataFrame possui as colunas esperadas
def test_colunas_esperadas(df_mock):
    assert 'nome_do_site' in df_mock.columns
    assert 'valor_interferencia' in df_mock.columns

#T2 - verifica se a média está correta
def test_media_interferencia(df_mock):
    media = df_mock['valor_interferencia'].mean()
    assert round(media, 2) == -110.2

#T3 - máximo e mínimo
def test_max_min(df_mock):
    assert df_mock['valor_interferencia'].max() == -107
    assert df_mock['valor_interferencia'].min() == -115

#T4 - porcentagem de interferência acima de -110
def test_percentual_acima_limite(df_mock):
    total = len(df_mock)
    acima = len(df_mock[df_mock['valor_interferencia'] > -110])
    percentual = (acima / total) * 100
    assert 0 <= percentual <= 100

#T5 - agrupamento por estado
def test_agrupamento_estado(df_mock):
    df_mock['estado'] = df_mock['nome_do_site'].str[:2]
    estados = df_mock.groupby('estado').size().to_dict()
    assert estados == {'SP': 2, 'MG': 2, 'RJ': 1}

# T6 - filtro por estado
def test_filtro_estado(df_mock):
    df_mock['estado'] = df_mock['nome_do_site'].str[:2]
    sp_sites = df_mock[df_mock['estado'] == 'SP']
    assert len(sp_sites) == 2

#T7 - filtro por alta interferência (> -110 dBm)
def test_filtro_interferencia(df_mock):
    filtrado = df_mock[df_mock['valor_interferencia'] > -110]
    assert set(filtrado['nome_do_site']) == {'SPABC01', 'RJRIO03', 'MGABC05'}

#T8 - confere se estados únicos estão corretos
def test_estados_unicos(df_mock):
    df_mock['estado'] = df_mock['nome_do_site'].str[:2]
    estados = sorted(df_mock['estado'].unique())
    assert estados == ['MG', 'RJ', 'SP']

#T9 - verifica se o número total de linhas está certo
def test_numero_total_linhas(df_mock):
    assert len(df_mock) == 5

#T10 - garante que nenhum valor está fora da faixa aceitável (-150 a -50 dBm)
def test_valores_dentro_de_faixa(df_mock):
    assert df_mock['valor_interferencia'].between(-150, -50).all()
