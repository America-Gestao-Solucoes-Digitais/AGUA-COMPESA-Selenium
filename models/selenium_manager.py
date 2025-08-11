# Import Modulos
import config
from functions.solver_two_captcha import solve_captcha

# Import Libs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

# Importando url do site para ficar mais organizado
site_url = config.URL_LOGIN

class Selenium_manager():
    '''
    Classe reponsável por gerenciar o selenium, 
    Inicializa criando o drive do Selenium e acessando o site da Compensa.
    Além disso, faz todo o controle do navegador e dos elementos nele.
    '''
    def __init__(self, temp_dir):
        '''Inicializa o Selenium e acessa o site da Compesa.'''
        self.driver = self.iniciar_selenium(temp_dir)
        self.status = self.get_site()



    def iniciar_selenium(self, temp_dir):
        '''Inicializa o Selenium com o Chrome WebDriver padrão'''

        options = Options()

        # User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
        options.add_argument(f"user-agent={user_agent}")

        # Configurações de idioma
        options.add_argument("--lang=pt-BR,pt,en,en-GB,en-US")

        # Optins Uteis
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



        # Opções para download de arquivos, alocando em um repositorio temporário
        prefs = {
        "download.default_directory": temp_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)



        # Inicializa o driver padrão do Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        return driver



    def get_site(self):
        '''Abra o site da Compensa por meio do Selenium'''

        try:
            # Timeout, necessario pois tem o erro de carregamento infinito do site, principalmente ELEKTRO (site instável)
            self.driver.set_page_load_timeout(40)

            # Abre o site da Compensa
            self.driver.get(site_url)

            # tempo para a página carregar por completo
            time.sleep(0.5)
            status = True

            return status

        except Exception as e:
            print(f"[ERRO] get_site: {e}")
            status = False

            return status



    def captura_recaptcha(driver, dict_elements):
        '''
        Captura a imagem do reCaptcha, salva localmente, retorna o captcha_code e somente depois exclui a imagem local.
        '''

        # Encontra o elemento da imagem do CAPTCHA
        captcha_img = driver.find_element(dict_elements['ID_image_captcha_login'][0], dict_elements['ID_image_captcha_login'][1])

        # Tira screenshot do elemento e salva como JPG
        captcha_img.screenshot("images/captcha.jpg")



    def captura_html(driver):
        '''Captura o HTML da página atual.'''

        html = driver.page_source

        return html



    def driver_close(self):
        '''Fecha o driver do Selenium'''
        
        self.driver.quit()