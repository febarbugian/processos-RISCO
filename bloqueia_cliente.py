from Solution import Solution
from line import APILine
from playwright.sync_api import sync_playwright, expect


cd_clientes = [167498, 14348]

with sync_playwright() as playwright:
    api_line = APILine()
    api_line.auth()
    solution = Solution()
    solution.loga(playwright)
    for cd_cliente in cd_clientes:
        solution.abre_cliente(cd_cliente)
        solution.comentario("comentario")
        solution.salva_limite()
        
        cliente = api_line.consultaAccount(cd_cliente)
        api_line.isBlockedAccount(True)
    solution.fecha()