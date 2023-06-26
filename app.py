## BIBLIOTECAS
from urllib.parse import urlparse
import mysql.connector
import pandas as pd
import os

## VARIAVEIS

## CAMINHOS
path_planilha = r'C:\Users\mathe\OneDrive\Área de Trabalho\DESPESAS_MENSAIS.xlsx'

## DADOS BASE PARA O MYSQL
# LEITURA DA PLANILHAS
df = pd.read_excel(path_planilha, sheet_name='BD_DESPESAS')

df = df.rename(columns={
    'CONTA':'DS_DESPESA',
    'R$':'VR_DESPESA',
    'DATA VENCIMENTO':'DT_VENCIMENTO',
    'ANO VENCIMENTO':'DT_ANO_VECIMENTO',
    'MÊS VENCIMENTO':'DT_MES_VECIMENTO',
    'ATRASO':'QT_DIAS_ATRASO',
    'STATUS':'ST_VENCIMENTO',
    'DATA DE PAMENTO':'DT_PAGAMENTO',
    'ANO PAGAMENTO':'DT_ANO_PAGAMENTO',
    'MÊS PAGAMENTO':'DT_MES_PAGAMENTO',
    'DIA PAGAMENTO':'DT_DIA_PAGAMENTO',
    'PERIODO':'DT_PERIODO',
    'TIPO':'ST_PAGAMENTO',
    'QUEM':'NM_PAGADOR'
})

## CONEXAO MYSQL
# LEITURA DO ARQUIVO .ENV
database_url = os.getenv("DATABASE_URL")

# COMPOR A URL DE CONEXAO
url_components = urlparse(database_url)
conn = mysql.connector.connect(
    host=url_components.hostname,
    port=url_components.port,
    user=url_components.username,
    password=url_components.password,
    database=url_components.path[1:]
)

# ABERTURA DO CURSO
curso = conn.cursor()

# FUNCAO PARA CRIAR TABELA NO MYSQL
def CriarTabelaDoZero(df, nome_tabela, database_url):
    df.to_sql(nome_tabela, database_url, index=False, if_exists='replace')

# FUNCAO PARA APPENDAR NOVOS DADOS NA TABELA
def AppendNovosDados(df, nome_tabela, database_url):
    # LER A TABELA NO MYSQL
    df_sql = pd.read_sql(nome_tabela, con=database_url)
    # CRIAR O LEFTANTI DO BANCO PARA A PLANILHA
    merge_leftanti = df.merge(df_sql, on=['DS_DESPESA', 'VR_DESPESA', 'DT_VENCIMENTO'], how='left', indicator=True)
    df_geral = merge_leftanti[merge_leftanti['_merge'] == 'left_only']
    #APPENDAR OS DADOS NO MYSQL
    df_geral.to_sql(nome_tabela, database_url, if_exists='append', index=False)