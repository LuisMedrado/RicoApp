import customtkinter as ctk
from pyglet import font as pfont
from os import path, listdir
from PIL import Image
import webbrowser
from view.db import get_db_connection
from model.login.usuarioModel import usuarioModel
from model.jogoModel import jogoModel
from model.reviewModel import reviewsModel
from view.utils import carregar_fontes_globais
from controller.usuario_control import insertAdmin
import sys

# importar a classe das telas
from view.tela_login import telaLoginFrame
from view.tela_cadastro import TelaCadastro
from view.tela_dict import telaDictFrame
from view.paginas.tela_info1 import TelaInfo1Frame
from view.paginas.tela_info2 import TelaInfo2
from view.paginas.tela_info3 import TelaInfo3
from view.paginas.tela_info4 import TelaInfo4
from view.paginas.tela_info5 import TelaInfo5


# adicionar as outras pastas ao path
sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

# consts cores
DIR_TELA = path.dirname(__file__)
PATH_FONTS = path.join(DIR_TELA, "fonts")
PATH_IMGS = path.join(DIR_TELA, "images")

# cores
COR_HEADER = "#3f2a87"
COR_SUBHEADER = "#7a6ef5"
COR_FUNDO = "#2d234d"
COR_CLARA = "#e6e6f0"
COR_AZUL = "#7a6ef5"

# funcs
def abrirLink():
    link = "https://www.youtube.com/watch?v=30del_ojFfs"
    try:
        webbrowser.open_new_tab(link)
    except Exception as e:
        print(f"Não foi possível abrir o link: {e}")


