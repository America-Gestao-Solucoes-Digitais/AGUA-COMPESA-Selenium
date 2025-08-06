# Import Libs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class Selenium_driver():
    '''
    Classe reponsável por gerenciar o selenium. 
    Inicializa criando o drive do Selenium e acessando o site da Neoenergia.
    '''
    def __init__(self, url):
        '''Inicializa o Selenium e acessa o site da Compesa.'''
        self.url = url
        self.driver = self.iniciar_selenium()
        self.get_site()

    def iniciar_selenium(self):
        '''Inicializa o Selenium com o Chrome WebDriver padrão'''

        options = Options()

        # 1. User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
        options.add_argument(f"user-agent={user_agent}")

        # 2. Configurações de idioma
        options.add_argument("--lang=pt-BR,pt,en,en-GB,en-US")

        # 3. Outras opções úteis
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--safebrowsing-disable-download-protection')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-webgl")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--start-maximized")

        # Inicializa o driver padrão do Selenium
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        return driver



    def get_site(self):
        '''Abra o site da Compensa por meio do Selenium'''

        # Abre o site da Compesa
        self.driver.get('https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true')

        # tempo para a página carregar por completo
        time.sleep(0.5)


    def captura_recaptcha(self):
        '''Captura a imagem do reCAPTCHA.'''

        # Encontra o elemento da imagem do reCAPTCHA
        recaptcha_img = self.driver.find_element(By.ID, "loginCaptcha_CaptchaImage")

        # Tira screenshot do elemento e salva como JPG
        recaptcha_img.screenshot("images/recaptcha.jpg")

        return "images/recaptcha.jpg"


    def captura_html(self):
        '''Captura o HTML da página atual.'''

        html = self.driver.page_source

        return html



    def driver_close(self):
        '''Fecha o driver do Selenium'''
        
        self.driver.quit()