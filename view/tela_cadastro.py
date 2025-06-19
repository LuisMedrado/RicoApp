
from ctypes import c_ushort
import customtkinter as ctk
import tkinter as tk
from PIL.ImageChops import darker
from PIL import Image, ImageTk
from pyglet import image
from os import path
from model.login.usuarioModel import usuarioModel

COR_FUNDO_ESCURA = "#1E1B2E"
COR_FUNDO_CLARA = "#3F2A87"
COR_DESTAQUE = "#F4C326"

DIR_TELA = path.dirname(__file__)
PATH_IMGS = path.join(DIR_TELA, "images")


class TelaCadastro(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_cadastro = ctk.CTkFrame(self, fg_color=COR_FUNDO_ESCURA)
        self.frame_cadastro.grid(row=0, column=1, sticky='nsew')

        self.frame_explicativo = ctk.CTkFrame(self, fg_color=COR_FUNDO_CLARA)
        self.frame_explicativo.grid(row=0, column=0, sticky='nsew')

        self.criar_componentes_explicativos()
        self.criar_componentes_cadastro()



    def criar_componentes_explicativos(self):

        imagem_final = Image.open("images/imagem_cadastro.png")

        self.layout_completo_img = ctk.CTkImage(
            light_image=imagem_final,
            dark_image=imagem_final,
            size=(1036, 1080)
        )

        self.layout_completo_label = ctk.CTkLabel(
            self.frame_explicativo,
            image=self.layout_completo_img,
            text="",
            fg_color="transparent"
        )

        self.layout_completo_label.place(x=0, y=0)

        

    def criar_componentes_cadastro(self):

        self.frame_cadastro.grid_columnconfigure(0, weight=1)

        self.titulo_cadastro = ctk.CTkLabel(
            self.frame_cadastro,
            text="Cadastro"
        )



        self.titulo_cadastro.grid(row=0, column=0, sticky='nsew')



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro")
        self.geometry("1920x1080")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tela_cadastro = TelaCadastro(self)
        self.tela_cadastro.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    usuarioModel()

