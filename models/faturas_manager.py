# Importando Modulos
import functions.file_functions as file_functions

# Importando bibliotecas
from selenium.webdriver.support.ui import WebDriverWait
#import time

class Faturas_manager:

    def __init__(self, driver, temp_dir, instalacao, dict_elements):
        
        # Váriaveis de ambiente
        self.driver = driver
        self.temp_dir = temp_dir

        # Configurações de elementos da página web
        self.dict_elements = dict_elements

        # Trazendo dados de Faturas
        self.instalacao = instalacao
        self.distribuidora = 'COMPENSA'


        self.download_fatura()
    


    def download_fatura(self):
        '''
        Passo a Passo:
        - Apertar o botão de download
        - Faz abri o popup
        - Faz o download da fatura
        - Fecha o popup
        '''

        # Salva a Janela atual como principal
        janela_principal = self.driver.current_window_handle

        # Clica no botão de download
        download_button = self.driver.find_element(self.dict_elements['XPATH_Download_button'][0], self.dict_elements['XPATH_Download_button'][1])
        download_button.click()

        # Aguarda carregar a fatura (ou download)
        #file_functions.wait_download(self.temp_dir) # Não precisa, pois o código já consegue fazer 100% com o WebDriverWait, já que sempre que abrir o popup vai baixar a fatura.

        # Aguarda a nova janela (popup) abrir
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Identifica a nova janela (popup)
        for handle in self.driver.window_handles:
            if handle != janela_principal:
                popup = handle
                break


        # Alterna para o popup
        self.driver.switch_to.window(popup)

        # Fecha somente o popup
        self.driver.close() 

        # Volta para a janela principal
        self.driver.switch_to.window(janela_principal)