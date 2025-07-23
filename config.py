from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API
API_KEY = os.getenv("API_KEY")



# Urls base do Site
URL_GET_LOGIN = "https://lojavirtual.compesa.com.br/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"
URL_POST_LOGIN = "https://lojavirtual.compesa.com.br/gsan/loginPortalAction.do?action=login"



# --------------- Configurando Header ---------------
def get_headers(cookie):
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,  # Ex: 'JSESSIONID=xyz; dtCookiemplfigul=abc; ...'
        "Host": "lojavirtual.compesa.com.br",
        "Origin": "https://lojavirtual.compesa.com.br",
        "Referer": "https://lojavirtual.compesa.com.br/gsan/loginPortalAction.do?action=login",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        ),
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

