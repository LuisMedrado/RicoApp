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

# Dados escritos para as telas dicionário

def get_info_topico(topico):
    dados = {
        "guardar_investir": {
            "titulo": "Guardar também é investir?",
            "autor": "Equipe Rico",
            "data": "Junho de 2025",
            "descricao": (
                "Guardar dinheiro é o primeiro passo para começar a investir.\n\n"
                "Ao juntar uma parte do que você ganha, você cria uma reserva que pode crescer com o tempo — "
                "desde que aplicada da maneira certaaaaa.\n\n"
                "Investir não precisa ser complicado. O importante é começar!"
            )
        },
        "tipos_risco": {
            "titulo": "Entendendo os tipos de risco",
            "autor": "Equipe Rico",
            "data": "Junho de 2025",
            "descricao": (
                "Investir envolve riscos variados, como risco de mercado, risco de crédito e risco de liquidez.\n\n"
                "Conhecer esses riscos ajuda a tomar decisões mais seguras e conscientes."
            )
        }
    }
    return dados.get(topico, {
        "titulo": "Sem título",
        "autor": "Desconhecido",
        "data": "Data não informada",
        "descricao": "Sem descrição disponível."
    })