# Importando Modulos
import shutil

# Importando bibliotecas
import os

def verifica_fatura_bd(class_bd, tabela , data_referencia, instalacao):
    '''
    Verifica se a fatura já foi baixada no banco de dados, 
    Return:
    True: Fatura já foi baixada
    False: Fatura não foi baixada
    '''

    # Faz um select/dataframe para verificar se a fatura já foi baixada
    df_veficacao = class_bd.read_table(tabela, columns=['REFERENCIA', 'COD_INSTALACAO'], where= f"COD_INSTALACAO = '{instalacao}'")

    # Faz um Where para verificação
    df_veficacao = df_veficacao[
        (df_veficacao['REFERENCIA'] == data_referencia) &
        (df_veficacao['COD_INSTALACAO'] == instalacao)
    ]

    # Verifica se o df está vazio, conseguentemente se foi encontrado algum registro ou não
    # Dessa forma trazendo a informação se atualizou não.
    if not df_veficacao.empty:
        return True

    if df_veficacao.empty:
        return False



def mover_pdf(temp_dir, distribuidora, instalacao, cliente, path, numero_fatura): # mover_pdf(temp_dir, ano_referencia, mes_referencia, distribuidora, instalacao, cliente, path):
    '''Pega do diretorio temporário, altera o nome da fatura e move para o diretório final '''
    

    try:
        # Buscar PDF no diretório temporário
        pdfs = [f for f in os.listdir(temp_dir) if f.endswith('.pdf')]
        if not pdfs:
            raise FileNotFoundError("Nenhum PDF encontrado no diretório temporário.")
        
        # Determina o diretorio incial e o novo nome do pdf
        original_path = os.path.join(temp_dir, pdfs[0])
        #novo_nome = f"{ano_referencia}.{mes_referencia}_DIST_{distribuidora}_{cliente}_{instalacao}.pdf"
        novo_nome = f"25.00_DIST_{distribuidora}_{cliente}_{instalacao}_{numero_fatura}.pdf"

        # Criar diretório, se não existir
        os.makedirs(path, exist_ok=True)
        destino_final = os.path.join(path, novo_nome)

        # Verificar se o PDF já existe no destino
        if os.path.exists(destino_final):
            print(f"Arquivo {novo_nome} já existe. Removendo o PDF temporário.")
            os.remove(original_path)

        else:
        # Se não exister no destino move o PDF com o novo nome
            shutil.move(original_path, destino_final)
            print(f"Fatura movido com sucesso para: {destino_final}")

    except Exception as e:
        print("Erro ao mover o PDF:", e)