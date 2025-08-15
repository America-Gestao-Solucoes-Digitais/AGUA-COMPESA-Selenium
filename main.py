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
- Capturar Referencia

- Hístorico
    - Pegar as faturas dos últimos 6 meses

- Fazer o WebWait das coisas (FEITO)
- Pegar o Status e a Nomeclatura da Fatura Correta (FEITO)
- Pegar as Faturas e construir a classe de Faturas (FEITO)

- Fazer com que o código pegue mais de uma mátricula no mesmo login
    - Tirar o pop-up e manter a página principal (FEITO)
    - fazer um loop que identifique a próxima UC do mesmo login

- Verificar de login e senha (Afim de manter na mesma Sessão)
    - Necessário criar uma base de dados teste
    - Criar um repositorio temporario

- Criar um banco de dados ACCESS (temporário) (EXCEL)
    - Status
    - Faturas já baixadas
    - insert

PRÓXIMOS PASSOS:
- Ver as Faturas de Hístorico, pegar faturas que não estão no principal

FIRULA:
- Criar um dataframe com os logs (facilitar a manutenção dos logins e do código)
- Criar Validador de excessões afim de continuar o código e ser base para os logs
    - Try e Except
- Criar um log de quais não estão em dia, quais são as faltantes.

'''

# Variaveis de AMBIENTE
dict_elements = config.dict_elenments
img_file_path = config.img_file_path

df_login = pd.read_excel('teste.xlsx')

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


    # Instancia a classe de controle de faturas
    faturas_manager = Faturas_manager(driver, temp_dir, instalacao, dict_elements, cliente)

    # Salva o registro atual afim de fazer o compartivo com o próximo registro.
    login_linha_anterior = login
    senha_linha_anterior = senha


driver.quit()
