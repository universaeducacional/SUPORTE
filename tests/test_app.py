import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

def test_streamlit_app():
    # 1️⃣ Inicia o Streamlit em background (porta 8501)
    process = subprocess.Popen(
        ["streamlit", "run", "configurar_noticias/noticias.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    url = "http://localhost:8501"

    # 2️⃣ Healthcheck: tenta até 60 vezes (~1 min)
    for i in range(60):
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
        # Se não subir, captura os logs e termina o processo
        out, _ = process.communicate(timeout=5)
        print("=== LOGS DO STREAMLIT ===")
        print(out)
        process.terminate()
        raise Exception("Streamlit não respondeu a tempo")

    # 3️⃣ Configura Selenium em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")  # ajuste pro GitHub Actions
    driver = webdriver.Chrome(service=service, options=options)

    # 4️⃣ Abre o app via Selenium
    driver.get(url)
    assert "Streamlit" in driver.title

    # 5️⃣ Finaliza
    driver.quit()
    process.terminate()

