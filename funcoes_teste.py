import os
import re
import pandas as pd
from pandas.tseries.offsets import MonthBegin
from datetime import datetime
import undetected_chromedriver as uc
import requests
import time as t
import subprocess
import speech_recognition as sr
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from twocaptcha import TwoCaptcha
import random

class DadosGerais:
    
    def __init__(self, conn = None):

        self.conn = conn

    def Pasta(self,Cliente):
        if Cliente == "DASA":
            caminho                   = r"G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\Faturas"
        elif Cliente == "MAGAZINE LUIZA":
            caminho                   = r"G:\QUALIDADE\Códigos\Nova Leitura de Faturas de Agua\MAGAZINE LUIZA\Faturas"
        else:
            caminho = ''


        return caminho

    
    def Distribuidoras(self):

        dist    = []
  
        for arquivo in os.listdir(os.getcwd()):

            termos = any(x in arquivo for x in ["funcoes", "main", "cpython"])
            if arquivo.endswith(".py") and not termos:
                dist.append(re.sub(r"\.py$", "", arquivo))
        
        return dist  
    
    def Logins(self, debug, Cliente, UC):
        
        Consulta = '''SELECT * FROM Logins''' 
        Logins   = pd.read_sql(Consulta, self.conn)

        if UC != False:
            Logins   = Logins.loc[Logins['Matricula'].str.contains(UC)]

        if Cliente:
            Logins = Logins.loc[Logins['Cliente'].str.contains(Cliente)]

        if debug:

            Status = '''
                SELECT DISTINCT ID FROM tbl_status
                WHERE status_fatura LIKE '%Erro%'
            '''

            Status = pd.read_sql(Status, self.conn)
            Status = set(Status['ID'])
            IDS = Status
            Logins = Logins[Logins['ID'].isin(IDS)]

        else:

            Consulta = '''SELECT * FROM tbl_status'''
            Status   = pd.read_sql(Consulta, self.conn)

            Status['data_referencia'] = pd.to_datetime(Status['data_referencia'], errors='coerce')

            data_atual      = datetime.now()
            Status          = Status[Status['data_referencia'] <= data_atual]

            Status['Chave'] = Status['status_fatura'] + "01" + Status['data_referencia'].dt.strftime('/%m/%Y')

            Baixados        = [f'Baixado01/{mes:02d}/{datetime.now().year}' for mes in range(datetime.now().month, 0, -1)]
            
            IDs             = Status.loc[~(Status['Chave'].isin(Baixados))]
            IDs             = Status.loc[~(Status['Chave'].str.contains('Baixado')), 'ID']
            IDs             = IDs.dropna().astype(int).unique()

            Logins['ID']    = Logins['ID'].astype(int)
            IDs_logins      = Logins['ID'].unique()
            IDs_comuns      = set(IDs).intersection(IDs_logins)
            IDs_exclusivos = set(IDs_logins).difference(Status.loc[Status['data_referencia'].dt.to_period('M') == pd.Period(datetime.now(), freq='M'), 'ID'].unique())

            IDs             = IDs_comuns.union(IDs_exclusivos)
            Logins          = Logins[Logins['ID'].isin(IDs)]

        if not Logins.empty:
            Logins = [grupo for _, grupo in Logins.groupby(['Distribuidora', 'Login'])]
        else:
            Logins = []

        return Logins
    

class Banco:
    
    def __init__(self, conn):

        self.conn = conn

    def Processar(self, ID, Matricula, dist, status):
    
        inicio = pd.Timestamp('2024-01-01')
        hoje   = pd.Timestamp(datetime.now().strftime('%Y-%m-%d')) - MonthBegin(1)
        meses  = pd.date_range(start=inicio, end=hoje, freq='MS')
        meses  = meses.strftime('%d/%m/%Y').to_list()

        for mes in meses:
            self.Status(ID, datetime.strptime(mes, '%d/%m/%Y'), status, Matricula, dist)


    def Pagamentos(self, Tabela):

        cursor = self.conn.cursor()
        
        for _, row in Tabela.iterrows():

            cursor.execute("SELECT COUNT(*) FROM tbl_pagamentos WHERE ID = ? AND data_referencia = ?", (row['ID'], row['data_referencia']))
            count = cursor.fetchone()[0]

            if count > 0:

                cursor.execute("UPDATE tbl_pagamentos SET valor_total = ?, Matricula = ?, dist_fatura = ?, data_execucao = ?, status_fatura = ?, data_vencimento = ? WHERE ID = ? AND data_referencia = ?", 
                            (row['valor_total'], row['Matricula'], row['dist_fatura'], row['data_execucao'], row['status_fatura'], row['data_vencimento'], row['ID'], row['data_referencia']))
            else:
                cursor.execute("INSERT INTO tbl_pagamentos (valor_total, Matricula, dist_fatura, ID, data_execucao, status_fatura, data_vencimento, data_referencia) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                            (row['valor_total'], row['Matricula'], row['dist_fatura'], row['ID'], row['data_execucao'], row['status_fatura'], row['data_vencimento'], row['data_referencia']))

        self.conn.commit()

        return

    def Status(self, ID, Ref, info, Matricula, dist):
        
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tbl_status WHERE ID = ? AND data_referencia = ?", (ID, Ref))
        count = cursor.fetchone()[0]

        if count > 0:
            
            cursor.execute("UPDATE tbl_status SET data_execucao = ?, status_fatura = ?, Matricula = ? WHERE ID = ? AND data_referencia = ? AND status_fatura <> 'Baixado'", 
                        (datetime.now(), info, Matricula, ID, Ref))
        else:

            cursor.execute("INSERT INTO tbl_status (ID, Matricula, dist_fatura, data_execucao, status_fatura, data_referencia) VALUES (?, ?, ?, ?, ?, ?)", 
                        (ID, Matricula, dist, datetime.now(), info, Ref))

        self.conn.commit()

    def Trava(self, i, ID):
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbl_status WHERE ID = ? AND data_referencia = ? AND status_fatura = 'Baixado'", (int(ID), i))
        return cursor.fetchone()[0] > 0
    
class Recaptcha:
    
    def __init__(self):

        self.Token  = None

    def TwoCaptcha(self, chave, url):

        api_key = "c559ef9877a25f6c80f12d9e846ea1f0"
        solver  = TwoCaptcha(api_key)
        result  = solver.recaptcha(sitekey=chave, url=url)
        captcha_response = result['code']
        self.Token = captcha_response
        return captcha_response