# classe tela inicial
class telaInicialFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller):
        super().__init__(parent_container, fg_color=COR_FUNDO)
        self.controller = controller

        # header
        header = ctk.CTkFrame(self, height=60, fg_color=COR_HEADER, corner_radius=0)
        header.pack(fill="x", side="top")

        frame_menu = ctk.CTkFrame(header, fg_color="transparent")
        frame_menu.pack(side="right", padx=20, pady=(10, 10))

        self.carregar_img(header, "ricoIconVertical.png", 50, "w")

        btn_sobre = ctk.CTkButton(frame_menu, text="Sobre", fg_color="transparent", hover_color=COR_AZUL,
                                  font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"))
        btn_login = ctk.CTkButton(frame_menu, text="Login", fg_color="transparent", border_color="white",
                                  border_width=2, hover_color=COR_AZUL,
                                  font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"),
                                  command=lambda: controller.mostrar_frame(telaLoginFrame))  # NAVEGAÇÃO
        btn_cadastro = ctk.CTkButton(frame_menu, text="Cadastre-se", fg_color="white", text_color="black",
                                     hover_color="#d4d4d4",
                                     font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"),
                                     command=lambda: controller.mostrar_frame(TelaCadastro))
        # adicionar: command=lambda: controller.mostrar_frame(TelaCadastroFrame))

        btn_sobre.pack(side="left", padx=5)
        btn_login.pack(side="left", padx=5)
        btn_cadastro.pack(side="left", padx=5)

        subheader = ctk.CTkFrame(self, height=50, fg_color=COR_SUBHEADER, corner_radius=0)
        subheader.pack(fill="x", side="top")

        # conteudo principal
        frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=60)

        frame_conteudo.grid_columnconfigure(0, weight=2, uniform="group1")
        frame_conteudo.grid_columnconfigure(1, weight=3, uniform="group1")
        frame_conteudo.grid_rowconfigure(0, weight=1)

        # frame esquerda
        frame_esquerda = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 30))

        frame_esquerda_agrupador_outer = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_esquerda_agrupador_outer.pack(expand=True, anchor="w", padx=0)

        frame_esquerda_agrupador_inner = ctk.CTkFrame(frame_esquerda_agrupador_outer, fg_color="transparent")
        frame_esquerda_agrupador_inner.pack(pady=20)

        titulo = ctk.CTkLabel(frame_esquerda_agrupador_inner,
                              text="Construa\nseu império\ncomeçando do\ncompleto zero",
                              font=ctk.CTkFont(family="Roboto-Black", size=90, weight="bold"),
                              justify="left", text_color=COR_CLARA, anchor="w")
        titulo.pack(side="top", anchor="w", pady=(0, 30))

        frame_botoes = ctk.CTkFrame(frame_esquerda_agrupador_inner, fg_color="transparent")
        frame_botoes.pack(side="top", anchor="w")

        btn_entrar = ctk.CTkButton(frame_botoes, width=230, height=70,
                                   text="ENTRE AGORA",
                                   fg_color=COR_CLARA, text_color="black",
                                   hover_color="#d4d4d4", corner_radius=8,
                                   font=ctk.CTkFont(family="Roboto-Bold", size=20, weight="bold"),
                                   command=lambda: controller.mostrar_frame(telaLoginFrame))
        btn_entrar.pack(side="left", padx=(60, 100))

        btn_trailer = ctk.CTkButton(frame_botoes, width=230, height=70,
                                    text="▶ VEJA O TRAILER",
                                    fg_color=COR_AZUL, hover_color="#5f55c2", corner_radius=8,
                                    font=ctk.CTkFont(family="Roboto-Bold", size=20, weight="bold"),
                                    command=abrirLink)
        btn_trailer.pack(side="left")

        # frame direita
        frame_direita = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_direita.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.carregar_img(frame_direita, "porquinhoDinheiro.png", 925, "center")

        # footer
        rodape = ctk.CTkFrame(self, height=80, fg_color=COR_SUBHEADER, corner_radius=0)
        rodape.pack(fill="x", side="bottom")
        label_footer = ctk.CTkLabel(rodape,
                                    text="2025, RICO App. Projeto para a disciplina de Novas Tecnologias | UCB.",
                                    font=ctk.CTkFont(family="Roboto-Regular", size=12), text_color=COR_CLARA)
        label_footer.pack(expand=True)

    def carregar_img(self, parent_frame, nome_img, tamanho, ancoragem):
        nome_arquivo_imagem = nome_img
        path_img = path.join(PATH_IMGS, nome_arquivo_imagem)
        try:
            pil_original_image = Image.open(path_img)
            max_altura = tamanho
            original_width, original_height = pil_original_image.size
            aspect_ratio = original_width / float(original_height)

            img_altura_calc = max_altura
            img_larg_calc = int(img_altura_calc * aspect_ratio)

            pil_resized_image = pil_original_image.resize((img_larg_calc, img_altura_calc), Image.Resampling.LANCZOS)

            ctk_porquinho_image = ctk.CTkImage(light_image=pil_resized_image,
                                               dark_image=pil_resized_image,
                                               size=(img_larg_calc, img_altura_calc))

            label_img = ctk.CTkLabel(parent_frame, image=ctk_porquinho_image, text="")
            label_img.pack(anchor=ancoragem, expand=True, padx=20, pady=20)
        except FileNotFoundError:
            print(f"ERRO imagem '{path_img}' não encontrada.")

        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")


# classe principal
class appPrincipal(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        carregar_fontes_globais()

        self.title("RICO")
        # self.geometry("1920x1080")
        self.after(1, lambda: self.state("zoomed"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container_principal = ctk.CTkFrame(self, fg_color=COR_FUNDO, corner_radius=0)
        container_principal.grid(row=0, column=0, sticky="nsew")
        container_principal.grid_rowconfigure(0, weight=1)
        container_principal.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.PAGINAS = {
    'inicial': telaInicialFrame,
    'login': telaLoginFrame,
    'cadastro': TelaCadastro,
    'dict': telaDictFrame,
    'info1': TelaInfo1Frame,
    'info2': TelaInfo2,
    'info3': TelaInfo3,
    'info4': TelaInfo4,
    'info5': TelaInfo5
}

        for nome_pagina, frame_class in self.PAGINAS.items():
            frame = frame_class(parent_container=container_principal, controller=self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(telaInicialFrame)

    def mostrar_frame(self, classe_frame_alvo):
        """Diexa o frame especificado em foco na tela"""
        frame = self.frames.get(classe_frame_alvo)
        if frame:
            frame.tkraise()
        else:
            print(f"Erro: frame para a classe {classe_frame_alvo} não encontrado")

def iniciar_app():
    app = appPrincipal()
    app.mainloop()
    get_db_connection()
    usuarioModel()
    jogoModel()
    reviewsModel()
    insertAdmin()