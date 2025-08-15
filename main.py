# Importando Modulos
from models.selenium_manager import Selenium_manager
from models.faturas_manager import Faturas_manager
from functions.solver_two_captcha import solve_captcha
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

- Capturar Status
    - Fazer inserção dos status
- Capturar Referencia (html) 
- Capturar Histórico (html)
    - Pegar as faturas dos últimos 6 meses

- Fazer um tratamento de erros:
    - Fazer o WebWait das coisas
    - Try e Except
    - Fazer logs para erros

- Criar um banco de dados ACCESS (temporário) (EXCEL) (Atualizar para SQL)
    - Status
    - Faturas já baixadas
    - insert
'''



# Variaveis de AMBIENTE
dict_elements = config.dict_elenments
img_file_path = config.img_file_path

df_login = pd.read_excel('teste.xlsx')
df_login_base = df_login

# Remove os zeros há esquerda
df_login['Matricula'] = df_login['Matricula'].astype(str).str.lstrip('0')

# Cria um diretório temporário para downloads
temp_dir = tempfile.mkdtemp()



# Ajuste para o primeiro registro do df_login
login_linha_anterior = ''
senha_linha_anterior = ''
driver = ''



for i in range(len(df_login)):

    linha = df_login.iloc[i]

    login = linha['Login']
    senha = linha['Senha']
    instalacao = linha['Matricula']
    distribuidora = linha['Distribuidora']
    cliente = linha['Cliente']

    instalacao = str(instalacao)



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
    status = site_functions.entry_page_uc(driver, dict_elements, instalacao)
    if status == False:
        continue



    # Captura o html da página
    html_page = driver.page_source

    # Instancia a classe de controle de faturas
    faturas_manager = Faturas_manager(driver, temp_dir, dict_elements, html_page, instalacao, cliente)

    # Pega o status de acordo com uc/referencia
    df_faturas, fatura_aberta = faturas_manager.status_fatura_atual()
    if df_faturas.empty or fatura_aberta:
        continue

    # Pegando, renomeando e movendo as faturas atuais (mais recentes)
    status = faturas_manager.download_fatura_atual()
    if status == False:
        continue



    # Salva o registro atual afim de fazer o compartivo com o próximo registro.
    login_linha_anterior = login
    senha_linha_anterior = senha

driver.quit()
