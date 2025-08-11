# Importando Modulos
import config

# Importando bibliotecas
from twocaptcha import TwoCaptcha
import sys
import os

# Colocando a raiz do repositório como o repositório pai
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

API_KEY = config.API_KEY

def solve_captcha(captcha_image_path):
    '''
    Resolvendo o CAPTCHA de imagem usando a API do TwoCaptcha.

    Observação:
    * A imagem do CAPTCHA é pega localmente pelo caminho: 'images/captcha.jpg'
    '''

    solver = TwoCaptcha(API_KEY)

    try:
        result = solver.normal(captcha_image_path)
        return result['code']
    
    except Exception as e:
        print(f"Erro ao resolver CAPTCHA: {e}")
        return None
    
    finally:
        if os.path.exists(captcha_image_path):
            os.remove(captcha_image_path)