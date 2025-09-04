import setuptools 
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
import subprocess
import re


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
    options.add_argument("--headless=chrome")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    
    # força o uc a usar a versão exata do Chromium no container
    navegador = uc.Chrome(
        version_main=120,  # versão do Chromium do Streamlit Cloud
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


            # Ajusta o seletor para algo que aparece quando a página tá pronta
           # elemento = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
           # print(f"Página carregada em {url}!")

            # Espera até o input de usuário aparecer
            usuario_input = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            senha_input = wait.until(EC.element_to_be_clickable((By.ID, "senha")))
            entrar_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "arrow-wrapper")))

            
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
            # ...existing code...

            # Salva no session_state
            st.session_state["usuario"] = usuario
            st.session_state["senha"] = senha
            # ...existing code...
            
            st.success(f"Login automático feito em {url}! 🚀")
            
            
            # espera até 10 segundos para os elementos aparecerem
            time.sleep(2)
            
            
            
            pesquisar = wait.until(EC.presence_of_element_located((By.ID,"pesMenu")))
            pesquisar.send_keys("Gerenciamento de Notícias")
                
            # Screenshot após pesquisa
            screenshot_pesquisa = navegador.get_screenshot_as_png()
            image_pesquisa = Image.open(io.BytesIO(screenshot_pesquisa))
            st.image(image_pesquisa, caption=f"Screenshot após pesquisa em {url}", use_container_width=True)
            st.write("Título após pesquisa:", navegador.title)


            # clicar na barra de pesquisar menu
            pesquisar = wait.until(EC.presence_of_element_located((By.ID,"pesMenu")))
            pesquisar.send_keys("Gerenciamento de Notícias")
          
            # Screenshot antes do clique no menu
            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Antes do clique no menu")


            st.info("Buscando menu 'Gerenciamento de Notícias'...")
            
            # Busca o elemento mesmo oculto
            opcao = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Gerenciamento de Notícias')]"))
            )

            # Torna visível (se necessário)
            navegador.execute_script("arguments[0].style.display = 'block';", opcao)
            time.sleep(0.5)

            # Tenta clicar via JS
            navegador.execute_script("arguments[0].click();", opcao)
                
            
            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Depois do clique no menu")
            # ...existing code...
            
            # Screenshot após acessar o menu Gerenciamento de Notícias
            screenshot_menu = navegador.get_screenshot_as_png()
            image_menu = Image.open(io.BytesIO(screenshot_menu))
            st.image(image_menu, caption=f"Screenshot após acessar menu em {url}", use_container_width=True)
            st.write("Título após acessar menu:", navegador.title)
            
            # espera até 10 segundos para os elementos aparecerem
            time.sleep(2)
            
            # Espera até o botão estar clicável
            # ...existing code...

            # Espera até o botão estar clicável
            adicionar = wait.until(EC.element_to_be_clickable((By.ID, "btn-sis-gerenciamento-noticias-add")))

            if adicionar is None:
                st.error("Botão 'Adicionar' não encontrado!")
            else:
                st.success("Botão 'Adicionar' encontrado e pronto para clique.")
                adicionar.click()
                st.info("Clique em 'Adicionar' realizado.")
                # Screenshot após clicar em Adicionar
                screenshot_modal = navegador.get_screenshot_as_png()
                image_modal = Image.open(io.BytesIO(screenshot_modal))
                st.image(image_modal, caption="Screenshot após clicar em Adicionar")
                # Exibe HTML do modal (se existir)
                try:
                    modal = wait.until(EC.presence_of_element_located((By.ID, "modalNoticia")))
                except Exception as e:
                    st.warning("Modal não encontrado após clicar em Adicionar.")
                    st.error(str(e))

            # ...continue o fluxo normalmente...
            
            # ...existing code...

            try:
                # Preenche título
                titulo = wait.until(EC.element_to_be_clickable((By.ID, "titulo")))
                titulo.clear()
                titulo.send_keys(TITULO or "Título de Teste")
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher título")
            
                # Ativa modo código do editor
                botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
                botao_codeview.click()
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após ativar codeview")
            
                # Preenche conteúdo HTML
                codable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.note-codable")))
                navegador.execute_script("arguments[0].value = arguments[1];", codable, HTML or "<p>Conteúdo de teste</p>")
                navegador.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", codable)
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher conteúdo")
                
                # ...após preencher conteúdo HTML...
                # Fecha o modo código (volta ao modo visual)
                botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
                botao_codeview.click()
                time.sleep(0.5)
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após fechar codeview")
            
                # Preenche Data Inicial
                data_inicio = wait.until(EC.element_to_be_clickable((By.ID, "dataInicio")))
                data_inicio.clear()
                data_inicio.send_keys(DATA_INICIO or "01/01/2025")
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data início")
            
                # Preenche Data Final
                data_fim = wait.until(EC.element_to_be_clickable((By.ID, "dataFim")))
                data_fim.clear()
                data_fim.send_keys(DATA_FIM or "31/12/2025")
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data fim")
            
                # Preenche Prioridade
                prioridade = wait.until(EC.element_to_be_clickable((By.ID, "prioridade")))
                prioridade.clear()
                prioridade.send_keys("1")
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher prioridade")
            
                from selenium.webdriver.common.action_chains import ActionChains

                # Seleciona Status (Select2)
                selecao_status = wait.until(EC.element_to_be_clickable((By.ID, "s2id_status")))
                ActionChains(navegador).move_to_element(selecao_status).click().perform()
                time.sleep(0.5)
                
                # Tenta todos os seletores possíveis para o campo de busca
                search_input = None
                for selector in [".select2-input", ".select2-search__field", "ul.select2-results li input"]:
                    try:
                        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                    
                if not search_input:
                    raise Exception("Campo de busca do Select2 (Status) não encontrado!")
                
                search_input.clear()
                search_input.send_keys("Ativo")
                time.sleep(0.5)
                
                # Tenta todos os seletores possíveis para o item
                item = None
                for xpath in [
                    "//div[contains(@class,'select2-result-label') and text()='Ativo']",
                    "//li[contains(@class,'select2-results__option') and text()='Ativo']",
                    "//ul/li[.//text()[normalize-space()='Ativo']]"
                ]:
                    try:
                        item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                        break
                    except:
                        continue
                    
                if not item:
                    raise Exception("Item 'Ativo' do Select2 (Status) não encontrado!")
                
                item.click()
                navegador.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.5)
                
                # Seleciona Grupo (Select2)
                selecao_grupos = wait.until(EC.element_to_be_clickable((By.ID, "s2id_grupos")))
                ActionChains(navegador).move_to_element(selecao_grupos).click().perform()
                time.sleep(0.5)
                
                search_input_grupos = None
                for selector in [".select2-input", ".select2-search__field", "ul.select2-results li input"]:
                    try:
                        search_input_grupos = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                    
                if not search_input_grupos:
                    raise Exception("Campo de busca do Select2 (Grupo) não encontrado!")
                
                search_input_grupos.clear()
                search_input_grupos.send_keys("admin")
                time.sleep(0.5)
                
                item_grupo = None
                for xpath in [
                    "//div[contains(@class,'select2-result-label') and text()='admin']",
                    "//li[contains(@class,'select2-results__option') and text()='admin']",
                    "//ul/li[.//text()[normalize-space()='admin']]"
                ]:
                    try:
                        item_grupo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                        break
                    except:
                        continue
                    
                if not item_grupo:
                    raise Exception("Item 'admin' do Select2 (Grupo) não encontrado!")
                
                item_grupo.click()
                navegador.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.5)

                # Clique em salvar
                salvar = wait.until(EC.element_to_be_clickable((By.ID, "salvar-gerenciamento-noticia")))
                salvar.click()
                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em salvar")

                st.success("Notícia criada com sucesso!")

