from view.db import get_db_connection, close_db_connection
import sqlite3

def insert_dicionario():
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            cadastro_string = """INSERT INTO usuarios (id, título, autor_artigo, data_artigo, conteudo_artigo)
                                 VALUES (NULL, 'Como aumentar seu pênis', 'Kid Bengala', 21/06/2025, 'Compra ai meu óleo que vai ficar grande')"""
            cursor.execute(cadastro_string)
            conn.commit()
            print("Cadastro realizado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."