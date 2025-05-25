import customtkinter as ctk
import tkinter as tk
from pyglet import font as pfont
from os import path, listdir
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# diretorios
dir_tela = path.dirname(__file__)
path_fonts = path.join(dir_tela, "fonts")
path_imgs = path.join(dir_tela, "images")

# carregar fontes da pasta fonts
try:
    for nome_arq in listdir(path_fonts):
        if nome_arq.lower().endswith(".ttf"):
            nome_fonte = path.join(path_fonts, nome_arq)
            pfont.add_file(nome_fonte)
except Exception as e:
    print(f"Erro ao carregar fonte: {e}")

# start da tela principal
app = ctk.CTk()
app.title("Tela Inicial")
app.after(1, app.state, "zoomed")

# consts cores
cor_header = "#3c2e83"
cor_subheader = "#6c4eea"
cor_fundo = "#2b1b4a"
cor_clara = "#dad8f8"
cor_azul = "#7c65f2"

# fontes
roboto_padrao = ctk.CTkFont(family="Roboto")

# container geral
frame_main = ctk.CTkFrame(master=app, fg_color=cor_fundo)
frame_main.pack(fill="both", expand=True)

# header
header = ctk.CTkFrame(master=frame_main, height=60, fg_color=cor_header)
header.pack(fill="x", side="top")

frame_menu = ctk.CTkFrame(master=header, fg_color=cor_header)
frame_menu.pack(side="right", padx=20, pady=10)

btn_sobre = ctk.CTkButton(master=frame_menu, text="Sobre", fg_color="transparent", hover_color=cor_azul,
                          font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
                          )
btn_login = ctk.CTkButton(master=frame_menu, text="Login", fg_color="transparent", border_color="white",
                          border_width=2, hover_color=cor_azul,
                          font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
                          )
btn_cadastro = ctk.CTkButton(master=frame_menu, text="Cadastre-se", fg_color="white", text_color="black",
                             font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
                             )

btn_sobre.pack(side="left", padx=5)
btn_login.pack(side="left", padx=5)
btn_cadastro.pack(side="left", padx=5)

# faixa cor diferente
subheader = ctk.CTkFrame(master=frame_main, height=50, fg_color=cor_subheader)
subheader.pack(fill="x", side="top")

# conteudo principal
frame_conteudo = ctk.CTkFrame(master=frame_main, fg_color=cor_fundo)
frame_conteudo.pack(fill="both", expand=True, pady=10, padx=60)

titulo = ctk.CTkLabel(master=frame_conteudo,
                      text="Construa\nseu império\ncomeçando do\ncompleto zero",
                      font=ctk.CTkFont(family="Roboto-Black", size=120, weight="bold"),
                      justify="left")
titulo.pack(anchor="w", pady=20)

# botões de ação
frame_botoes = ctk.CTkFrame(master=frame_conteudo, fg_color=cor_fundo)
frame_botoes.pack(anchor="w", pady=100)

btn_entrar = ctk.CTkButton(master=frame_botoes, width=250, height=75,
                           text="ENTRE AGORA",
                           fg_color=cor_clara, text_color="black",
                           font=ctk.CTkFont(family="Roboto-Bold", size=22, weight="bold")
                           )

btn_trailer = ctk.CTkButton(master=frame_botoes, width=250, height=75,
                            text="▶ VEJA O TRAILER",
                            fg_color=cor_azul,
                            font=ctk.CTkFont(family="Roboto-Bold", size=22, weight="bold")
                            )

btn_entrar.pack(side="left", padx=60)
btn_trailer.pack(side="left", padx=75)

# footer

rodape = ctk.CTkFrame(master=frame_main, height=300, fg_color=cor_subheader)
rodape.pack(fill="x", side="bottom")

 ############ AVALIAR NECESSIDADE DESSE BOTAO AQUI

# btn_ver_mais = ctk.CTkButton(master=rodape, text="Ver mais", fg_color="transparent",
#                              border_color="white", border_width=2, text_color="white",
#                              height=150, width=150, font=ctk.CTkFont(family="Roboto-Bold", weight="bold", size=22))
# btn_ver_mais.pack(pady=10)

# func pra rodar o app
app.mainloop()