# Importando Modulos
from models.database_mysql_manager import Manage_database
from models.selenium_manager import Selenium_manager
from models.faturas_manager import Faturas_manager
from functions.solver_two_captcha import solve_captcha
from functions.pandas_fuctions import extrai_dados_df_login
import functions.site_functions as site_functions
import os
import config

# Importando bibliotecas
import sys
import os
import tempfile
import pandas as pd

# Colocando a raiz do repositório como o repositório pai
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

'''
Coisas para Criar no código:

- Pegar os dados de login direto pelo banco de dados

- Capturar Referencia (html)
- Capturar Histórico (html)
    - Pegar as faturas dos últimos 6 meses

- Fazer um tratamento de erros:
    - Fazer o WebWait das coisas
    - Try e Except
    - Fazer logs para erros

- Criar um banco de dados (Atualizar para SQL)
    - Faturas já baixadas (Precisa da referencia)
    - insert
'''


# Variaveis de AMBIENTE
dict_elements = config.dict_elenments
img_file_path = config.img_file_path



database_manager = Manage_database()

# Lê a tabela baseado no Distribuidor
df_login = database_manager.read_table('tb_clientes_gestao_faturas', where=config.distribuidora_where)

# Fecha a conexão com o banco de dados
database_manager.close_connection()



# Remove os zeros há esquerda
df_login['INSTALACAO_MATRICULA_PESQUISA'] = df_login['INSTALACAO_MATRICULA'].astype(str).str.lstrip('0')




# Cria um diretório temporário para downloads
temp_dir = tempfile.mkdtemp()

# Ajuste para o primeiro registro do df_login
login_linha_anterior = ''
senha_linha_anterior = ''
driver = ''



for i in range(len(df_login)):

    linha = df_login.iloc[i]

    login, senha, instalacao, instalacao_pesquisa, distribuidora, cliente = extrai_dados_df_login(linha)



    # Verifica se o login e senha do registro atual 
    if login != login_linha_anterior or senha != senha_linha_anterior:

        # Verifica se não é o primeiro registro do df_login
        if driver != '':
            driver.close()

        # Inicializando o driver do Selenium e o driver, além disso retorna o status de carregamento do site 
        selenium_manager_instance = Selenium_manager(temp_dir)
        driver = selenium_manager_instance.driver
        #status = selenium_manager_instance.status



        # Captura code_recaptcha
        Selenium_manager.captura_recaptcha(driver, dict_elements)

        # Resolvendo o CAPTCHA usando a API do TwoCaptcha
        captcha_code = solve_captcha(img_file_path)

        # Faz o login no site 
        status = site_functions.entry_login(driver, dict_elements, login, senha, captcha_code)



    # Entra na página da UC
    status = site_functions.entry_page_uc(driver, dict_elements, instalacao_pesquisa)
    if status == False:
        continue



    # Captura o html da página da UC
    html_page = driver.page_source



    # Abre uma nova conexão com o Banco (Estava dando erro de protocolo do mysql depois de um tempo)
    database_manager = Manage_database()

    # Instancia a classe de controle de faturas
    faturas_manager = Faturas_manager(driver, database_manager, temp_dir, dict_elements, html_page, instalacao, cliente)

    # Pega o status de acordo com uc/referencia
    df_faturas, sem_fatura_aberta = faturas_manager.status_fatura_atual()
    if df_faturas.empty or sem_fatura_aberta:

        if sem_fatura_aberta:
            print('[INFO] Não há faturas em aberto.')
            continue

        continue

    # Pegando, renomeando e movendo as faturas atuais (mais recentes)
    status = faturas_manager.download_fatura_atual()
    if status == False:
        continue

    # Fecha a conexão com o banco de dados
    database_manager.close_connection()



    # Salva o registro atual afim de fazer o compartivo com o próximo registro.
    login_linha_anterior = login
    senha_linha_anterior = senha

# Fecha o driver do Selenium no final do código
driver.quit()