# ...existing code...
            
            except Exception as e:
                st.error(f"Erro no fluxo de criação da notícia: {e}")

# ...existing code...

    #        # Preenche título
    #        try:
    #            titulo = wait.until(EC.element_to_be_clickable((By.ID, "titulo")))
    #            if titulo is None:
    #                st.error("Campo título não encontrado!")
    #            else:
    #                st.success("Campo título encontrado.")
    #                titulo.clear()
    #                titulo.send_keys(TITULO)
    #                st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher título")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher título: {e}")
#
    #        # Ativa modo código do editor
    #        try:
    #            botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
    #            botao_codeview.click()
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após ativar codeview")
    #        except Exception as e:
    #            st.error(f"Erro ao ativar codeview: {e}")
#
    #        try:
    #            titulo = wait.until(EC.element_to_be_clickable((By.ID, "titulo")))
    #            st.success("Campo título encontrado.")
    #            titulo.clear()
    #            titulo.send_keys(TITULO)
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher título")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher título: {e}")
#
    #        try:
    #            botao_codeview = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
    #            botao_codeview.click()
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após ativar codeview")
    #        except Exception as e:
    #            st.error(f"Erro ao ativar codeview: {e}")
#
    #        try:
    #            codable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.note-codable")))
    #            navegador.execute_script("arguments[0].value = arguments[1];", codable, HTML)
    #            navegador.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", codable)
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher conteúdo")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher conteúdo: {e}")
#
    #        # Preenche Data Inicial
    #        try:
    #            data_inicio = wait.until(EC.element_to_be_clickable((By.ID, "dataInicio")))
    #            data_inicio.clear()
    #            data_inicio.send_keys(DATA_INICIO or "01/01/2025")
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data início")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher data início: {e}")
#
    #        # Preenche Data Final
    #        try:
    #            data_fim = wait.until(EC.element_to_be_clickable((By.ID, "dataFim")))
    #            data_fim.clear()
    #            data_fim.send_keys(DATA_FIM or "31/12/2025")
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher data fim")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher data fim: {e}")
#
    #        # Preenche Prioridade
    #        try:
    #            prioridade = wait.until(EC.element_to_be_clickable((By.ID, "prioridade")))
    #            prioridade.clear()
    #            prioridade.send_keys("1")
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após preencher prioridade")
    #        except Exception as e:
    #            st.error(f"Erro ao preencher prioridade: {e}")
