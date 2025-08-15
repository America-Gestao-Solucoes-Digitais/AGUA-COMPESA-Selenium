# Import Modulos
from models.sqlalchemy_mysql_connect import Sqlalchemy_mysql_connect as driver

# Import Libs
from sqlalchemy import create_engine, text
import pandas as pd

class Manage_database(driver):
    '''
    Classe responsável por gerenciar as operações no banco de dados, 
    se baseia na sqlalchemy_mysql_connect (classe pai, driver do sgbd)
    para fazer a conexão com o banco. 
    '''

    def __init__(self):
        super().__init__() # <- aqui você chama o __init__ da classe pai (driver ou sqlalchemy_mysql_connect) 
    
        
    def read_table(self, table_name, columns=None, where=None):
        '''
        Lê uma tabela do banco de dados e retorna um DataFrame.
        Tem como padrão o database "america_gestao"

        Argumentos:
            table_name: Nome da tabela a ser lida
            columns: Colunas a serem lidas (pode ser uma lista ou None para todas as colunas)
            where: Condição WHERE para filtrar os dados (pode ser None para não filtrar)
            
        '''
        
        # Lê uma tabela do banco de dados e retorna um DataFrame
        try:

            # Verifica engine
            engine = self.engine
            if engine is not None:

                with engine.connect() as connection:

                    # Executa a consulta SQL para ler a tabela
                    query = ( 
                        f"SELECT {', '.join(columns) if columns else '*'} "
                        f"FROM {table_name}"
                    )
                    if where:
                        query += f" WHERE {where}"

                    df = pd.read_sql(query, connection)

                return df
            
            # Caso não consiga conectar, retorna None
            else:
                print("Erro ao conectar ao banco de dados.")
                return None
            
        # Caso ocorra algum erro, retorna None
        except Exception as e:
            print(f"Erro ao ler a tabela {table_name}: {e}")
            return None


    def insert_status(self, data_status, instalacao, referencia, distribuidora, vencimento, status):
        '''
        Insere um registro em uma tabela do banco de dados.
        Tem como padrão o database "america_gestao"

        Argumentos:
            table_name: Nome da tabela a ser lida
            instalacao: Instalação a ser lida
            referencia: Referência a ser lida
            vencimento: Vencimento a ser lido
            status: Status a ser lido
            data_status: Horário a ser lido
        '''
        
        # Insere um DataFrame em uma tabela do banco de dados
        try:
            # Verifica engine
            engine = self.engine
            if engine is not None:

                check_query = f"""
                SELECT COUNT(*) 
                FROM tb_status_pagamento_gestao_faturas 
                WHERE INSTALACAO = {instalacao} 
                AND REFERENCIA = '{referencia}'
                AND DT_VENCIMENTO = '{vencimento}'
                AND STATUS_PAGAMENTO = '{status}'
                """

                # faz a query de inserção dos dados
                with self.engine.connect() as connection:
                    result = connection.execute(text(check_query)).scalar()
                    if result == 0:
                        
                        query = f'''
                        INSERT INTO tb_status_pagamento_gestao_faturas 
                        (DATA_STATUS, INSTALACAO, REFERENCIA, DISTRIBUIDORA, DT_VENCIMENTO, STATUS_PAGAMENTO, COMENTARIO) 
                        VALUES 
                        ('{data_status}', '{instalacao}', '{referencia}', '{distribuidora}', '{vencimento}', '{status}', 'Água')
                        '''
                        
                        connection.execute(text(query))

                        connection.commit()
            
            # Caso não consiga conectar, retorna None
            else:
                print("Erro ao conectar ao banco de dados.")
                return None
            
        # Caso ocorra algum erro, retorna None
        except Exception as e:
            print(f"Erro ao inserir o DataFrame na tabela: {e}")
            return None