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
    conn, cursor = None, None # Inicializa para garantir que sejam None em caso de erro inicial
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            # 1. Use placeholders (ponto de interrogação '?' para cada valor)
            cadastro_string = """INSERT INTO usuarios (id, nome, email, senha, saldo, tipo_de_investidor)
                                 VALUES (?, ?, ?, ?, ?, ?)"""

            # 2. Passe os valores como uma tupla para o execute()
            # O NULL para o ID é padrão para colunas AUTOINCREMENT PRIMARY KEY
            valores_admin = (None, 'Admin', 'Admin@email.com', 'Admin123', 100.00, 'Conservador')

            cursor.execute(cadastro_string, valores_admin) # Passa a tupla com os valores
            conn.commit()
            print("Admin cadastrado com sucesso!")
            return True

        except sqlite3.Error as e:
            # Erros comuns: UNIQUE constraint failed (se já houver um admin com esse email)
            # ou tabela não existe.
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)
    else: # Caso a conexão falhe antes do try interno
        return "Erro inesperado: Conexão não estabelecida."