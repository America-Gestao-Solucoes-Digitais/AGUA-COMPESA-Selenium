# Importando Modulos
import functions.file_functions as file_functions

# Importando bibliotecas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def extrair_faturas_por_titulo(titulo_texto, status, soup):
    """Procura um h3 com texto igual ao título e extrai a tabela logo abaixo"""
    dados = []
    titulo = soup.find("h3", string=lambda t: t and titulo_texto in t)
    if titulo:
        tabela = titulo.find_next("table")
        for linha in tabela.select("tbody tr"):
            colunas = linha.find_all("td")
            if len(colunas) >= 2:
                mes_ano = colunas[0].get_text(strip=True)
                valor = colunas[1].get_text(strip=True).replace("R$", "").strip()
                dados.append({"Mês/Ano": mes_ano, "Valor": valor, "Status": status})
    return dados


class Faturas_manager:

    def __init__(self, driver, temp_dir, dict_elements,  html_page, instalacao, cliente):
        
        # Váriaveis de ambiente
        self.driver = driver
        self.temp_dir = temp_dir

        # Configurações de elementos da página web
        self.dict_elements = dict_elements

        # Pegando o HTML da página da UC
        self.html = html_page

        # Trazendo dados de Faturas
        self.referencia = ''
        self.distribuidora = 'COMPESA'
        self.instalacao = instalacao
        self.cliente = cliente

        # Configurando o caminho para cada cliente
        if cliente == 'MAGAZINE LUIZA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\{cliente}\Faturas'
        elif cliente == 'DASA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\Faturas'

    

    def status_fatura_atual(self):
        '''Pegando o status da fatura atual a partir do html_page'''

        soup = BeautifulSoup(self.html, "html.parser")

        # Extrair baseado no título
        faturas = []
        faturas.extend(extrair_faturas_por_titulo("Faturas em Aberto", "Aberto", soup))
        faturas.extend(extrair_faturas_por_titulo("Faturas Pagas", "Pago", soup))

        # Verifica se não tem nenhuma fatura em aberto
        fatura_aberta = faturas[faturas["Status"] == "Aberto"].empty

        # Criar DataFrame
        df_faturas = pd.DataFrame(faturas)
        
        return df_faturas, fatura_aberta


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

        status = False

        try:

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

            status = True
            return status

        except:
            print('[ERROR] Fatura atual não encontrada.')
            return status
