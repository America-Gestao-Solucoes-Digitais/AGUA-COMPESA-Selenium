import pandas as pd

def ajusta_df_login(df):
    '''
    Ajusta o DataFrame de login para o formato correto.
    
    - Tira o zero a esquerda da coluna 'INSTALACAO_MATRICULA' e cria a coluna 'INSTALACAO_MATRICULA_PESQUISA'.
    - Ordena o DataFrame por 'LOGIN', 'SENHA' e 'INSTALACAO_MATRICULA_PESQUISA', afim de facilitar a busca no site.
    '''

    # Remove os zeros há esquerda (afim de bater com o dados do site)
    df['INSTALACAO_MATRICULA_PESQUISA'] = df['INSTALACAO_MATRICULA'].astype(str).str.lstrip('0')

    # Transforma em int para facilitar o sort e depois volta para str
    # (Facilita na hora de encontrar os valores de 'INSTALACAO_MATRICULA_PESQUISA' no site)
    df['INSTALACAO_MATRICULA_PESQUISA'] = df['INSTALACAO_MATRICULA_PESQUISA'].astype(int)
    df = df.sort_values(by=['LOGIN', 'SENHA', 'INSTALACAO_MATRICULA_PESQUISA'])
    df['INSTALACAO_MATRICULA_PESQUISA'] = df['INSTALACAO_MATRICULA_PESQUISA'].astype(str)

    return df


def extrai_dados_df_login(linha):

    login = linha['LOGIN']
    senha = linha['SENHA']
    instalacao = linha['INSTALACAO_MATRICULA']
    instalacao_pesquisa = linha['INSTALACAO_MATRICULA_PESQUISA'] # Tira os zeros a esquerda, afim de bater com os dados do site
    distribuidora = linha['DISTRIBUIDORA']
    cliente = linha['GRUPO']

    instalacao = str(instalacao)

    return login, senha, instalacao, instalacao_pesquisa, distribuidora, cliente

def formatar_datas(df):
    """Converte mm/aaaa para aaaa/mm/dd (dd fixo = 01)"""

    df["data_referencia"] = pd.to_datetime(
        "01/" + df["data_referencia"].astype(str), format="%d/%m/%Y"
    ).dt.strftime("%Y/%m/%d")
    
    return df