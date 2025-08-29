import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

def test_streamlit_app():
    # 1️⃣ Inicia o Streamlit em background (porta 8501)
    process = subprocess.Popen(
        ["streamlit", "run", "noticias.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # 2️⃣ Espera o servidor subir com healthcheck
    url = "http://localhost:8501"
    for i in range(60):  # tenta até 60 vezes (~1 min)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print("✅ Streamlit subiu!")
                break
        except requests.exceptions.ConnectionError:
            pass
        print(f"⏳ Esperando Streamlit subir... ({i+1}/60)")
        time.sleep(1)
    else:
        process.terminate()
        raise Exception("Streamlit não respondeu a tempo")

    # 3️⃣ Configura o Selenium em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")  # caminho do Chromedriver no GitHub Actions
    driver = webdriver.Chrome(service=service, options=options)

    # 4️⃣ Abre o app via Selenium
    driver.get(url)
    assert "Streamlit" in driver.title  # verifica se o título contém "Streamlit"

    # 5️⃣ Finaliza
    driver.quit()
    process.terminate()
