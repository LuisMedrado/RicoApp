import customtkinter as ctk
import tkinter as tk
from pyglet import font as pfont
from os import path, listdir
from PIL import Image
import webbrowser

def abrirlink():
    link = "https://www.youtube.com/watch?v=BVNnRVOQ73Q"
    webbrowser.open_new_tab(link)

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
cor_header = "#3f2a87"
cor_subheader = "#7a6ef5"
cor_fundo = "#2d234d"
cor_clara = "#e6e6f0"
cor_azul = "#7a6ef5"

# fontes
roboto_padrao = ctk.CTkFont(family="Roboto")

# container geral
frame_main = ctk.CTkFrame(master=app, fg_color=cor_fundo)
frame_main.pack(fill="both", expand=True)

# header
header = ctk.CTkFrame(master=frame_main, height=60, fg_color=cor_header)
header.pack(fill="x", side="top")

frame_menu = ctk.CTkFrame(master=header, fg_color=cor_header)
frame_menu.pack(side="right", padx=20, pady=15)

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

frame_conteudo.grid_columnconfigure(0, weight=2)
frame_conteudo.grid_columnconfigure(1, weight=3)
frame_conteudo.grid_rowconfigure(0, weight=1)

frame_esquerda = ctk.CTkFrame(master=frame_conteudo, fg_color="transparent")
frame_esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

frame_esquerda_agrupador = ctk.CTkFrame(master=frame_esquerda, fg_color="transparent")
frame_esquerda.grid_rowconfigure(0, weight=1)
frame_esquerda.grid_rowconfigure(1, weight=0)
frame_esquerda.grid_rowconfigure(2, weight=1)
frame_esquerda.grid_columnconfigure(0, weight=1)
frame_esquerda_agrupador.grid(row=1, column=0, sticky="w")


titulo = ctk.CTkLabel(master=frame_esquerda_agrupador,
                      text="Construa\nseu império\ncomeçando do\ncompleto zero",
                      font=ctk.CTkFont(family="Roboto-Black", size=120, weight="bold"),
                      justify="left",
                      anchor="w")
titulo.pack(side="top", anchor="w", pady=(0, 30), padx=0)

frame_botoes = ctk.CTkFrame(master=frame_esquerda_agrupador, fg_color="transparent")
frame_botoes.pack(side="top", anchor="w", pady=(0, 0), padx=0)

btn_entrar = ctk.CTkButton(master=frame_botoes, width=250, height=75,
                           text="ENTRE AGORA",
                           fg_color=cor_clara, text_color="black",
                           font=ctk.CTkFont(family="Roboto-Bold", size=22, weight="bold")
                           )
btn_entrar.pack(side="left", padx=(0, 20))

btn_trailer = ctk.CTkButton(master=frame_botoes, width=250, height=75,
                            text="▶ VEJA O TRAILER",
                            fg_color=cor_azul,
                            font=ctk.CTkFont(family="Roboto-Bold", size=22, weight="bold"),
                            command=abrirlink
                            )
btn_trailer.pack(side="left", padx=0)

frame_direita = ctk.CTkFrame(master=frame_conteudo, fg_color="transparent")
frame_direita.grid(row=0, column=1, sticky="nsew", padx=(0, 0))

nome_arquivo_imagem = "porquinhoDinheiro.png"
path_imagem_porquinho = path.join(path_imgs, nome_arquivo_imagem)

try:
    pil_original_image = Image.open(path_imagem_porquinho)

    img_altura_desejada = 800
    
    original_width, original_height = pil_original_image.size
    aspect_ratio = original_width / float(original_height)
    img_larg_calc = int(img_altura_desejada * aspect_ratio)

    pil_resized_image = pil_original_image.resize((img_larg_calc, img_altura_desejada), Image.Resampling.LANCZOS)
    
    ctk_porquinho_image = ctk.CTkImage(light_image=pil_resized_image,
                                       dark_image=pil_resized_image,
                                       size=(img_larg_calc, img_altura_desejada)
                                       )
    
    label_imagem_porquinho = ctk.CTkLabel(master=frame_direita, image=ctk_porquinho_image, text="")
    label_imagem_porquinho.pack(anchor="center", expand=True, padx=20, pady=20)

except FileNotFoundError:
    print(f"ERRO Imagem '{path_imagem_porquinho}' não encontrada.")
    label_erro_imagem = ctk.CTkLabel(master=frame_direita, text=f"Imagem não encontrada:\n{nome_arquivo_imagem}",
                                     font=ctk.CTkFont(family="Roboto-Regular", size=16)
                                     )
    label_erro_imagem.pack(anchor="center", expand=True)
except Exception as e:
    print(f"Erro ao carregar imagem: {e}")
    label_erro_imagem = ctk.CTkLabel(master=frame_direita, text="Erro ao carregar imagem.",
                                     font=ctk.CTkFont(family="Roboto-Regular", size=16)
                                     )
    label_erro_imagem.pack(anchor="center", expand=True)

# footer

rodape = ctk.CTkFrame(master=frame_main, height=100, fg_color=cor_subheader)
rodape.pack(fill="x", side="bottom")

 ############ AVALIAR NECESSIDADE DESSE BOTAO AQUI

# btn_ver_mais = ctk.CTkButton(master=rodape, text="Ver mais", fg_color="transparent",
#                              border_color="white", border_width=2, text_color="white",
#                              height=150, width=150, font=ctk.CTkFont(family="Roboto-Bold", weight="bold", size=22))
# btn_ver_mais.pack(pady=10)

# func pra rodar o app
app.mainloop()