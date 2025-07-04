from view.db import get_db_connection, close_db_connection
import re
import sqlite3

def insert_cadastro(nome, email, senha):
    if not validar_email(email):
        print("Email inválido.")
        return "Email inválido."

    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            if cursor.fetchone():
                print("Email já cadastrado.")
                return "Email já cadastrado."

            cadastro_string = """INSERT INTO usuarios (id, nome, email, senha, saldo, tipo_de_investidor)
                                 VALUES (NULL, ?, ?, ?, 0.00, 'Conservador')"""
            cursor.execute(cadastro_string, (nome, email, senha))
            conn.commit()
            print("Cadastro realizado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."

def validar_email(email):
    """Valida se o email tá no formato certo"""
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

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

def insertAdmin():
    conn, cursor = None, None
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            # 1. Verificar se o admin já existe pelo email
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", ('admin@email.com',))
            admin_existente = cursor.fetchone()

            if admin_existente:
                print("Admin já existe no banco de dados.")
                return "Admin já existe."
            else:
                # 2. Se não existe, insere
                cadastro_string = """INSERT INTO usuarios (id, nome, email, senha, saldo, tipo_de_investidor)
                                     VALUES (?, ?, ?, ?, ?, ?)"""
                valores_admin = (None, 'Admin', 'admin@email.com', 'Admin123', 100.00, 'Conservador')

                cursor.execute(cadastro_string, valores_admin)
                conn.commit()
                print("Admin cadastrado com sucesso!")
                return True

        except sqlite3.Error as e:
            print(f"Erro ao executar operação: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)
    else:
        return "Erro inesperado: Conexão não estabelecida."