from ctypes import c_ushort

import customtkinter as ctk
import tkinter as tk

from PIL.ImageChops import darker

from view.tela_inicial import COR_FUNDO

class telaCadastro(ctk.CTkFrame):
    def __init__(self, master, **kwarg):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)

        self.frame_cadastro = ctk.CTkFrame(self, width=400)
        self.frame_cadastro.grid(row=0, column=0, sticky='nsew')

        self.frame_explicativo = ctk.CTkFrame(self, width=400)
        self.frame_explicativo.grid(row=0, column=1, sticky='nsew')

        self.criar_componentes_cadastro()
        self.criar_compenentes_explicativos()

        def criar_componentes_cadastro(self):
            self.titulo_cadastro = ctk.CTkLabel(
                self.frame_cadastro,
                text = "Cadastro",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            self.titulo_cadastro.grid(row=0, column=0, padx=20, pady=10)

app = telaCadastro()
app.mainloop()
