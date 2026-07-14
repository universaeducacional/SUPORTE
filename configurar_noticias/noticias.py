import setuptools 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
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
import subprocess
import re


st.title("Portal de acesso automático")

with st.form("login_form"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    TITULO = st.text_input("Título da Notícia")
    HTML = st.text_area("Conteúdo HTML")
    DATA_INICIO = st.text_input("Data Início (DD/MM/AAAA)")
    DATA_FIM = st.text_input("Data Fim (DD/MM/AAAA)")
    submit = st.form_submit_button("Prosseguir")



# localicar o caminho do .env para preenchimento dos dados necessários para a configuração
#load_dotenv(dotenv_path="./load_dotenv(dotenv_path=./configurar_noticias/dados_formulario.env")

# valores das variáveis
#TITULO = os.getenv("TITULO") 
#HTML = os.getenv("HTML")
#DATA_INICIO = os.getenv("DATA_INICIO")
#DATA_FIM = os.getenv("DATA_FIM")



# --- Caminho do JSON ---
base_path = os.path.dirname(__file__)  # diretório do app.py
json_path = os.path.join(base_path, 'urls.json')
            
            
if submit:
    st.success("Rodando Selenium headless no servidor...")

    # Inicializa Selenium headless
    options = uc.ChromeOptions()
    options.add_argument("--headless=chrome")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    
    # força o uc a usar a versão exata do Chromium no container
    navegador = uc.Chrome(
        version_main=150,  # versão do Chromium do Streamlit Cloud
        options=options
    )
    
   # navegador = uc.Chrome(options=options)
    wait = WebDriverWait(navegador, 10)

    # Carrega URLs do JSON
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            st.error("Arquivo JSON inválido!")
            urls = []
        else:
            urls = data.get("urls", [])
    except FileNotFoundError:
        st.error(f"Não encontrei o arquivo urls.json em {json_path}")
        urls = []
    except json.JSONDecodeError:
        st.error("Erro ao ler o JSON!")
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
            # Espera até o input de usuário aparecer
            usuario_input = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            senha_input = wait.until(EC.element_to_be_clickable((By.ID, "senha")))
            entrar_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-login")))

            
            # Preenche o formulário e clica no botão
            usuario_input.send_keys(usuario)
            senha_input.send_keys(senha)
            entrar_btn.click()
            time.sleep(2)  # garante que a próxima ação tenha elementos carregados
            
            
            # Screenshot após login
            screenshot_login = navegador.get_screenshot_as_png()
            image_login = Image.open(io.BytesIO(screenshot_login))
            st.image(image_login, caption=f"Screenshot após login em {url}", use_container_width=True)
            st.write("Título após login:", navegador.title)


            # Salva no session_state
            st.session_state["usuario"] = usuario
            st.session_state["senha"] = senha

            st.success(f"Login automático feito em {url}! 🚀")
            
            
            # espera até 10 segundos para os elementos aparecerem
            time.sleep(2)
            
            # clicar na barra de pesquisar menu
            pesquisar = wait.until(EC.presence_of_element_located((By.ID,"pesMenu")))
            pesquisar.send_keys("Gerenciamento de Notícias")

          
            # Screenshot antes do clique no menu
            #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Antes do clique no menu")


            #st.info("Buscando menu 'Gerenciamento de Notícias'...")
            
            # Busca o elemento mesmo oculto
            opcao = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Gerenciamento de Notícias')]"))
            )

            # Torna visível (se necessário)
            navegador.execute_script("arguments[0].style.display = 'block';", opcao)
            time.sleep(0.5)

            # Tenta clicar via JS
            navegador.execute_script("arguments[0].click();", opcao)
                
            
            #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Depois do clique no menu")
            
            # Screenshot após acessar o menu Gerenciamento de Notícias
            #screenshot_menu = navegador.get_screenshot_as_png()
            #image_menu = Image.open(io.BytesIO(screenshot_menu))
            #st.image(image_menu, caption=f"Screenshot após acessar menu em {url}", use_container_width=True)
            #st.write("Título após acessar menu:", navegador.title)
            
            # espera até 5 segundos para os elementos aparecerem
            time.sleep(5)

            # Espera até o botão estar clicável
            adicionar = wait.until(EC.element_to_be_clickable((By.ID, "btn-sis-gerenciamento-noticias-add")))

            if adicionar is None:
                st.error("Botão 'Adicionar' não encontrado!")
            else:
                st.success("Botão 'Adicionar' encontrado e pronto para clique.")
                adicionar.click()
                st.info("Clique em 'Adicionar' realizado.")
                # Screenshot após clicar em Adicionar
                #screenshot_modal = navegador.get_screenshot_as_png()
                #image_modal = Image.open(io.BytesIO(screenshot_modal))
                #st.image(image_modal, caption="Screenshot após clicar em Adicionar")
                # Exibe HTML do modal (se existir)
                try:
                    modal = wait.until(EC.presence_of_element_located((By.ID, "modalNoticia")))
                except Exception as e:
                    st.warning("Modal não encontrado após clicar em Adicionar.")
                    st.error(str(e))
                    

            try:
                # Preenche título
                titulo = wait.until(EC.element_to_be_clickable((By.ID, "titulo")))
                titulo.clear()
                titulo.send_keys(TITULO)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher título")
            
                # Ativa modo código do editor
                botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
                botao_codeview.click()
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após ativar codeview")
            
                # Preenche conteúdo HTML
                codable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.note-codable")))
                navegador.execute_script("arguments[0].value = arguments[1];", codable, HTML)
                navegador.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", codable)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher conteúdo")
                
                # ...após preencher conteúdo HTML...
                # Fecha o modo código (volta ao modo visual)
                botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
                botao_codeview.click()
                time.sleep(0.5)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após fechar codeview")
            
                # Preenche Data Inicial
                data_inicio = wait.until(EC.element_to_be_clickable((By.ID, "dataInicio")))
                data_inicio.clear()
                data_inicio.send_keys(DATA_INICIO)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data início")
            
                # Preenche Data Final
                data_fim = wait.until(EC.element_to_be_clickable((By.ID, "dataFim")))
                data_fim.clear()
                data_fim.send_keys(DATA_FIM)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data fim")
            
                # Preenche Prioridade
                prioridade = wait.until(EC.element_to_be_clickable((By.ID, "prioridade")))
                prioridade.clear()
                prioridade.send_keys("3")
                prioridade.send_keys(Keys.ENTER)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher prioridade")

                # Seleciona Status (Select2 sem campo de busca)
                # abrir seleção de status
                # Aguarda o Select2 ficar clicável
                selecao = wait.until(
                    EC.element_to_be_clickable((By.ID, "s2id_status"))
                )

                # Centraliza o elemento na tela
                navegador.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    selecao
                )

                time.sleep(0.3)

                # Tenta clicar até 3 vezes
                for tentativa in range(3):
                    try:
                        selecao.click()
                        break
                    except ElementClickInterceptedException:
                        elemento = navegador.execute_script("""
                            var r = arguments[0].getBoundingClientRect();
                            return document.elementFromPoint(
                                r.left + r.width/2,
                                r.top + r.height/2
                        ).outerHTML;
                     """, selecao)

                    print(elemento)
                    st.code(elemento)

                    time.sleep(1)
                else:
                    raise Exception("Não foi possível clicar no campo Status.")

                # Aguarda a opção aparecer
                select = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//ul[contains(@class,'select2-results')]//div[normalize-space()='Ativo']"
                        )
                    )
                )

                select.click()
            
             #    selecao = navegador.find_element(
              #       By.ID,
             #        "s2id_status"
              #   )
             #    selecao.click()

                # clicar na situação
              #   select = wait.until(
             #        EC.element_to_be_clickable((By.XPATH,"//ul[contains(@class,'select2-results')]//div[normalize-space()='Ativo']"))
              #   )
              #   select.click()

                # achar o campo grupos
                seletor = navegador.find_element(
                    By.ID,"s2id_grupos"
                )
                seletor.click()
                time.sleep(0.5)

                
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em Status II")

                # --- Seleciona Grupo (Select2) ---
                # espera overlay sumir
                wait.until(EC.invisibility_of_element_located((By.ID, "select2-drop-mask")))

                # agora clica no select2
                elem = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_grupos"))
                )
                navegador.execute_script("arguments[0].click();", elem)
                
                # entra na div que esta o campo de grupos
                camp = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,"div.select2-container.select2-container-multi.form-control.select2-dropdown-open"))
                )
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em Prioridade I")
                
                # delimita quais campos e a sequência que existe dentro da div
                search_input = camp.find_element(
                    By.CSS_SELECTOR,"ul li input"
                )

                # clica no item pelo texto
                item = navegador.find_element(By.XPATH, "//ul/li[.//text()[normalize-space()='Home -Noticias']]")
                navegador.execute_script("arguments[0].click();", item)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em Prioridade AAII")

                
                campo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_grupos input.select2-input")))
                campo.send_keys("Home -Noticias")
                campo.send_keys(Keys.ENTER)
                #st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em Prioridade III")

                # Clique em salvar
                salvar = wait.until(EC.element_to_be_clickable((By.ID, "salvar-gerenciamento-noticia")))
                salvar.click()
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em salvar")

                st.success("Notícia criada com sucesso!")
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Notícia")
            except Exception as e:
                st.error(f"Erro no fluxo de criação da notícia: {e}")
                
            time.sleep(3)
            
        except Exception as e:
            st.warning(f"Não consegui logar em {url}. Confira os seletores!")
            st.error(str(e))
    
        print("Processo finalizado, fechando navegador.")


    navegador.quit()









