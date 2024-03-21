import requests
from openpyxl import Workbook

def obter_ultima_operacao(cliente):
    url = f"exemplo_url/{cliente}"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados

clientes = [123, 345]  

# Criar uma nova pasta de trabalho do Excel
wb = Workbook()
# Selecionar a primeira planilha (por padrão, é Sheet)
ws = wb.active

# Adicionar cabeçalhos
ws.append(["Cliente", "Data última operação na BVSP", "Data última operação na BMF"])

for cliente in clientes:
    informacoes = obter_ultima_operacao(cliente)
    # Verificar se as informações não são NULL antes de processar
    if informacoes is not None:
        # Remover o "T" das datas
        data_bvsp = informacoes.get('DT_ULT_OPER_BVSP', '').split("T")[0]
        data_bmf = informacoes.get('DT_ULT_OPER_BMF', '').split("T")[0]
        # Adicionar informações do cliente à planilha
        ws.append([cliente, data_bvsp, data_bmf])

# Salvar a pasta de trabalho
wb.save("informacoes_ultima_operacao.xlsx")

import os
print("O arquivo foi salvo em:", os.getcwd())
