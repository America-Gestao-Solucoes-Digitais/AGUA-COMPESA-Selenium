# Importando Modulos
import functions.file_functions as file_functions

# Importando bibliotecas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Faturas_manager:

    def __init__(self, driver, temp_dir, instalacao, dict_elements, cliente):
        
        # Váriaveis de ambiente
        self.driver = driver
        self.temp_dir = temp_dir

        # Configurações de elementos da página web
        self.dict_elements = dict_elements

        # Trazendo dados de Faturas
        self.referencia = ''
        self.distribuidora = 'COMPESA'
        self.instalacao = instalacao
        self.cliente = cliente

        if cliente == 'MAGAZINE LUIZA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\{cliente}\Faturas'
        elif cliente == 'DASA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\Faturas'


        self.download_fatura_atual()
    


    def download_fatura_atual(self):
        '''
        Passo a Passo:
        - Apertar o botão de download
        - Faz abri o popup
        - Faz o download da fatura
        - Fecha o popup
        '''

        time.sleep(3)

        # Salva a Janela atual como principal
        janela_principal = self.driver.current_window_handle

        # Clica no botão de download
        download_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                self.dict_elements['XPATH_Download_button'][0],
                self.dict_elements['XPATH_Download_button'][1]
            ))
        )
        download_button.click()

        time.sleep(3)

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

        # Quebrando a referencia
        # referencia_ano = self.referencia
        # referencia_mes = self.referencia
        
        # Alterando o nome da fatura e passando o arquivo para o caminho de leituras
        file_functions.mover_pdf(self.temp_dir, self.distribuidora, self.instalacao, self.cliente, self.path)

        # Volta para a janela principal
        self.driver.switch_to.window(janela_principal)