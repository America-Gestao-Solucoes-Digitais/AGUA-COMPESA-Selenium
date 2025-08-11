# Importando Modulos
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

def entry_login(driver, dict_elements, login, password, captcha_code):
    '''
    Encontra os elementos de login do navegador, inputa os dados e faz login.
    '''

    try:
        # Encontra o campo e da input
        campo_login = driver.find_element(dict_elements['NAME_login'][0], dict_elements['NAME_login'][1])
        ActionChains(driver).move_to_element(campo_login).click().send_keys(login).perform()

        campo_password = driver.find_element(dict_elements['NAME_password'][0], dict_elements['NAME_password'][1])
        ActionChains(driver).move_to_element(campo_password).click().send_keys(password).perform()

        campo_captcha = driver.find_element(dict_elements['NAME_captcha_code'][0], dict_elements['NAME_captcha_code'][1])
        ActionChains(driver).move_to_element(campo_captcha).click().send_keys(captcha_code).perform()

        login_button = driver.find_element(dict_elements['XPATH_login_button'][0], dict_elements['XPATH_login_button'][1])
        ActionChains(driver).move_to_element(login_button).click().perform()
    
        # Verificar se realmente foi feito o login (Não um falso verdadeiro)

        return status

    except Exception as e:
        print(f"[ERRO] entry_login: {e}")
        status = False

        return status



def entry_page_uc(driver, dict_elements, instalacao):
    '''
    Entra no Menu, tenta encontrar a UC, se caso tenha a UC prossegui para a página dela.
    '''

    # Encontra e clica na UC
    menu_button = driver.find_element(dict_elements['XPATH_menu_button'][0], dict_elements['XPATH_menu_button'][1])
    menu_button.click()

    # Tenta encontrar a UC na lista
    selector = f'a.list-group-item[data-value="{instalacao}"]'
    wait = WebDriverWait(driver, 10)

    # Espera carregar a UC na lista
    el = wait.until(EC.presence_of_element_located((dict_elements['Dinamic_Selector'], selector)))

    # Scrolla a página a fim de encontrar o elemento da UC na aba de Menu, clica no elemento quando aparece
    driver.execute_script("arguments[0].scrollIntoView(true);", el)
    wait.until(EC.element_to_be_clickable((dict_elements['Dinamic_Selector'], selector)))
    driver.execute_script("arguments[0].click();", el)
    
    # Esperando a atualização da página
    time.sleep(1)