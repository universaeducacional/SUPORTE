from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
import time
import json
import io
import streamlit as st
import subprocess
import requests
from PIL import Image


st.title("Portal de acesso automático")

with st.form("login_form"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    submit = st.form_submit_button("Abrir páginas no Chrome")



# localicar o caminho do .env para preenchimento dos dados necessários para a configuração
load_dotenv(dotenv_path="./load_dotenv(dotenv_path=./configurar_noticias/dados_formulario.env")

# valores das variáveis
TITULO = os.getenv("TITULO") 
HTML = os.getenv("HTML")
DATA_INICIO = os.getenv("DATA_INICIO")
DATA_FIM = os.getenv("DATA_FIM")



# --- Caminho do JSON ---
base_path = os.path.dirname(__file__)  # diretório do app.py
json_path = os.path.join(base_path, 'urls.json')
            
            
if submit:
    st.success("Rodando Selenium headless no servidor...")

    # Inicializa Selenium headless
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.binary_location = "/usr/bin/chromium-browser"
    
    navegador = uc.Chrome(options=options)
   # wait = WebDriverWait(navegador, 10)

    # Carrega URLs do JSON
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        urls = data.get("urls", [])
    except FileNotFoundError:
        st.error(f"Não encontrei o arquivo urls.json em {json_path}")
        urls = []

    st.write(f"{len(urls)} URLs encontradas:")

    for url in urls:
        st.write(f"🔗 {url}")
        navegador.get(url)

        # Espera body carregar
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except:
            st.warning(f"Timeout ao carregar {url}")
            continue

        time.sleep(1)

        # Screenshot
        screenshot = navegador.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        st.image(image, caption=f"Screenshot de {url}", use_container_width=True)
        st.write("Título:", navegador.title)

    
        try: 


            # Ajusta o seletor para algo que aparece quando a página tá pronta
           # elemento = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
           # print(f"Página carregada em {url}!")

            # selecionar um elemento na tela
            entrar = navegador.find_element(By.CLASS_NAME, "arrow-wrapper")
            # escrever em um campo formulário
            navegador.find_element(By.NAME ,"username").send_keys(usuario)
            navegador.find_element(By.ID,"senha").send_keys(senha)
            # clicar em um elemento 
            entrar.click()
            st.success(f"Login automático feito em {url}! 🚀")
            # espera até 10 segundos para os elementos aparecerem
            time.sleep(2)
            # clicar na barra de pesquisar menu
            pesquisar = navegador.find_element(By.ID,"pesMenu")
            pesquisar.send_keys("Gerenciamento de Notícias")
            opcao = WebDriverWait(navegador, 2).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//li[normalize-space(.)='Gerenciamento de Notícias']"))
            )
            opcao.click()
            # espera até 10 segundos para os elementos aparecerem
            time.sleep(2)
            # clicar em adicionar nova noticia
            adicionar = navegador.find_element(By.ID,"btn-sis-gerenciamento-noticias-add")
            adicionar.click()
            # adicionar título
            titulo = WebDriverWait(navegador, 2).until(
                EC.element_to_be_clickable((By.ID,"titulo"))
            )
            titulo.clear()
            titulo.send_keys(TITULO)
            # abrir o contêiner dos botões
            container = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.note-btn-group.btn-group.note-view")
                )
            )
            # localiza o botão desejado
            botao_codeview = container.find_element(
                By.CSS_SELECTOR,
                "button.note-btn.btn.btn-default.btn-sm.btn-codeview"
            )
            # aguarda carregar o botão e clica nele
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
            botao_codeview.click()
            # espera até a classe "active" aparecer
            wait.until(lambda d: "active" in botao_codeview.get_attribute("class"))
            # abrir o contêiner do editor de texto
            area = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".note-editing-area")
                )
            )
            #acha a textarea.note-codable
            codable = area.find_element(
                By.CSS_SELECTOR, "textarea.note-codable"
            )
            html_content = HTML
            # injeta o HTML no atributo value
            navegador.execute_script(
                "arguments[0].value = arguments[1];", codable, html_content
            )
            # dispara evento 'input' → editor percebe que mudou
            navegador.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
                codable
            )
            # se o site salva ao perder foco, você pode dar um 'blur':
            navegador.execute_script("arguments[0].blur();", codable)
            # fechar o contêiner dos botões
            container = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.note-btn-group.btn-group.note-view")
                )
            )
            # localiza o botão desejado
            botao_codeview = container.find_element(
                By.CSS_SELECTOR,
                "button.note-btn.btn.btn-default.btn-sm.btn-codeview"
            )
            # aguarda carregar o botão e clica nele
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
            botao_codeview.click()
            # preencher data de inicio e fim
            def preencher_data_com_foco(campo_id, valor):
                campo = wait.until(EC.element_to_be_clickable((By.ID, campo_id)))
                campo.clear()
                campo.send_keys(valor)
                # clique fora para perder foco e fechar pop-up
                try:
                    elemento_fora = navegador.find_element(By.TAG_NAME, "body")
                    ActionChains(navegador).move_to_element(elemento_fora).click().perform()
                except Exception as e:
                    print("⚠️ Erro ao clicar fora (ignorado):", e)
            # ---- uso real ----
            preencher_data_com_foco("dataInicio", DATA_INICIO)
            preencher_data_com_foco("dataFim",  DATA_FIM)
            # adicionar prioridade
            prioridade = navegador.find_element(
                By.ID, "prioridade"
            )
            prioridade.send_keys("1")
            # abrir seleção de status
            selecao = navegador.find_element(
                By.ID,
                "s2id_status"
            )
            selecao.click()
            # clicar na situação
            select = wait.until(
                EC.element_to_be_clickable((By.XPATH,"//ul[contains(@class,'select2-results')]//div[normalize-space()='Ativo']"))
            )
            select.click()
            # achar o campo grupos
            seletor = navegador.find_element(
                By.ID,"s2id_grupos"
            )
            seletor.click()
            # entra na div que esta o campo de grupos
            camp = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"div.select2-container.select2-container-multi.form-control.select2-dropdown-open"))
            )
            # delimita quais campos e a sequência que existe dentro da div
            search_input = camp.find_element(
                By.CSS_SELECTOR,"ul li input"
            )
            #digita o valor da busca
            search_input.send_keys("admin")
            # esoera o li aparecer e seleciona o nome do grupo
            item = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//ul/li[.//text()[normalize-space()='admin']]"
            )))
            item.click()
            # seleciona o botão salvar
            salvar = navegador.find_element(
                By.ID, "salvar-gerenciamento-noticia"
            )
            salvar.click()
            # espera até 3 segundos para os elementos aparecerem
            time.sleep(3)
            
        except Exception as e:
                st.warning(f"Não consegui logar em {url}. Confira os seletores!")
                st.error(str(e))
    
        print("Processo finalizado, fechando navegador.")

        navegador.quit()