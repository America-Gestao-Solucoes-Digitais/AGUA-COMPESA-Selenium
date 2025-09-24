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

    status = False

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

        status = True
        return status

    except Exception as e:
        print(f"[ERRO] entry_login: {e}")
        status = False

        return status



def entry_page_uc(driver, dict_elements, instalacao_pesquisa, timeout=10):
    """
    Entra no Menu, tenta encontrar a UC, se caso tenha a UC prossegue para a página dela.
    Lida com elemento dinâmico que pode precisar de scroll.
    """

    status = True  # Define status padrão

    try:
        # Abre o menu
        menu_button = driver.find_element(
            dict_elements['XPATH_menu_button'][0],
            dict_elements['XPATH_menu_button'][1]
        )
        menu_button.click()

        # Define seletor dinâmico
        selector = f'a.list-group-item[data-value="{instalacao_pesquisa}"]'
        wait = WebDriverWait(driver, timeout)

        # Espera o container que contém as UCs
        container = wait.until(
            EC.presence_of_element_located(
                (dict_elements['Dinamic_Selector'], selector)
            )
        )

        # Tenta rolar até o elemento ser clicável
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                time.sleep(0.5)  # Pequena pausa para evitar sobrecarga
                el = driver.find_element(dict_elements['Dinamic_Selector'], selector)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                wait.until(EC.element_to_be_clickable((dict_elements['Dinamic_Selector'], selector)))
                driver.execute_script("arguments[0].click();", el)
                
                break  # Sai do loop
            except:
                # Se não encontrou, rola mais um pouco
                driver.execute_script("arguments[0].scrollTop += 100;", container)
                time.sleep(0.2)

    except Exception as e:
        print(f"[ERRO] UC não encontrada.")
        status = False

    time.sleep(3)

    return status
