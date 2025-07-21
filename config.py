from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API
API_KEY = os.getenv("API_KEY")



# Urls base do Site
URL_GET_LOGIN = "https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"
URL_POST_LOGIN = "https://lojavirtual.compesa.com.br:8443/gsan/loginPortalAction.do?action=login"



# --------------- Configurando Header ---------------
cookie = "JSESSIONID=CRJH-C7iLXOS8fZPWKey52W8UoXQO5mZiXdGVK2O.lojavirtual"

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookie,
    'Host': 'lojavirtual.compesa.com.br:8443',
    'Origin': 'https://lojavirtual.compesa.com.br:8443',
    'Referer': 'https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}