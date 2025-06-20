import sqlite3
from view.db import get_db_connection, close_db_connection

def usuarioModel():
    conn, cursor = None, None # Inicializa para garantir que sejam None se houver erro
    try:
        # 1. Obtém a conexão e o cursor
        conn, cursor = get_db_connection()

        if conn and cursor: # Verifica se a conexão foi bem-sucedida
            # Exemplo: Criar uma tabela (se ainda não existir)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    senha TEXT NOT NULL,
                    saldo REAL,
                    tipo_de_investidor TEXT
                )
            ''')
            conn.commit()
            print("Tabela 'usuarios' verificada/criada.")
        else:
            print("Não foi possível estabelecer a conexão com o banco de dados.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro no aplicativo: {e}")
    finally:
        # 3. Fecha a conexão ao finalizar (ou em caso de erro)
        close_db_connection(conn, cursor)

