import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Carrega os IDs válidos do arquivo JSON
with open("cities_amazon.json", "r") as f:
    data = json.load(f)

# Configurações do navegador
download_path = os.path.abspath("sheets_cities")  # Crie a pasta se não existir
os.makedirs(download_path, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")  # roda sem abrir a janela (remova se quiser ver o navegador)
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Inicializa o navegador
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 5)

# IDs com erro durante o processo
erro_ids = []

try:
    for el in data:
        id = el["id"]
        city = el["cidade"]
        state = el["estado"]
        
        print(f"🔍 Processando ID {id}...")

        url = f"https://www.painelsaneamento.org.br/localidade?id={id}"
        driver.get(url)

        try:
            download_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "control-edit")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
            time.sleep(1)
            download_button.click()
            time.sleep(2)  # Aguarda o download começar (ajuste se necessário)

            # renomeia o arquivo baixado
            downloaded_files = os.listdir(download_path)
            if downloaded_files:
                latest_file = max([os.path.join(download_path, f) for f in downloaded_files], key=os.path.getctime)
                new_file_name = f"{id}_{city}_{state}.xlsx"
                new_file_path = os.path.join(download_path, new_file_name)
                os.rename(latest_file, new_file_path)
                print(f"📥 Arquivo baixado e renomeado para: {new_file_name}")

            print(f"✅ Download iniciado para ID {id}")

        except (TimeoutException, NoSuchElementException):
            print(f"⚠️ Erro ao processar ID {id}, sem botão ou problema na página.")
            erro_ids.append(id)
            continue

finally:
    if erro_ids:
        print("IDs com erro:", erro_ids)
        # salva os IDs com erro em um arquivo JSON
        with open("ids_erro.json", "w") as f:
            json.dump({"ids": erro_ids}, f, indent=4)
    else:
        print("Todos os downloads iniciados com sucesso!")
    driver.quit()
