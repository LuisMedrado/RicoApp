import customtkinter as ctk
from PIL import Image
from os import path
import controller.usuario_control as user

COR_FUNDO_ESCURA = "#1E1B2E"
COR_FUNDO_CLARA = "#3F2A87"
COR_DESTAQUE = "#F4C326"

DIR_TELA = path.dirname(__file__)
PATH_IMGS = path.join(DIR_TELA, "images")

class telaLoginFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller, **kwargs):
        super().__init__(parent_container, **kwargs)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_cadastro = ctk.CTkFrame(self, fg_color=COR_FUNDO_ESCURA)
        self.frame_cadastro.grid(row=0, column=0, sticky='nsew')

        self.frame_explicativo = ctk.CTkFrame(self, fg_color=COR_FUNDO_CLARA)
        self.frame_explicativo.grid(row=0, column=1, sticky='nsew')

        self.criar_componentes_cadastro()
        self.criar_componentes_explicativos()

    def criar_componentes_cadastro(self):
        self.frame_cadastro.grid_columnconfigure(0, weight=1)

        # NOVO: Use o caminho absoluto para carregar as imagens
        caminho_logo = Image.open(path.join(PATH_IMGS, "ricoIcon.png"))
        self.logo_imagem = ctk.CTkImage(
            light_image=caminho_logo,
            dark_image=caminho_logo,
            size=(258, 258)
        )
        
        # BOTÃO DE VOLTAR (IMPORTAÇÃO INTERNA)
        self.botao_voltar = ctk.CTkButton(
            self.frame_cadastro,
            text="← Voltar",
            fg_color="transparent",
            hover_color="#cccccc",
            text_color=COR_DESTAQUE,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.controller.mostrar_frame(
                __import__('view.tela_inicial', fromlist=['telaInicialFrame']).telaInicialFrame
            )
        )
        self.botao_voltar.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 0))

        self.logo_label = ctk.CTkLabel(
            self.frame_cadastro,
            image=self.logo_imagem,
            text=""
        )
        self.logo_label.grid(row=1, column=0, pady=(60, 0))

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

        self.forget_password = ctk.CTkButton(
            self.frame_cadastro,
            fg_color="transparent",
            text="Esqueceu sua senha?",
            font=ctk.CTkFont(underline=True)
        )
        self.forget_password.grid(row=5, column=0, pady=(10, 254))

        def pegar_valores_login():
            from view.tela_dict import telaDictFrame

            email = self.input_email.get()
            senha = self.input_senha.get()

            verif = user.select_login(email, senha)

            if verif == True:
                self.controller.mostrar_frame(telaDictFrame)
            else:
                mostrar_popup_erro("Email ou senha incorretos.")

        self.button_login = ctk.CTkButton(
            self.frame_cadastro,
            fg_color="#3F2A87",
            text="Entrar",
            width=114,
            height=46,
            command=pegar_valores_login
        )
        self.button_login.grid(row=5, column=0, pady=10)
            
        self.new_user_button = ctk.CTkButton(
            self.frame_cadastro,
            fg_color="transparent",
            text="Novo usuário? Cadastre-se!",
            font=ctk.CTkFont(underline=True)
        )
        self.new_user_button.grid(row=7, column=0, pady=10)

        def mostrar_popup_erro(mensagem):
            popup = ctk.CTkToplevel()
            popup.title("Erro de Login")
            popup.geometry("300x150")
            popup.resizable(False, False)

            label_mensagem = ctk.CTkLabel(popup, text=mensagem, font=ctk.CTkFont(size=14))
            label_mensagem.pack(pady=20)

            btn_fechar = ctk.CTkButton(popup, text="Fechar", command=popup.destroy)
            btn_fechar.pack(pady=10)

            # centralizar o popup
            popup.grab_set()
            popup.focus_force()

    def criar_componentes_explicativos(self):
        imagem_final = Image.open(path.join(PATH_IMGS, "teste4.png"))

        # get da largura e altura da tela, ajustadas para caber no espaço disponível pra imagem
        largura_tela = (self.winfo_screenwidth() / 1.7)
        altura_tela = (self.winfo_screenheight() * 1.1)

        # ajuste de tamanho da imagem
        largura_img = int(largura_tela * 0.8)
        altura_img = int(altura_tela * 0.9)

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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")

        # Corrigido para funcionar em diferentes sistemas operacionais
        try:
            self.state('zoomed')
        except ctk.TclError:  # Em alguns sistemas (Linux/macOS) 'zoomed' pode não funcionar
            self.attributes('-fullscreen', True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tela_cadastro = telaLoginFrame(self, controller=self)  # Passando 'self' como controller
        self.tela_cadastro.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()