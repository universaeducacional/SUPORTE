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

    # 2️⃣ Espera o servidor subir
    time.sleep(15)  # 15 segundos para garantir que o app esteja online

    # 3️⃣ Verifica se a página responde (opcional)
    try:
        resp = requests.get("http://localhost:8501")
        assert resp.status_code == 200
    except Exception as e:
        process.terminate()
        raise e

    # 4️⃣ Configura o Selenium em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")  # caminho do Chromedriver no GitHub Actions
    driver = webdriver.Chrome(service=service, options=options)

    # 5️⃣ Abre o app via Selenium
    driver.get("http://localhost:8501")
    assert "Streamlit" in driver.title  # verifica se o título contém "Streamlit"

    # 6️⃣ Finaliza
    driver.quit()
    process.terminate()
