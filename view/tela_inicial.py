import tkinter as tk
from tkinter import font as tkfont

# const das cores
COR_BG_PRINCIPAL = "#2b1b4a"
COR_NAVBAR = "#3f2b7b"
COR_HL = "#7c5cf4"
COR_TEXTO = "white"
COR_BOTAO_1 = "#e0dcf9"
COR_BOTAO_2 = "#7c5cf4"

# tlea principal
root = tk.Tk()
root.title("Tela inicial RICO")
root.state("zoomed")
root.configure(bg=COR_BG_PRINCIPAL)

# fonte custom
fonte_titulo = tkfont.Font(family="Roboto", size=40, weight="bold")
fonte_botao = tkfont.Font(family="Roboto", size=12, weight="bold")

# navbar
navbar = tk.Frame(root, bg=COR_NAVBAR, height=60)
navbar.pack(side="top", fill="x")

# botões da navbar
tk.Label(navbar, text="Sobre", bg=COR_NAVBAR, fg=COR_TEXTO, font=fonte_botao).pack(side="right", padx=60)
tk.Label(navbar, text="Login", bg=COR_NAVBAR, fg=COR_TEXTO, font=fonte_botao).pack(side="right", padx=60)

cadastro_btn = tk.Button(navbar, text="Cadastre-se", bg="white", fg=COR_NAVBAR, font=fonte_botao, relief="sunken", padx=60, pady=15)
cadastro_btn.pack(side="right", padx=10)

# conteudo principal
conteudo = tk.Frame(root, bg=COR_BG_PRINCIPAL)
conteudo.pack(expand=True)

texto = """Construa
seu império
começando do
completo zero"""
label_texto = tk.Label(conteudo, text=texto, bg=COR_BG_PRINCIPAL, fg=COR_TEXTO, font=fonte_titulo, justify="left")
label_texto.pack(anchor="w", padx=80, pady=20)

# botoes principais
botoes_frame = tk.Frame(conteudo, bg=COR_BG_PRINCIPAL)
botoes_frame.pack(anchor="w", padx=80, pady=10)

btn1 = tk.Button(botoes_frame, text="ENTRE AGORA", font=fonte_botao, bg=COR_BOTAO_1, fg=COR_NAVBAR, padx=20, pady=10)
btn1.pack(side="left", padx=10)

btn2 = tk.Button(botoes_frame, text="▶ VEJA O TRAILER", font=fonte_botao, bg=COR_BOTAO_2, fg="white", padx=20, pady=10)
btn2.pack(side="left", padx=10)

# botao de baixo
rodape = tk.Frame(root, bg=COR_HL, height=80)
rodape.pack(side="bottom", fill="x")

btn_mais = tk.Button(rodape, text="Ver Mais", font=fonte_botao, bg=COR_HL, fg="white", relief="groove", padx=15, pady=5)
btn_mais.pack(pady=20)

# sair do app
root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()
