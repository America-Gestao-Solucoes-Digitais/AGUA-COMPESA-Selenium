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

# - Login e Senha Base (depois pegar df_login) -
login = "aguaeenergia@magazineluiza.com.br"
senha = "Magazine@2025"

# - URLs de Login -
url_get_login = config.URL_GET_LOGIN
url_post_login = config.URL_POST_LOGIN

driver = Selenium_driver().driver

# Move o mouse e digita algo
campo_login = driver.find_element(By.NAME, "login")
ActionChains(driver).move_to_element(campo_login).click().send_keys(login).perform()

campo_password = driver.find_element(By.NAME, "senha")
ActionChains(driver).move_to_element(campo_password).click().send_keys(senha).perform()

# Encontra o elemento da imagem do CAPTCHA
captcha_img = driver.find_element(By.ID, "loginCaptcha_CaptchaImage")

# Tira screenshot do elemento e salva como JPG
captcha_img.screenshot("images/captcha.jpg")

# Resolvendo o CAPTCHA usando a API do TwoCaptcha
captcha_code = solve_captcha("images/captcha.jpg")

campo_captcha = driver.find_element(By.NAME, "captchaCode")
ActionChains(driver).move_to_element(campo_captcha).click().send_keys(captcha_code).perform()


entrar_button = driver.find_element(By.XPATH, '/html/body/form/div[5]/div/div/div[5]/div/input[1]')
ActionChains(driver).move_to_element(entrar_button).click().perform()

time.sleep(10)