import streamlit as st
import mysql.connector
from mysql.connector import Error

# --- Função de conexão ---
def create_connection(host, database, user, password):
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if conn.is_connected():
            st.success("✅ Conexão bem-sucedida com o banco de dados!")
            return conn
    except Error as e:
        st.error(f"❌ Erro na conexão: {e}")
        return None


# --- Layout Streamlit ---
st.title("🔌 Conexão com Banco de Dados")

host = st.text_input("IP/Host do Banco", placeholder="ex: 127.0.0.1")
database = st.text_input("Nome do Banco de Dados", placeholder="ex: minha_base")
user = st.text_input("Usuário", placeholder="ex: root")
password = st.text_input("Senha", type="password")

if st.button("Conectar"):
    conn = create_connection(host, database, user, password)
    if conn:
        st.session_state.conn = conn
