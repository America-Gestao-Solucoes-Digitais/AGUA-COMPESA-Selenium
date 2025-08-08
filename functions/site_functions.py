# Importando Modulos
import config

# Importando bibliotecas
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def get_elements_html_login(html_login):
    '''
    Obtém os elementos/atributos do HTML necessários para o login.
    
    * vcid = BDC_VCID_loginCaptcha\n
    * hs = BDC_Hs_loginCaptcha\n
    * sp = BDC_SP_loginCaptcha\n

    Observação: img_tag é a tag da imagem do CAPTCHA que será resolvido pelo 2Captcha.
    '''

    soup = BeautifulSoup(html_login, "html.parser")

    vcid = soup.find("input", {"name": "BDC_VCID_loginCaptcha"})["value"]
    hs = soup.find("input", {"name": "BDC_Hs_loginCaptcha"})["value"]
    sp = soup.find("input", {"name": "BDC_SP_loginCaptcha"})["value"]

    return vcid, hs, sp



def capture_captcha_image(requests_session, img_tag, url_get_login):
    '''
    Captura a imagem do CAPTCHA, salva ela no diretório 'images/' 
    e retorna a URL da imagem.
    '''

    # Acessa o atributo 'src' da tag img para obter a URL do CAPTCHA
    captcha_src = img_tag['src']
    captcha_url = urljoin(url_get_login, captcha_src)

    # Faz a requisição para obter a imagem do CAPTCHA
    response_img = requests_session.get(captcha_url)

    # Salva a imagem do CAPTCHA no arquivo images/
    with open("images/captcha.jpg", "wb") as f:
        f.write(response_img.content)

    return "images/captcha.jpg"