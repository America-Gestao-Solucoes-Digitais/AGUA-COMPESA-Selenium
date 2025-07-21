import requests
from bs4 import BeautifulSoup
import sys
import os
from twocaptcha import TwoCaptcha
from urllib.parse import urljoin

API_KEY = "c559ef9877a25f6c80f12d9e846ea1f0"

'''
Tipo de requisição POST Nécessária:
login: aguaeenergia@magazineluiza.com.br (DataBase) (FEITO)
senha: Magazine@2025 (DataBase) (FEITO)
BDC_VCID_loginCaptcha: 2a06f74b4ff8487fa39709926bfe6b47 (Request) (FEITO)
BDC_BackWorkaround_loginCaptcha: 1 (Default) (FEITO)
BDC_Hs_loginCaptcha: 892eeaa9a5863c1b1fdc09b568ea5b990d0797b1 (Request) (FEITO)
BDC_SP_loginCaptcha: 568668182 (Request) (FEITO)
captchaCode: dv34 (Captcha - 2Captcha)
jwtGoogle: (Default)
'''

# --------------- Login e Senha ---------------
login = "aguaeenergia@magazineluiza.com.br"
senha = "Magazine@2025"

# --------------- Login -------------------
url = "https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"
matricula = "000001759"
cookies ="JSESSIONID=CRJH-C7iLXOS8fZPWKey52W8UoXQO5mZiXdGVK2O.lojavirtual"
seassion = requests.Session()

url_post = "https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"

# -------------- Configurações do POST ---------------
# data_post = {
#     'action': 'setMatricula',
#     'matricula': str(int(matricula))
# }

headers_post = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookies,
    'Host': 'lojavirtual.compesa.com.br:8443',
    'Origin': 'https://lojavirtual.compesa.com.br:8443',
    'Referer': 'https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = seassion.get(url)

soup = BeautifulSoup(response.text, "html.parser")

vcid = soup.find("input", {"name": "BDC_VCID_loginCaptcha"})["value"]
hs = soup.find("input", {"name": "BDC_Hs_loginCaptcha"})["value"]
sp = soup.find("input", {"name": "BDC_SP_loginCaptcha"})["value"]
img_tag = soup.find("img", {"class": "BDC_CaptchaImage"})

print(f"vcid: {vcid}, hs: {hs}, sp: {sp}")

captcha_src = img_tag['src']
captcha_url = urljoin(response.url, captcha_src)

print("""
      
------------------------------------------------------------
      
""")

print("URL da imagem do CAPTCHA:", captcha_url)

response_img = requests.get(captcha_url)

with open("images/captcha.jpg", "wb") as f:
    f.write(response_img.content)

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

solver = TwoCaptcha(API_KEY)

try:
    result_captcha = solver.normal('images/captcha.jpg')

except Exception as e:
    sys.exit(e)

else:
    print('solved: ' + str(result_captcha))

print("""
      
------------------------------------------------------------

""")

data = {
    'login': login,
    'senha': senha,
    'BDC_VCID_loginCaptcha': vcid,
    'BDC_BackWorkaround_loginCaptcha': '1',
    'BDC_Hs_loginCaptcha': hs,
    'BDC_SP_loginCaptcha': sp,
    'captchaCode': result_captcha,
    'jwtGoogle': ''
}

url_post = "https://lojavirtual.compesa.com.br:8443/gsan/loginPortalAction.do?action=login"

result_login = requests.post(url_post, data=data)

print(f"Status Code: {result_login.status_code}")
print("")
print(f"Response Text: {result_login.text}")

print("t")