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

# Se conecta no banco de dados e pega os dados de login
database_manager = Manage_database()
df_login = database_manager.read_table('tb_clientes_gestao_faturas', where=config.distribuidora_where)
database_manager.close_connection()

# Remove os zeros há esquerda (afim de bater com o dados do site)
df_login['INSTALACAO_MATRICULA_PESQUISA'] = df_login['INSTALACAO_MATRICULA'].astype(str).str.lstrip('0')

# Cria um diretório temporário para downloads de faturas
# Diretorio base para o Selenium
temp_dir = tempfile.mkdtemp()

# Declarando variaveis para controle de login
login_linha_anterior = ''
senha_linha_anterior = ''
driver = ''

# Loop para cada registro do df_login
for i in range(len(df_login)):

    # Pegando os dados do registro atual
    linha = df_login.iloc[i]
    login, senha, instalacao, instalacao_pesquisa, distribuidora, cliente = extrai_dados_df_login(linha)

    # Verifica se o login e senha do registro atual são diferentes do registro anterior
    if login != login_linha_anterior or senha != senha_linha_anterior:

        # Verifica se não é o primeiro registro (driver não inicializado)
        if driver != '':
            driver.close()

        # Inicializando o driver do Selenium e o driver, além disso retorna o status de carregamento do site 
        selenium_manager_instance = Selenium_manager(temp_dir)
        driver = selenium_manager_instance.driver
        status = selenium_manager_instance.status

        # Captura code_recaptcha, resolve o recaptcha e faz o login no site
        Selenium_manager.captura_recaptcha(driver, dict_elements)
        captcha_code = solve_captcha(img_file_path)
        status = site_functions.entry_login(driver, dict_elements, login, senha, captcha_code)

        # Salva o registro atual afim de fazer o compartivo com o próximo registro.
        login_linha_anterior = login
        senha_linha_anterior = senha

    # Entra na página da UC
    status = site_functions.entry_page_uc(driver, dict_elements, instalacao_pesquisa)
    if status == False:
        continue

    # Pegando o HTML da página da UC
    html_page = driver.page_source

    # Abre uma nova conexão com o Banco (Estava dando erro de protocolo do mysql depois de um tempo)
    database_manager = Manage_database()

    # Instancia a classe de controle de faturas
    faturas_manager = Faturas_manager(driver, database_manager, temp_dir, dict_elements, html_page, instalacao, cliente)

    # Verifica o status se tem faturas abertas 
    df_faturas, faturas_abertas = faturas_manager.status_fatura_atual()
    if faturas_abertas.empty:
        print('[INFO] Não há faturas em aberto.')
        continue


    # Pegando, renomeando e movendo as faturas atuais (mais recentes)
    status = faturas_manager.download_fatura_atual()
    if status == False:
        continue

    database_manager.close_connection()

# Fecha o driver do Selenium no final do código
driver.quit()
