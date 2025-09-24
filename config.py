from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()



# Varíaveis do banco de dados (.env)
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD_DB")
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
port = os.getenv("PORT")


# Filtro para a leitura da tabela no SQL
#distribuidora_where = "DISTRIBUIDORA = 'COMPESA' AND GRUPO = 'DASA' AND INSTALACAO_MATRICULA IN ('57869631', '57864060', '57973684', '76312933')"
distribuidora_where = "DISTRIBUIDORA = 'COMPESA' ORDER BY GRUPO, LOGIN, SENHA"

# Obter a chave da API
API_KEY = os.getenv("API_KEY")

# File path do captcha
img_file_path = "images/captcha.jpg"

# Urls base do Site
URL_LOGIN = "https://lojavirtual.compesa.com.br/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"

# --------------- Dicíonario com os elementos do site ---------------

dict_elenments = {
    'ID_image_captcha_login': [By.ID, 'loginCaptcha_CaptchaImage'],
    'NAME_login': [By.NAME, 'login'],
    'NAME_password': [By.NAME, 'senha'],
    'NAME_captcha_code': [By.NAME, 'captchaCode'],
    'XPATH_login_button': [By.XPATH, '/html/body/form/div[5]/div/div/div[5]/div/input[1]'],
    'XPATH_menu_button': [By.XPATH, '//*[@id="btn-side-menu"]/span'],
    'XPATH_side_menu': [By.XPATH, '//*[@id="side-menu"]'],
    'XPATH_download_button': [By.XPATH, '//*[@id="seg-via-conta"]/form/table[1]/tbody/tr/td[3]/div[1]/a'],
    'Dinamic_Selector': By.CSS_SELECTOR, # Somente esse elemento que não foi possível colocar aqui, pois ele é dinamico, está no site_functions.
    'XPATH_Download_button' : [By.XPATH, '//*[@id="seg-via-conta"]/form/table[1]/tbody/tr/td[3]/div[1]/a']
}

