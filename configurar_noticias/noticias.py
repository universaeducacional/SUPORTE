from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import json
import streamlit as st
import subprocess
import requests




def test_streamlit_app():
    # Inicia o app Streamlit em background
    process = subprocess.Popen(
        ["streamlit", "run", "noticias.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Aguarda alguns segundos para o servidor subir
    time.sleep(10)

    # Verifica se a página responde
    resp = requests.get("http://localhost:8501")
    assert resp.status_code == 200

    # Configurações do Selenium (modo headless para rodar no CI)
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://localhost:8501")
    assert "Streamlit" in driver.title
    
    driver.quit()
    process.terminate()

