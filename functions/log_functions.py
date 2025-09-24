import pandas as pd
from datetime import datetime

def cria_df_log():
    '''Cria o Dataframe de logs.'''

    log_df = pd.DataFrame(columns=["timestamp", "primary_key", "status", "function", "message"])
    return log_df

def registrar_linha_df_log(df_log, uc, status, funcao, mensagem):
    '''Registra uma nova linha no Dataframe de logs.'''

    # Retorna o error
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{status}] ({funcao}) {mensagem}")
    print('')
    print('-----------------------------------------------------------------------')

    # Forma da linha
    nova_linha = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "codigo_instalacao": uc,
        "status": status,
        "function": funcao,
        "message": mensagem
    }

    return pd.concat([df_log, pd.DataFrame([nova_linha])], ignore_index=True)