from rich.progress import Progress
import pandas as pd
from pandas.tseries.offsets import MonthBegin
from funcoes_teste import *
import time as t
import json
import base64
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

class ObterToken:
     
    def __init__(self, row, conn, pasta):
 
        self.ID        = row.ID
        self.Matricula = row.Matricula
        self.Cliente   = row.Cliente
        self.Contrato  = row.Contrato
        self.Dist      = row.Distribuidora
        self.Login     = row.Login
        self.Senha     = row.Senha
        self.Nome      = row.Nome
        self.Cookies   = None
        self.conn      = conn
        self.Pasta     = pasta

        self.ObterToken()       

    def ObterToken(self):

        print(self.Login)
        print(self.Senha)

        self.Cookies     = "JSESSIONID=CRJH-C7iLXOS8fZPWKey52W8UoXQO5mZiXdGVK2O.lojavirtual"
        return self.Cookies

   
class COMPESA:
 
    def __init__(self, row, conn, Token, pasta):
 
        self.ID        = row.ID
        self.CNPJ      = row.CNPJ
        self.Matricula = row.Matricula
        self.Cliente   = row.Cliente
        self.Contrato  = row.Contrato
        self.Dist      = row.Distribuidora
        self.Login     = row.Login
        self.Senha     = row.Senha
        self.Nome      = row.Nome
        self.conn      = conn
        self.Cookies     = Token
        self.seassion  = requests.Session()
        self.Pasta     = fr"G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\Faturas"        
        
        self.StatusPagamento()

    def StatusPagamento(self):

        self.Inserir = Banco(self.conn)

        try:

            url = "https://lojavirtual.compesa.com.br:8443/gsan/loginPortalAction.do"

            data = {
                'action': 'setMatricula',
                'matricula': str(int(self.Matricula))
            }

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'pt-BR,pt;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': self.Cookies,
                'Host': 'lojavirtual.compesa.com.br:8443',
                'Origin': 'https://lojavirtual.compesa.com.br:8443',
                'Referer': 'https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.seassion.post(url, data=data, headers=headers, verify=False)

            url = "https://lojavirtual.compesa.com.br:8443/gsan/exibirServicosPortalCompesaAction.do?method=emitirSegundaViaConta&matriculaObrigatoria=true"

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'pt-BR,pt;q=0.9',
                'cache-control': 'max-age=0',
                'connection': 'keep-alive',
                'cookie': self.Cookies,
                'host': 'lojavirtual.compesa.com.br:8443',
                'referer': 'https://servicos.compesa.com.br/',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            }

            response = self.seassion.get(url, headers=headers)

            soup = BeautifulSoup(response.content, 'html.parser')

            tables_html = soup.find_all('table', {'summary': 'Tabela de contas'})

            dfs = []
            for j, table_html in enumerate(tables_html):
                df = pd.read_html(str(table_html))[0]
                df.columns = ['data_referencia', 'valor_total', "A"]
                df = df.drop("A", axis=1)

                df["data_vencimento"] = "01/01/1900"
                
                df["data_referencia"] = pd.to_datetime(df["data_referencia"], format='%m/%Y')
                df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], format='%d/%m/%Y')

                df["valor_total"] = df["valor_total"].map(lambda x: re.sub(r"R\$", "", x))
                if len(table_html) > 1 and j == 0:
                    df['status_fatura'] = "Pendente"
                    df["data_referencia"] = pd.to_datetime(df["data_referencia"], format='%m/%Y')
                    df["valor_total"] = df["valor_total"].map(lambda x: re.sub(r"R\$", "", x))
                    df["valor_total"] = df["valor_total"].map(lambda x: re.sub(r"\.", "", x))
                    df["valor_total"] = df["valor_total"].map(lambda x: re.sub(r"\,", ".", x))
                else:
                    df['status_fatura'] = "Pago"
                
                df["valor_total"] = df["valor_total"].astype(float)
                dfs.append(df)

            Faturas = pd.concat(dfs, ignore_index=True)
            Faturas["ID"] = self.ID
            Faturas["Matricula"] = self.Matricula
            Faturas["dist_fatura"] = self.Dist
            Faturas["data_execucao"] = datetime.now()

            NF = BeautifulSoup(response.content, 'html.parser')

            self.nf = re.findall(r"idConta='\+(\d*)", str(NF))


            self.Faturas = Faturas

            self.Inserir.Pagamentos(self.Faturas)
    
            inicio = pd.Timestamp('2024-01-01')
            hoje   = pd.Timestamp(datetime.now().strftime('%Y-%m-%d')) - MonthBegin(1)
            meses  = pd.date_range(start=inicio, end=hoje, freq='MS')
            meses  = meses[~meses.isin(self.Faturas['data_referencia'])]
            meses  = meses.strftime('%d/%m/%Y').tolist()
    
            for mes in meses:
    
                mes = datetime.strptime(mes, '%d/%m/%Y')
                self.Inserir.Status(self.ID, mes, "Não Emitida", self.Matricula, self.Dist)
    
            self.Downloads()

        except Exception as e:

            Banco(self.conn).Processar(self.ID, self.Matricula, self.Dist, "Erro ao obter CNPJ")
            t.sleep(2)
            return
        
    def Downloads(self):

        try:

            for j, i in enumerate(list(self.Faturas["data_referencia"].values)):
    
                Fatura = self.nf[j]
                i = datetime.strptime(str(i).split("T")[0], '%Y-%m-%d')
                
                Ref = i
                trava = self.Inserir.Trava(i, self.ID)
    
                if trava:
                    continue
            
                i = i.strftime("%m/%y")
    
                Nome  = f"{i.split('/')[1]}.{i.split('/')[0]}_DIST_{self.Dist}_{self.Nome}_{str(self.Matricula)}.pdf"

                url = f"https://lojavirtual.compesa.com.br:8443/gsan/gerarRelatorio2ViaContaAction.do?lojaVirtual=S&cobrarTaxaEmissaoConta=N&idConta={Fatura}"

                response = self.seassion.get(url)

                if response.status_code == 200:
                    with open(fr"{self.Pasta}\{Nome}", "wb") as file:
                        file.write(response.content)
                    self.Inserir.Status(self.ID, Ref, "Baixado", self.Matricula, self.Dist)
                else:
                    continue

        except Exception as e:

            Banco(self.conn).Processar(self.ID, self.Matricula, self.Dist, "Erro ao fazer download")
            t.sleep(2)
            return
        

def main(logins, conn, pasta):
    with Progress() as progress:
        linhas = list(logins.itertuples(index=False))
        row = linhas[0]
        Progresso = progress.add_task("Distribuidora: UC em Download: ", total=len(linhas))
        Token = ObterToken(row, conn, pasta).Cookies
        if Token:
            for row in linhas:
                progress.update(Progresso, advance=1, description=f"[cyan]Distribuidora: [gold3]{row.Distribuidora} [cyan]UC em Download: [gold3]{row.Matricula}")
                COMPESA(row, conn, Token, pasta)
