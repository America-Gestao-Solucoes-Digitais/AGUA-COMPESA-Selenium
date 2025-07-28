# Import Libs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time



class Selenium_driver():
    '''
    Classe reponsável por gerenciar o selenium. 
    Inicializa criando o drive do Selenium e acessando o site da Neoenergia.
    
    Métodos:
    - iniciar_selenium (chamado quando é instanciada) 
    - get_site (chamado quando é instanciada)
    - captura_html (chamado para function: captura_recaptcha)
    - driver_close (chamado para fechar o driver, logo após da captura recaptcha)

    '''

    def __init__(self):
        # inicia e entra no site da Neoenergia
        self.driver = self.iniciar_selenium()
        self.get_site()


    # def iniciar_selenium(self): # temp_dir como atributo
    #     '''Inicializa o Selenium com o Chrome WebDriver'''

    #     # Configurações do Chrome
    #     options = Options() # Usando Options() diretamente
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_argument("--disable-popup-blocking")
    #     options.add_argument('--safebrowsing-disable-download-protection')
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--disable-software-rasterizer")
    #     options.add_argument("--disable-webgl")

    #     # Suprime os logs do ChromeDriver e do Chromium
    #     options.add_argument("--log-level=3")  # Supressão de logs (apenas erros críticos)
    #     options.add_argument("--silent")       # Evitar logs desnecessários

    #     # Inicia o driver do Chrome
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #     return driver

    def iniciar_selenium(self):
        '''Inicializa o Selenium com o Chrome WebDriver mascarado'''

        options = uc.ChromeOptions()

        # 1. User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
        options.add_argument(f"user-agent={user_agent}")

        # 2. Configurações de idioma
        options.add_argument("--lang=pt-BR,pt,en,en-GB,en-US")

        # 3. Desativa extensões que entregam o Selenium
        options.add_argument("--disable-blink-features=AutomationControlled")

        # 4. Outras opções úteis
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--safebrowsing-disable-download-protection')
        options.add_argument("--disable-gpu") # <-- Pode não mascarar o Selenium, mas pode causar problemas em alguns sites
        options.add_argument("--disable-software-rasterizer") # <-- Pode não mascarar o Selenium, mas pode causar problemas em alguns sites
        options.add_argument("--disable-webgl") # <-- Pode não mascarar o Selenium, mas pode causar problemas em alguns sites
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--start-maximized")

        # 5. Inicializa o driver com stealth
        driver = uc.Chrome(options=options)

        return driver


    def get_site(self):
        '''Abra o site da Neoenergia por meio do Selenium'''

        # Abre o site da Compesa
        self.driver.get('https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true')

        # tempo para a página carregar por completo
        time.sleep(0.5)



    def captura_html(self):
        '''Captura o HTML da página atual.'''

        html = self.driver.page_source

        return html



    def driver_close(self):
        '''Fecha o driver do Selenium'''
        
        self.driver.quit()