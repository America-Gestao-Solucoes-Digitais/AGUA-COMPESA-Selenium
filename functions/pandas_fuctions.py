import pandas as pd

def extrai_dados_df_login(linha):

    login = linha['Login']
    senha = linha['Senha']
    instalacao = linha['Matricula']
    instalacao_pesquisa = linha['Matricula_Pesquisa']
    distribuidora = linha['Distribuidora']
    cliente = linha['Cliente']

    instalacao = str(instalacao)

    return login, senha, instalacao, instalacao_pesquisa, distribuidora, cliente

def formatar_datas(df):
    """Converte mm/aaaa para aaaa/mm/dd (dd fixo = 01)"""

    df["data_referencia"] = pd.to_datetime(
        "01/" + df["data_referencia"].astype(str), format="%d/%m/%Y"
    ).dt.strftime("%Y/%m/%d")
    
    return df