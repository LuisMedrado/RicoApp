from ctypes import c_ushort
import customtkinter as ctk
import tkinter as tk
from PIL.ImageChops import darker
from PIL import Image, ImageTk
from pyglet import image

COR_FUNDO_ESCURA = "#2d234d"
COR_FUNDO_CLARA = "#786AAB"

class TelaCadastro(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_cadastro = ctk.CTkFrame(self, width=400, fg_color=COR_FUNDO_ESCURA)
        self.frame_cadastro.grid(row=0, column=0, sticky='nsew')

        self.frame_explicativo = ctk.CTkFrame(self, width=400, fg_color=COR_FUNDO_CLARA)
        self.frame_explicativo.grid(row=0, column=1, sticky='nsew')

        self.criar_componentes_cadastro()
        self.criar_componentes_explicativos()


    def criar_componentes_cadastro(self):

        self.frame_cadastro.grid_columnconfigure(0, weight=1)


        self.logo_imagem = ctk.CTkImage(
            light_image=Image.open("images/ricoIcon.png"),
            dark_image = Image.open("images/ricoIcon.png"),
            size=(258,258)
        )

        self.logo_label = ctk.CTkLabel(
            self.frame_cadastro,
            image= self.logo_imagem,
            text= ""
        )
        self.logo_label.grid(row=1, column=0, pady=(60,0))

        self.titulo_explicativo = ctk.CTkLabel(
            self.frame_cadastro,
            text="Acesse sua conta",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.titulo_explicativo.grid(row=2, column=0)

        self.input_email = ctk.CTkEntry(
            self.frame_cadastro,
            fg_color="#E6E6F0",
            placeholder_text="Endereço de email",
            corner_radius=25,
            width=284,
            height=54,
            text_color=COR_FUNDO_ESCURA,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_email.grid(row=3, column=0, pady=10)

        self.input_senha = ctk.CTkEntry(
            self.frame_cadastro,
            fg_color="#E6E6F0",
            placeholder_text="Sua senha",
            corner_radius=25,
            width=284,
            height=54,
            text_color=COR_FUNDO_ESCURA,
            show="*",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_senha.grid(row=4, column=0, pady=10)

    def criar_componentes_explicativos(self):
        self.titulo_explicativo = ctk.CTkLabel(
            self.frame_explicativo,
            text="Como Funciona",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.titulo_explicativo.grid(row=0, column=0, padx=20, pady=10)


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
    app = App()  # Cria uma instância da sua classe App
    app.mainloop() # Inicia o loop principal da interface