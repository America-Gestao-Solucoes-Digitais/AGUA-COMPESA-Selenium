import pandas as pd

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