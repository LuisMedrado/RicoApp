import customtkinter as ctk
from PIL import Image
from pathlib import Path

COR_FUNDO_ESCURA = "#1E1B2E"
COR_FUNDO_CLARA = "#3F2A87"
COR_DESTAQUE = "#F4C326"


CAMINHO_IMAGENS = Path(__file__).parent / "images"


class telaLoginFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller, **kwargs):
        super().__init__(parent_container, **kwargs)

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
        caminho_logo = CAMINHO_IMAGENS / "ricoIcon.png"
        self.logo_imagem = ctk.CTkImage(
            light_image=Image.open(caminho_logo),
            dark_image=Image.open(caminho_logo),
            size=(258, 258)
        )

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

        self.button_login = ctk.CTkButton(
            self.frame_cadastro,
            fg_color="#3F2A87",
            text="Entrar",
            width=114,
            height=46
        )
        self.button_login.grid(row=6, column=0, pady=10)

        self.new_user_button = ctk.CTkButton(
            self.frame_cadastro,
            fg_color="transparent",
            text="Novo usuário? Cadastre-se!",
            font=ctk.CTkFont(underline=True)
        )
        self.new_user_button.grid(row=7, column=0, pady=10)

    def criar_componentes_explicativos(self):
        # NOVO: Use o caminho absoluto para carregar a imagem
        imagem_final = Image.open(CAMINHO_IMAGENS / "teste4.png")

        self.layout_completo_img = ctk.CTkImage(
            light_image=imagem_final,
            dark_image=imagem_final,
            size=(920, 1080)
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