import os
import zipfile
from playwright.sync_api import sync_playwright, expect
from time import sleep

def extraiMargem(outer_zip_path,base_directory):
    extract_dir = "pasta_de_extracao"

    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(outer_zip_path, 'r') as outer_zip:
        inner_zip_names = []
        
        for file_info in outer_zip.infolist():
            if file_info.filename.endswith('.zip'):
                inner_zip_names.append(file_info.filename)
                
                with outer_zip.open(file_info.filename) as inner_zip_file:
                    temp_extract_dir = "temp_dir"
                    os.makedirs(temp_extract_dir, exist_ok=True)
                    
                    with zipfile.ZipFile(inner_zip_file, 'r') as inner_zip:
                        inner_zip.extractall(temp_extract_dir)
                        
                        for inner_file_info in inner_zip.infolist():
                            if inner_file_info.filename.endswith('.csv'):
                                csv_filename = inner_file_info.filename
                                
                                csv_path = os.path.join(temp_extract_dir, csv_filename)
                                final_csv_path = os.path.join(base_directory, csv_filename)
                                os.rename(csv_path, final_csv_path)
                                
                                print(f"Arquivo CSV '{csv_filename}' extraído com sucesso.")
                                
                    os.rmdir(temp_extract_dir)
                    os.rmdir(extract_dir)

def downloadMargem():
    url_site = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/pesquisa-por-pregao/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()

        page.goto(url_site)
        page.locator("body").click()
        page.locator("//*[@id=\"8AA8D0975C8A570C015C8E128AEF795B\"]").check()
        
        with page.expect_download() as download_info:
            page.locator("//*[@id=\"botao-download\"]").click()
        name = os.path.join(os.getcwd(), nome_arquivo)
        download_info.value.save_as(name)


        sleep(10)
        page.close()

        context.close()
        browser.close()

current_script_path = os.path.abspath(__file__)
base_directory = os.path.dirname(current_script_path)

os.chdir(base_directory)

nome_arquivo = "pesquisa-pregao.zip"   
if os.path.exists(nome_arquivo):
    os.remove(nome_arquivo)
    
if os.path.exists("MaximumTheoreticalMargin.csv"):
    os.remove("MaximumTheoreticalMargin.csv")

downloadMargem()

extraiMargem(nome_arquivo,base_directory)

