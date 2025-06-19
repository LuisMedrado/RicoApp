import sqlite3

def get_db_connection():
    """
    Estabelece e retorna a conexão com o banco de dados e um objeto cursor.
    """
    try:
        conn = sqlite3.connect('ricoapp.db')
        conn.row_factory = sqlite3.Row # Opcional: para acessar colunas por nome
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None # Retorna None em caso de erro

def close_db_connection(conn, cursor):
    """
    Fecha a conexão com o banco de dados.
    """
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Conexão com o banco de dados fechada.")