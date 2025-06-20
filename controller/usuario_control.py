from view.db import get_db_connection, close_db_connection
import sqlite3

def insert_cadastro(email, senha):
    cadastro_string = f"INSERT INTO usuarios (id, nome, email, senha, saldo, tipo_de_investidor) VALUES (NULL, 'Usuario', ?, ?, 0.00, 'Conservador')"

    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        close_db_connection(conn, cursor)
        print(f"Erro ao conectar ao banco: {e}")

    if conn and cursor:
        cursor.execute(cadastro_string, (email, senha))

        try:
            conn.commit()
        except sqlite3.Error as e:
            close_db_connection(conn, cursor)
            print(f"Erro ao executar insert: {e}")
        finally:
            close_db_connection(conn, cursor)

def select_login(email, senha):
    try:
        conn, cursor = get_db_connection()

        if conn and cursor:
            query = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
            cursor.execute(query, (email, senha))
            resultado = cursor.fetchone()

            if resultado:
                print("Login bem-sucedido!")
                return True 
            else:
                print("Email ou senha incorretos.")
                return False

    except sqlite3.Error as e:
        print(f"Erro ao executar select: {e}")
        return False

    finally:
        close_db_connection(conn, cursor)