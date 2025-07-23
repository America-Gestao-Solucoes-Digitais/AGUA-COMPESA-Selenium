# Importando Modulos
from functions.elements_capture_site import get_elements_html_login
from functions.elements_capture_site import capture_captcha_image
from functions.solver_two_captcha import solve_captcha
import os
import config

# Importando bibliotecas
import requests
import sys
import os

# Colocando a raiz do repositório como o repositório pai
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

'''
Base para o POST:

Tipo de requisição POST Nécessária:
login: aguaeenergia@magazineluiza.com.br (DataBase) (FEITO)
senha: Magazine@2025 (DataBase) (FEITO)
BDC_VCID_loginCaptcha: 2a06f74b4ff8487fa39709926bfe6b47 (Request) (FEITO)
BDC_BackWorkaround_loginCaptcha: 1 (Default) (FEITO)
BDC_Hs_loginCaptcha: 892eeaa9a5863c1b1fdc09b568ea5b990d0797b1 (Request) (FEITO)
BDC_SP_loginCaptcha: 568668182 (Request) (FEITO)
captchaCode: dv34 (Captcha - 2Captcha)
jwtGoogle: (Default)
'''

# Variaveis de AMBIENTE

# - Login e Senha Base (depois pegar df_login) -
login = "aguaeenergia@magazineluiza.com.br"
senha = "Magazine@2025"

# - URLs de Login -
url_get_login = config.URL_GET_LOGIN
url_post_login = config.URL_POST_LOGIN

# Inicializando request session
session = requests.Session()
session.headers.update(config.headers)

# Fazendo a requisição GET e obtendo os elementos HTML necessários para o login
vcid, hs, sp, img_tag = get_elements_html_login(session, url_get_login)

# Capturando a imagem e retornando o caminho da imagem
path_img = capture_captcha_image(img_tag, url_get_login)

# Resolvendo o CAPTCHA usando a API do TwoCaptcha
recaptcha_code = solve_captcha(path_img)

# deletar o arquivo de imagem após o uso (ou usar o diretorio temporário)

# Construindo payload base para o POST
payload = {
    'login': login,
    'senha': senha,
    'BDC_VCID_loginCaptcha': vcid,
    'BDC_BackWorkaround_loginCaptcha': '1',
    'BDC_Hs_loginCaptcha': hs,
    'BDC_SP_loginCaptcha': sp,
    'captchaCode': recaptcha_code,
    'jwtGoogle': ''
}

print(f'Recaptcha Code: {recaptcha_code}')

result_login = requests.post(url_post_login, data=payload, headers=config.headers, allow_redirects=True)

print(f"Status Code: {result_login.status_code}")
print("")
print(f"Response Text: {result_login.text}")
