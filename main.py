# Importando Modulos
from functions.solver_two_captcha import solve_captcha
from models.selenium_manager import Selenium_driver
import os
import config

# Importando bibliotecas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
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

Coisas para Criar no código

- Fazer com que o código pegue mais de uma mátricula no mesmo login
    - Tirar o pop-up e manter a página principal
    - fazer um loop que identifique a próxima UC do mesmo login

- Verificar de login e senha (Afim de manter na mesma Sessão)
    - Necessário criar uma base de dados teste
    - Criar um repositorio temporario

- Criar Validador de excessões afim de continuar o código

- Criar um dataframe com os logs (facilitar a manutenção dos logins e do código)

- Criar um banco de dados ACCESS (temporário)
    - Status
    - Faturas já baixadas
    - insert
'''



# Variaveis de AMBIENTE

# - Login e Senha Base (depois pegar df_login) - (DEPOIS FAZER UM SELECT QUE ORDERNE POR LOGIN E SENHA)
login = "aguaeenergia@magazineluiza.com.br"
senha = "Magazine@2025"
uc = '2749351'


# URLs de Login
url_get_login = config.URL_GET_LOGIN
url_post_login = config.URL_POST_LOGIN

# Inicializando o driver do Selenium
driver = Selenium_driver().driver



# Encontra o elemento da imagem do CAPTCHA
captcha_img = driver.find_element(By.ID, "loginCaptcha_CaptchaImage")

# Tira screenshot do elemento e salva como JPG
captcha_img.screenshot("images/captcha.jpg")

# Resolvendo o CAPTCHA usando a API do TwoCaptcha
captcha_code = solve_captcha("images/captcha.jpg")



# Faz o login no site
campo_login = driver.find_element(By.NAME, "login")
ActionChains(driver).move_to_element(campo_login).click().send_keys(login).perform()

campo_password = driver.find_element(By.NAME, "senha")
ActionChains(driver).move_to_element(campo_password).click().send_keys(senha).perform()

campo_captcha = driver.find_element(By.NAME, "captchaCode")
ActionChains(driver).move_to_element(campo_captcha).click().send_keys(captcha_code).perform()

entrar_button = driver.find_element(By.XPATH, '/html/body/form/div[5]/div/div/div[5]/div/input[1]')
ActionChains(driver).move_to_element(entrar_button).click().perform()

# Espera o carregamento da página após o login
time.sleep(2)



html_pos_login = driver.page_source
soup = BeautifulSoup(html_pos_login, "html.parser")

menu_button = driver.find_element(By.XPATH, '//*[@id="btn-side-menu"]/span')
menu_button.click()
time.sleep(1)

if uc:
    seletor = f'a.list-group-item[data-value="{uc}"]'
    wait = WebDriverWait(driver, 10)

    el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
    driver.execute_script("arguments[0].scrollIntoView(true);", el)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
    driver.execute_script("arguments[0].click();", el)
    time.sleep(1)

# Salva a janela original
janela_principal = driver.current_window_handle

menu_button = driver.find_element(By.XPATH, '//*[@id="seg-via-conta"]/form/table[1]/tbody/tr/td[3]/div[1]/a')
menu_button.click()

# Aguarda a nova janela abrir
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

# Identifica a nova janela (popup)
for handle in driver.window_handles:
    if handle != janela_principal:
        popup = handle
        break

# Alterna para o popup
driver.switch_to.window(popup)

print("🪟 Popup aberto:", driver.title)

# Aguarda carregar a fatura (ou download)
time.sleep(3)

# Fecha o popup
driver.close()  # <- FECHA SOMENTE A JANELA ATUAL (popup)

# Volta para a janela principal
driver.switch_to.window(janela_principal)

driver.refresh()
time.sleep(3)
# ---------------------- UC

uc = '1759'

menu_button = driver.find_element(By.XPATH, '//*[@id="btn-side-menu"]/span')
menu_button.click()
time.sleep(1)

if uc:
    seletor = f'a.list-group-item[data-value="{uc}"]'
    wait = WebDriverWait(driver, 10)

    el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
    driver.execute_script("arguments[0].scrollIntoView(true);", el)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
    driver.execute_script("arguments[0].click();", el)
    time.sleep(1)

# Salva a janela original
janela_principal = driver.current_window_handle

menu_button = driver.find_element(By.XPATH, '//*[@id="seg-via-conta"]/form/table[1]/tbody/tr/td[3]/div[1]/a')
menu_button.click()

# Aguarda a nova janela abrir
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

# Identifica a nova janela (popup)
for handle in driver.window_handles:
    if handle != janela_principal:
        popup = handle
        break

# Alterna para o popup
driver.switch_to.window(popup)

print("🪟 Popup aberto:", driver.title)

# Aguarda carregar a fatura (ou download)
time.sleep(3)

# Fecha o popup
driver.close()  # <- FECHA SOMENTE A JANELA ATUAL (popup)

# Volta para a janela principal
driver.switch_to.window(janela_principal)



time.sleep(2)

driver.quit()