#
    #        # Seleciona Status (Select2)
    #        try:
    #            selecao_status = wait.until(EC.element_to_be_clickable((By.ID, "s2id_status")))
    #            selecao_status.click()
    #            search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-input")))
    #            search_input.send_keys("Ativo")
    #            item = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'select2-result-label') and text()='Ativo']")))
    #            item.click()
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após selecionar status")
    #        except Exception as e:
    #            st.error(f"Erro ao selecionar status: {e}")
#
    #        # Seleciona Grupo (Select2)
    #        try:
    #            selecao_grupos = wait.until(EC.element_to_be_clickable((By.ID, "s2id_grupos")))
    #            selecao_grupos.click()
    #            search_input_grupos = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-input")))
    #            search_input_grupos.send_keys("admin")
    #            item_grupo = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'select2-result-label') and text()='admin']")))
    #            item_grupo.click()
    #            st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após selecionar grupo")
    #        except Exception as e:
    #            st.error(f"Erro ao selecionar grupo: {e}")
#
    #        # Continue assim para status, grupos e salvar...
    #        
    #        # Clique em salvar
    #        salvar = wait.until(EC.element_to_be_clickable((By.ID, "salvar-gerenciamento-noticia")))
    #        salvar.click()
    #        st.image(Image.open(io.BytesIO(navegador.get_screenshot_as_png())), caption="Após clicar em salvar")


            # adicionar título
            #titulo = WebDriverWait(navegador, 2).until(
            #    EC.element_to_be_clickable((By.ID,"titulo"))
            #)
            #titulo.clear()
            #titulo.send_keys(TITULO)
            
            # abrir o contêiner dos botões
            #container = wait.until(
            #    EC.visibility_of_element_located(
            #        (By.CSS_SELECTOR, "div.note-btn-group.btn-group.note-view")
            #    )
            #)
            ## localiza o botão desejado
            #botao_codeview = wait.until(
            #    EC.presence_of_element_located((By.CSS_SELECTOR, "button.note-btn.btn.btn-default.btn-sm.btn-codeview"))
            #)   
            #
            ## aguarda carregar o botão e clica nele
            #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
            #botao_codeview.click()
            #
            ## espera até a classe "active" aparecer
            #wait.until(lambda d: "active" in botao_codeview.get_attribute("class"))
            #
            ## abrir o contêiner do editor de texto
            #area = wait.until(
            #    EC.visibility_of_element_located((By.CSS_SELECTOR, ".note-editing-area"))
            #)
            #
            ##acha a textarea.note-codable
            #codable = wait.until(
            #    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.note-codable"))
            #)
            #html_content = HTML
            #
            ## injeta o HTML no atributo value
            #navegador.execute_script(
            #    "arguments[0].value = arguments[1];", codable, html_content
            #)
            #
            ## dispara evento 'input' → editor percebe que mudou
            #navegador.execute_script(
            #    "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
            #    codable
            #)
            #
            ## se o site salva ao perder foco, você pode dar um 'blur':
            #navegador.execute_script("arguments[0].blur();", codable)
            #
            ## fechar o contêiner dos botões
            #container = wait.until(
            #    EC.visibility_of_element_located(
            #        (By.CSS_SELECTOR, "div.note-btn-group.btn-group.note-view")
            #    )
            #)
            ## localiza o botão desejado
            #botao_codeview = container.presence_of_element_located(
            #    By.CSS_SELECTOR,
            #    "button.note-btn.btn.btn-default.btn-sm.btn-codeview"
            #)
            ## aguarda carregar o botão e clica nele
            #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.note-btn.btn-codeview")))
            #botao_codeview.click()
            ## preencher data de inicio e fim
            #def preencher_data_com_foco(campo_id, valor):
            #    campo = wait.until(EC.element_to_be_clickable((By.ID, campo_id)))
            #    campo.clear()
            #    campo.send_keys(valor)
            #    # clique fora para perder foco e fechar pop-up
            #    try:
            #        elemento_fora = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            #        ActionChains(navegador).move_to_element(elemento_fora).click().perform()
            #    except Exception as e:
            #        print("⚠️ Erro ao clicar fora (ignorado):", e)
            ## ---- uso real ----
            #preencher_data_com_foco("dataInicio", DATA_INICIO)
            #preencher_data_com_foco("dataFim",  DATA_FIM)
            ## adicionar prioridade
            #prioridade = wait.until(EC.presence_of_element_located
            #    (By.ID, "prioridade")
            #)
            #prioridade.send_keys("1")
            ## abrir seleção de status
            #selecao = wait.until(EC.presence_of_element_located(
            #    (By.ID,
            #    "s2id_status"))
            #)
            #selecao.click()
            ## clicar na situação
            #select = wait.until(
            #    EC.element_to_be_clickable((By.XPATH,"//ul[contains(@class,'select2-results')]//div[normalize-space()='Ativo']"))
            #)
            #select.click()
            ## achar o campo grupos
            #seletor = wait.until(EC.presence_of_element_located(
            #    (By.ID,"s2id_grupos"))
            #)
            #seletor.click()
            ## entra na div que esta o campo de grupos
            #camp = wait.until(
            #    EC.visibility_of_element_located((By.CSS_SELECTOR,"div.select2-container.select2-container-multi.form-control.select2-dropdown-open"))
            #)
            ## delimita quais campos e a sequência que existe dentro da div
            #search_input = wait.until(
            #    EC.presence_of_element_located((By.CSS_SELECTOR,"ul li input"))
            #)
            ##digita o valor da busca
            #search_input.send_keys("admin")
            ## esoera o li aparecer e seleciona o nome do grupo
            #item = wait.until(EC.element_to_be_clickable((
            #    By.XPATH,
            #    "//ul/li[.//text()[normalize-space()='admin']]"
            #)))
            #item.click()
            ## seleciona o botão salvar
            #salvar = wait.until(EC.presence_of_element_located(
            #    (By.ID, "salvar-gerenciamento-noticia"))
            #)
            #salvar.click()
            # espera até 3 segundos para os elementos aparecerem
            time.sleep(3)
            
        except Exception as e:
            st.warning(f"Não consegui logar em {url}. Confira os seletores!")
            st.error(str(e))
    
        print("Processo finalizado, fechando navegador.")

        navegador.quit()