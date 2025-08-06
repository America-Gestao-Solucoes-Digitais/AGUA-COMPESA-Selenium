# Importando Modulos
from functions.elements_capture_site import get_elements_html_login
from functions.elements_capture_site import capture_captcha_image
from functions.solver_two_captcha import solve_captcha
from models.selenium_manager import Selenium_driver
import os
import config

# Importando bibliotecas
from requests import Request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
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

# - Login e Senha Base (depois pegar df_login)
login = "aguaeenergia@magazineluiza.com.br"
senha = "Magazine@2025"

# - URLs de Login -
url_get_login = config.URL_GET_LOGIN
url_post_login = config.URL_POST_LOGIN



# Inicializando o Selenium e Capturando dados base para o POST
driver = Selenium_driver(url_get_login).driver

# Encontra o elemento da imagem do CAPTCHA
captcha_img = driver.find_element(By.ID, "loginCaptcha_CaptchaImage")

# Tira screenshot do elemento e salva como JPG
captcha_img.screenshot("images/captcha.jpg")

# Resolvendo o CAPTCHA usando a API do TwoCaptcha
captcha_code = solve_captcha("images/captcha.jpg")

# Capturando os elementos HTML e cookies necessários para o POST
html = driver.page_source
cookies = driver.get_cookies()

# Fazendo a requisição GET e obtendo os elementos HTML necessários para o login
vcid, hs, sp = get_elements_html_login(html)

# Obtendo o valor do cookie JSESSIONID
session_cookie = f"JSESSIONID={cookies[0]['value']}"  



session = requests.Session()

# Construindo payload base para o POST
payload = {
    'login': login,
    'senha': senha,
    'BDC_VCID_loginCaptcha': vcid,
    'BDC_BackWorkaround_loginCaptcha': '1',
    'BDC_Hs_loginCaptcha': hs,
    'BDC_SP_loginCaptcha': sp,
    'captchaCode': captcha_code,
    'jwtGoogle': ''
}

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": session_cookie,
    "Host": "lojavirtual.compesa.com.br",
    "Origin": "https://lojavirtual.compesa.com.br",
    "Referer": "https://lojavirtual.compesa.com.br/gsan/loginPortalAction.do?action=login",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    ),
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
    }

result_login = session.post(url_post_login, data=payload, headers=header)

print(result_login.status_code)

with open("result_login.html", "w", encoding='utf-8') as f:
    f.write(result_login.text)

time.sleep(10)