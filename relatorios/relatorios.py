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