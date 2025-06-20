
import customtkinter as ctk
from PIL import Image
from os import path
import controller.usuario_control as user

COR_FUNDO_ESCURA = "#1E1B2E"
COR_FUNDO_CLARA = "#3F2A87"
COR_DESTAQUE = "#F4C326"

DIR_TELA = path.dirname(__file__)
PATH_IMGS = path.join(DIR_TELA, "images")


class TelaCadastro(ctk.CTkFrame):
    def __init__(self, parent_container, controller, **kwargs):
        super().__init__(parent_container, **kwargs)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Frames ---
        self.frame_explicativo = ctk.CTkFrame(self, fg_color=COR_FUNDO_CLARA, corner_radius=0)
        self.frame_explicativo.grid(row=0, column=0, sticky='nsew')

        self.frame_cadastro = ctk.CTkFrame(self, fg_color=COR_FUNDO_ESCURA, corner_radius=0)
        self.frame_cadastro.grid(row=0, column=1, sticky='nsew')

        self.criar_componentes_explicativos()
        self.criar_componentes_cadastro()

    def criar_componentes_explicativos(self):
        imagem_final = Image.open(path.join(PATH_IMGS, "imagem_cadastro.png"))

        largura_tela = (self.winfo_screenwidth() / 1.7)
        altura_tela = (self.winfo_screenheight() * 1.1)

        largura_img = int(largura_tela * 0.8)
        altura_img = int(altura_tela * 0.9)
        imagem_final = Image.open(path.join(PATH_IMGS, "imagem_cadastro.png"))


        self.layout_completo_img = ctk.CTkImage(
            light_image=imagem_final,
            dark_image=imagem_final,
            size=(largura_img, altura_img)
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
        self.frame_cadastro.grid_rowconfigure(0, weight=0)
        self.frame_cadastro.grid_rowconfigure(5, weight=1)

        self.titulo_cadastro = ctk.CTkLabel(
            self.frame_cadastro,
            text="Cadastro",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.titulo_cadastro.grid(row=0, column=0, pady=(80, 40), padx=30, sticky='n')

        self.input_nome = ctk.CTkEntry(
            self.frame_cadastro,
            fg_color="#E6E6F0",
            placeholder_text="Nome",
            width=400,
            height=54,
            corner_radius=25,
            text_color=COR_FUNDO_ESCURA,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_nome.grid(row=1, column=0, pady=10)

        self.input_email = ctk.CTkEntry(
            self.frame_cadastro,
            fg_color="#E6E6F0",
            placeholder_text="Endereço de email",
            corner_radius=25,
            width=400,
            height=54,
            text_color=COR_FUNDO_ESCURA,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_email.grid(row=2, column=0, pady=10)

        self.input_senha = ctk.CTkEntry(
            self.frame_cadastro,
            fg_color="#E6E6F0",
            placeholder_text="Sua senha",
            corner_radius=25,
            width=400,
            height=54,
            text_color=COR_FUNDO_ESCURA,
            show="*",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_senha.grid(row=3, column=0, pady=10)

        self.input_confirma_senha = ctk.CTkEntry(
            self.frame_cadastro,
            placeholder_text="Confirme sua senha",
            fg_color="#E6E6F0",
            width=400,
            height=54,
            corner_radius=25,
            text_color=COR_FUNDO_ESCURA,
            show="*",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.input_confirma_senha.grid(row=4, column=0, pady=10)

        def cadastrar():
            from view.tela_dict import telaDictFrame

            nome = self.input_nome.get()
            email = self.input_email.get()
            senha = self.input_senha.get()
            senhaConf = self.input_confirma_senha.get()

            verif = user.insert_cadastro(nome, email, senha)

            if senha == senhaConf and verif == True:
                self.controller.mostrar_frame(telaDictFrame)
            elif senha != senha and verif == True:
                mostrar_popup_erro("Senha e confirmação de senha não condizem!")
            else:
                mostrar_popup_erro(verif)


        def mostrar_popup_erro(mensagem):
            popup = ctk.CTkToplevel()
            popup.title("Erro de cadastro")
            popup.geometry("300x150")
            popup.resizable(False, False)

            label_mensagem = ctk.CTkLabel(popup, text=mensagem, font=ctk.CTkFont(size=14))
            label_mensagem.pack(pady=20)

            btn_fechar = ctk.CTkButton(popup, text="Fechar", command=popup.destroy)
            btn_fechar.pack(pady=10)

            # centralizar o popup
            popup.grab_set()
            popup.focus_force()

        self.button_cadastrar = ctk.CTkButton(
            self.frame_cadastro,
            text="CADASTRAR",
            fg_color=COR_FUNDO_CLARA,
            hover_color=COR_DESTAQUE,
            width=150,
            height=46,
            corner_radius=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=cadastrar
        )
        self.button_cadastrar.grid(row=6, column=0, pady=(20, 80), sticky='s')

        


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cadastro de Usuário")

        try:
            self.state('zoomed')
        except ctk.TclError:
            self.attributes('-fullscreen', True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # CORREÇÃO 1: Usando a classe correta, TelaCadastro
        self.tela_cadastro = TelaCadastro(self, controller=self)
        self.tela_cadastro.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
