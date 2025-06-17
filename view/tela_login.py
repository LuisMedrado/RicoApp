import customtkinter as ctk
from PIL import Image, ImageTk
import os

# Cores
COR_ESQUERDA = "#1a132b"
COR_DIREITA = "#3e299a"
COR_CLARA = "#e6e6f0"
COR_AMARELA = "#f9d13b"
COR_BRANCA = "#ffffff"

# Caminhos
DIR_TELA = os.path.dirname(__file__)
PATH_IMGS = os.path.join(DIR_TELA, "images")

class telaLoginFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller):
        super().__init__(parent_container)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame Esquerdo
        frame_login = ctk.CTkFrame(self, fg_color=COR_ESQUERDA)
        frame_login.grid(row=0, column=0, sticky="nsew")
        frame_login.grid_columnconfigure(0, weight=1)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_rowconfigure(1, weight=1)
        frame_login.grid_rowconfigure(2, weight=1)

        conteudo_login = ctk.CTkFrame(frame_login, fg_color="transparent")
        conteudo_login.grid(row=1, column=0)
        conteudo_login.grid_columnconfigure(0, weight=1)

        # Logo do porquinho com "RICO"
        img_logo = ctk.CTkImage(Image.open(os.path.join(PATH_IMGS, "ricoIcon.png")), size=(130, 130))
        ctk.CTkLabel(conteudo_login, image=img_logo, text="").pack(pady=(40, 10))

        ctk.CTkLabel(conteudo_login, text="Acesse sua conta",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COR_CLARA).pack(pady=(10, 10))

        ctk.CTkEntry(conteudo_login, placeholder_text="Endereço de e-mail",
                     width=280, height=40, fg_color=COR_BRANCA, text_color="black").pack(pady=10)

        ctk.CTkEntry(conteudo_login, placeholder_text="Senha", show="*",
                     width=280, height=40, fg_color=COR_BRANCA, text_color="black").pack(pady=10)

        ctk.CTkLabel(conteudo_login, text="Esqueceu sua senha?",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color="#aaa").pack(pady=(5, 5))

        ctk.CTkButton(conteudo_login, text="Entrar", width=280, height=40, fg_color="#7a6ef5").pack(pady=(10, 10))

        ctk.CTkLabel(conteudo_login, text="Novo no app?",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_CLARA).pack()
        ctk.CTkLabel(conteudo_login, text="Cadastre-se",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_AMARELA).pack()

        # Frame Direito
        frame_info = ctk.CTkFrame(self, fg_color=COR_DIREITA)
        frame_info.grid(row=0, column=1, sticky="nsew")
        frame_info.grid_columnconfigure(0, weight=1)
        frame_info.grid_rowconfigure(0, weight=1)
        frame_info.grid_rowconfigure(1, weight=1)
        frame_info.grid_rowconfigure(2, weight=1)

        # Imagem decorativa superior esquerda
        img_top = ImageTk.PhotoImage(Image.open(os.path.join(PATH_IMGS, "carrossel.png")).resize((500, 500)))
        ctk.CTkLabel(frame_info, image=img_top, text="").place(x=0, y=0)

        # Personagem central
        img_personagem = ctk.CTkImage(Image.open(os.path.join(PATH_IMGS, "Pessoa_Login.png")), size=(380, 380))
        ctk.CTkLabel(frame_info, image=img_personagem, text="").grid(row=1, column=0)

        # Frame para os textos alinhados à esquerda com pequeno espaçamento
        texto_frame = ctk.CTkFrame(frame_info, fg_color="transparent")
        texto_frame.grid(row=2, column=0, sticky="w", padx=80)

        ctk.CTkLabel(texto_frame, text="Bem-vindo ao",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=COR_CLARA).pack(anchor="w")

        ctk.CTkLabel(texto_frame, text="Rico!",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=COR_AMARELA).pack(anchor="w", pady=(5, 5))

        ctk.CTkLabel(texto_frame, text="O lugar ideal\npara você aprender a investir!",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color=COR_CLARA,
                     justify="left").pack(anchor="w")

        # Imagem decorativa inferior direita
        img_bot = ImageTk.PhotoImage(Image.open(os.path.join(PATH_IMGS, "Group 13.png")).resize((300, 180)))
        ctk.CTkLabel(frame_info, image=img_bot, text="").place(relx=1.0, rely=1.0, anchor="se")
