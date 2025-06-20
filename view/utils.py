from os import path, listdir
from pyglet import font as pfont

DIR_TELA = path.dirname(__file__)
PATH_FONTS = path.join(DIR_TELA, "fonts")

def carregar_fontes_globais():
    try:
        for nome_arq in listdir(PATH_FONTS):
            if nome_arq.lower().endswith((".ttf", ".otf")):
                nome_fonte = path.join(PATH_FONTS, nome_arq)
                pfont.add_file(nome_fonte)
    except FileNotFoundError:
        print(f"ERRO: Diretório de fontes '{PATH_FONTS}' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar fontes: {e}")
