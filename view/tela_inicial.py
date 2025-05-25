import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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

# container geral
frame_main = ctk.CTkFrame(master=app, fg_color=cor_fundo)
frame_main.pack(fill="both", expand=True)

# header
header = ctk.CTkFrame(master=frame_main, height=60, fg_color=cor_header)
header.pack(fill="x", side="top")

frame_menu = ctk.CTkFrame(master=header, fg_color=cor_header)
frame_menu.pack(side="right", padx=20, pady=10)

btn_sobre = ctk.CTkButton(master=frame_menu, text="Sobre", fg_color="transparent", hover_color=cor_azul)
btn_login = ctk.CTkButton(master=frame_menu, text="Login", fg_color="transparent", hover_color=cor_azul)
btn_cadastro = ctk.CTkButton(master=frame_menu, text="Cadastre-se", fg_color="white", text_color="black")

btn_sobre.pack(side="left", padx=5)
btn_login.pack(side="left", padx=5)
btn_cadastro.pack(side="left", padx=5)

# faixa cor diferente
subheader = ctk.CTkFrame(master=frame_main, height=20, fg_color=cor_subheader)
subheader.pack(fill="x", side="top")

# conteudo principal
frame_conteudo = ctk.CTkFrame(master=frame_main, fg_color=cor_fundo)
frame_conteudo.pack(fill="both", expand=True, pady=30, padx=60)

titulo = ctk.CTkLabel(master=frame_conteudo,
                      text="Construa\nseu império\ncomeçando do\ncompleto zero",
                      font=ctk.CTkFont(size=40, weight="bold"),
                      justify="left")
titulo.pack(anchor="w", pady=20)

# botões de ação
frame_botoes = ctk.CTkFrame(master=frame_conteudo, fg_color=cor_fundo)
frame_botoes.pack(anchor="w", pady=20)

btn_entrar = ctk.CTkButton(master=frame_botoes, text="ENTRE AGORA", fg_color=cor_clara, text_color="black")
btn_trailer = ctk.CTkButton(master=frame_botoes, text="▶ VEJA O TRAILER", fg_color=cor_azul)

btn_entrar.pack(side="left", padx=10)
btn_trailer.pack(side="left", padx=10)

# footer
rodape = ctk.CTkFrame(master=frame_main, height=40, fg_color=cor_subheader)
rodape.pack(fill="x", side="bottom")

btn_ver_mais = ctk.CTkButton(master=rodape, text="Ver Mais", fg_color="white", text_color="black", height=28, width=100)
btn_ver_mais.pack(pady=5)

# func pra rodar o app
app.mainloop()