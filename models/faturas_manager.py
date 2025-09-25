# Importando Modulos
from functions.pandas_fuctions import formatar_datas
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
                dados.append({"data_referencia": mes_ano, "valor": valor, "status_fatura": status})
    return dados


class Faturas_manager:

    def __init__(self, driver, drive_manage_sql, temp_dir, dict_elements,  html_page, instalacao, cliente):
        
        # Váriaveis de ambiente
        self.driver = driver
        self.temp_dir = temp_dir
        self.drive_manage_sql = drive_manage_sql

        # Configurações de elementos da página web
        self.dict_elements = dict_elements

        # Pegando o HTML da página da UC
        self.html = html_page

        # Trazendo dados de Faturas
        self.distribuidora = 'COMPESA'
        self.instalacao = instalacao
        self.cliente = cliente

        # Configurando o caminho para cada cliente
        if cliente == 'MAGAZINE LUIZA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\{cliente}\Faturas'
        elif cliente == 'DASA':
            self.path = rf'G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\Faturas'

    

    def status_fatura_atual(self):
        '''
        Pegando o status da fatura atual a partir do html_page (Faturas em Aberto e Faturas Pagas),
        Cria dois DataFrames, um com todas as faturas e outro somente com as faturas em aberto.
        '''
        status = True

        try:
            soup = BeautifulSoup(self.html, "html.parser")

            # Extrair baseado no título
            faturas = []
            faturas.extend(extrair_faturas_por_titulo("Faturas em Aberto", "Em aberto", soup))
            faturas.extend(extrair_faturas_por_titulo("Faturas Pagas", "Pago", soup))

            # Criar DataFrame
            df_faturas = pd.DataFrame(faturas)

            # Formatar as datas
            df_faturas = formatar_datas(df_faturas)

            # Verifica se não tem nenhuma fatura em aberto
            faturas_abertas = df_faturas[df_faturas["status_fatura"] == "Em aberto"]

        except Exception as e:
            print(f'[ERROR] Erro ao extrair faturas: {e}')
            df_faturas = pd.DataFrame()
            faturas_abertas = pd.DataFrame()
            status = False

        return status, df_faturas, faturas_abertas



    def download_faturas(self):
        """
        Função responsável por fazer o download de TODAS as faturas disponíveis na tela.
        """

        time.sleep(3)
        janela_principal = self.driver.current_window_handle
        status = False

        try:
            # Localiza TODOS os botões de download (lista)
            botoes_download = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((
                    self.dict_elements['XPATH_Download_button'][0],
                    self.dict_elements['XPATH_Download_button'][1]
                ))
            )

            print(f"[INFO] Encontrados {len(botoes_download)} botões de download.")

            for i, botao in enumerate(botoes_download, start=1):
                try:
                    # Precisa garantir que o elemento ainda esteja clicável a cada iteração
                    botao = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((
                            self.dict_elements['XPATH_Download_button'][0],
                            self.dict_elements['XPATH_Download_button'][1]
                        ))
                    )
                    botao.click()
                    time.sleep(3)

                    # Aguarda a nova janela (popup) abrir
                    WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

                    # Identifica o popup
                    for handle in self.driver.window_handles:
                        if handle != janela_principal:
                            popup = handle
                            break

                    # Alterna para o popup
                    self.driver.switch_to.window(popup)

                    # Fecha somente o popup
                    self.driver.close()

                    # Movimenta o arquivo baixado
                    file_functions.mover_pdf(
                        self.temp_dir, self.distribuidora,
                        self.instalacao, self.cliente, self.path, i
                    )

                    # Volta para a janela principal
                    self.driver.switch_to.window(janela_principal)

                    print(f"[INFO] Fatura {i} baixada com sucesso.")
                    status = True

                except Exception as e:
                    print(f"[ERROR] Erro ao baixar fatura {i}: {e}")

            return status

        except Exception as e:
            print(f"[ERROR] Nenhuma fatura encontrada: {e}")
            return status
