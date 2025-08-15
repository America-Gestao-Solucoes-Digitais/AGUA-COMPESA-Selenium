# Import Modulos
import config

# Import Libs
from sqlalchemy import create_engine
import urllib.parse

class Sqlalchemy_mysql_connect():
    '''Classe responsável por gerenciar a conexão com o banco de dados (MySQL) usando o sqlalchemy'''

    def __init__(self):
        self.username = config.username
        self.password = config.password
        self.server = config.server
        self.port = config.port
        self.database = config.database
        self.engine = self.connect()

    def connect(self):
        '''Cria e retorna uma conexão com o MySQL'''

        # Codifica o password em caracteres especiais para ser usados em URL de querys
        encoded_password = urllib.parse.quote_plus(self.password)

        try:
            connect_string = (
            f"mysql+mysqlconnector://{self.username}:{encoded_password}@{self.server}:{self.port}/{self.database}"
            )
            
            engine = create_engine(connect_string, echo=False)

            return engine

        except Exception as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    def close_connection(self):
        '''Fecha a conexão com o banco de dados'''
        try:
            if self.engine:
                self.engine.dispose()  # Libera o pool de conexões
        except Exception as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")