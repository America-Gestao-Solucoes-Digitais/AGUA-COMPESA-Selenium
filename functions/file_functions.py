import os
import time

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



# def wait_download(temp_dir, timeout=120):
#     '''Espera até que um novo PDF completo seja baixado ou até o tempo limite.'''
    
#     tempo_inicial = time.time()
#     pdfs_antes = set(f for f in os.listdir(temp_dir) if f.endswith('.pdf'))

#     while True:
#         time.sleep(1)  # Espera 1 segundos antes de verificar novamente

#         arquivos = os.listdir(temp_dir)

#         # Checa se ainda tem algum .crdownload
#         if any(f.endswith('.crdownload') for f in arquivos):
#             continue

#         # Verifica se apareceu um novo PDF
#         pdfs_atuais = set(f for f in arquivos if f.endswith('.pdf'))
#         novos_pdfs = pdfs_atuais - pdfs_antes
#         if novos_pdfs:
#             print("Baixado Corretamente:", novos_pdfs)
#             break

#         # Timeout
#         if time.time() - tempo_inicial > timeout:
#             print(f"Tempo limite de download excedido, fatura não baixada.")
#             break
    


# def mover_pdf(temp_dir, ano_referencia, mes_referencia, distribuidora, instalacao, classe_tensao, cliente):
#     '''Pega do diretorio temporário, altera o nome e move para o diretório final '''
    
#     try:
#         # Buscar PDF no diretório temporário
#         pdfs = [f for f in os.listdir(temp_dir) if f.endswith('.pdf')]
#         if not pdfs:
#             raise FileNotFoundError("Nenhum PDF encontrado no diretório temporário.")
        
#         # Replace classe_tensao
#         if classe_tensao == "Baixa Tensão":
#             classe_tensao = "BT"
        
#         if classe_tensao == "Média Tensão":
#             classe_tensao = "MT"
        
#         # Determina o diretorio incial e o novo nome do pdf
#         original_path = os.path.join(temp_dir, pdfs[0])
#         novo_nome = f"{ano_referencia}.{mes_referencia}_DIST_{distribuidora}_{instalacao}_{classe_tensao}.pdf"

#         # Determinar diretório de destino com base na classe
#         if classe_tensao == "MT":
#             base_dir = os.path.join(configurations.DIR_MT, cliente, "Faturas")
#         else:
#             base_dir = os.path.join(configurations.DIR_BT, cliente, "Faturas")

#         # Criar diretório, se não existir
#         os.makedirs(base_dir, exist_ok=True)
#         destino_final = os.path.join(base_dir, novo_nome)

#         # Verificar se o PDF já existe no destino
#         if os.path.exists(destino_final):
#             print(f"Arquivo {novo_nome} já existe. Removendo o PDF temporário.")
#             os.remove(original_path)

#         else:
#         # Se não exister no destino move o PDF com o novo nome
#             shutil.move(original_path, destino_final)
#             print(f"PDF movido com sucesso para: {destino_final}")

#     except Exception as e:
#         print("Erro ao mover o PDF:", e)