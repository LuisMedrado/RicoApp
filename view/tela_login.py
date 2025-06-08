
import customtkinter as ctk
from pyglet import font as pfont


# consts cores
COR_FUNDO = "#2d234d"
COR_AZUL = "#7a6ef5"
COR_CLARA = "#e6e6f0"


class telaLoginFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller):
        super().__init__(parent_container, fg_color=COR_FUNDO)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame_login_inner = ctk.CTkFrame(self, fg_color="transparent", width=400, height=500)
        frame_login_inner.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        frame_login_inner.grid_columnconfigure(0, weight=1)

        label_titulo_login = ctk.CTkLabel(frame_login_inner, text="Acesse sua conta",
                                          font=ctk.CTkFont(family="Roboto-Bold", size=32, weight="bold"),
                                          text_color=COR_CLARA)
        label_titulo_login.pack(pady=(50,30), padx=20)

        # frame da esquerda
        self.frame_cadastro = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cadastro.grid(row=0, column=0, sticky="nsew")

        # frame da direita
        self.frame_info = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_info.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)





janela = ctk.CTk()
janela.title("Tela Login")

tela_login = telaLoginFrame(janela, None)
tela_login.pack(fill="both", expand=True)

janela.mainloop()