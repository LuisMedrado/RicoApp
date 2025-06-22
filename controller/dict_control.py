from view.db import get_db_connection, close_db_connection
import sqlite3

def insert_artigo_investimento_iniciante():
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            artigo_investimento_1 = """INSERT INTO usuarios (id, título, autor_artigo, data_artigo, conteudo_artigo)
                                     VALUES (NULL, 'Guia Completo de Investimentos em Ações para Iniciantes', 'Ana Clara Borges', '22/07/2025', 'Este guia aborda os fundamentos do mercado de ações, explicando como escolher suas primeiras ações, diversificar sua carteira e utilizar plataformas de home broker de forma segura e eficiente.')"""
            cursor.execute(artigo_investimento_1)
            conn.commit()
            print("Artigo sobre investimento em ações para iniciantes publicado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."

def insert_artigo_renda_fixa_digital():
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            artigo_investimento_2 = """INSERT INTO usuarios (id, título, autor_artigo, data_artigo, conteudo_artigo)
                                     VALUES (NULL, 'Renda Fixa Digital: Como Investir em CDB, LCI e LCA Online', 'Marcos Oliveira', '15/08/2025', 'Descubra as vantagens de investir em títulos de renda fixa através de bancos digitais e corretoras. Analisamos as melhores opções de CDB, LCI e LCA com boa liquidez e rentabilidade para proteger seu patrimônio.')"""
            cursor.execute(artigo_investimento_2)
            conn.commit()
            print("Artigo sobre renda fixa digital publicado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."

def insert_artigo_criptomoedas():
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            artigo_investimento_3 = """INSERT INTO usuarios (id, título, autor_artigo, data_artigo, conteudo_artigo)
                                     VALUES (NULL, 'Criptomoedas: Uma Análise de Risco e Potencial de Retorno', 'Juliana Rios', '01/09/2025', 'Bitcoin, Ethereum e outras altcoins podem oferecer altos retornos, mas também envolvem riscos significativos. Este artigo explora como funcionam as criptomoedas, estratégias de alocação e dicas para investir com mais segurança.')"""
            cursor.execute(artigo_investimento_3)
            conn.commit()
            print("Artigo sobre criptomoedas publicado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."

def insert_artigo_fiis():
    try:
        conn, cursor = get_db_connection()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return "Erro de conexão."

    if conn and cursor:
        try:
            artigo_investimento_4 = """INSERT INTO usuarios (id, título, autor_artigo, data_artigo, conteudo_artigo)
                                     VALUES (NULL, 'Como Receber Aluguéis Mensais com Fundos Imobiliários (FIIs)', 'Ricardo Almeida', '28/09/2025', 'Aprenda a investir em FIIs e a gerar uma fonte de renda passiva com dividendos mensais. Abordamos os melhores setores para investir, como analisar um fundo e os benefícios fiscais dessa modalidade de investimento.')"""
            cursor.execute(artigo_investimento_4)
            conn.commit()
            print("Artigo sobre Fundos Imobiliários publicado com sucesso!")
            return True

        except sqlite3.Error as e:
            print(f"Erro ao executar insert: {e}")
            return "Erro no cadastro."
        finally:
            close_db_connection(conn, cursor)

    return "Erro inesperado."