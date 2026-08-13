# conexao.py
# Arquivo responsável apenas por conectar ao banco MySQL
 
import mysql.connector          # importa a biblioteca para conectar ao MySQL
from mysql.connector import Error  # importa a classe de erro do MySQL
 
# --- CONFIGURAÇÃO DO BANCO (AJUSTE AQUI CONFORME SEU AMBIENTE) ---
HOST = "localhost"              # endereço do servidor MySQL (geralmente localhost)
USUARIO = "root"                # nome do usuário do MySQL
SENHA = ""                      # senha do usuário (deixe vazio se não tiver senha)
BANCO = "cantina"               # nome do banco de dados já criado
# ----------------------------------------------------------------
 
 
def conectar():
    # Função que abre a conexão com o MySQL e devolve o objeto connection
    try:                                          # tenta executar o bloco abaixo
        conn = mysql.connector.connect(          # cria a conexão com o banco
            host=HOST,                          # informa o endereço do servidor
            user=USUARIO,                       # informa o usuário
            password=SENHA,                     # informa a senha
            database=BANCO                      # seleciona o banco "cantina"
        )
        return conn                             # retorna a conexão aberta
    except Error as e:                          # se der erro na conexão
        print(f"Erro ao conectar ao MySQL: {e}")  # mostra a mensagem de erro
        return None                             # retorna None indicando falha

# pip install mysql-connector-python

