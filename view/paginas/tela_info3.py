import customtkinter as ctk
from PIL import Image
import os

# Cores fixas
COR_NAV = "#3F2A87"
COR_TITULO = "#FFC11E"
COR_TEXTO = "#FFFFFF"
COR_FUNDO = "#1E1B2E"
COR_CAIXA_TEXTO = "#2C2154"

class TelaInfo3(ctk.CTkFrame):
    def __init__(self, parent, voltar_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color=COR_FUNDO)
        self.voltar_callback = voltar_callback

        # === Barra superior ===
        nav_bar = ctk.CTkFrame(self, height=60, fg_color=COR_NAV)
        nav_bar.pack(fill="x", side="top")

        img_path = os.path.join(os.path.dirname(__file__), "ricoIconVertical.png")
        if os.path.exists(img_path):
            pil_image = Image.open(img_path)
            pil_image = pil_image.resize((180, 40), Image.Resampling.LANCZOS)
            nav_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(160, 40))
            label_img = ctk.CTkLabel(nav_bar, image=nav_img, text="")
            label_img.pack(side="left", padx=10, pady=10)
        else:
            print("Imagem 'ricoIconVertical.png' não encontrada.")

        # === Título ===
        label_titulo = ctk.CTkLabel(
            self,
            text="Como funciona a bolsa de valores?",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COR_TITULO
        )
        label_titulo.pack(anchor="w", padx=30, pady=(30, 5))

        # === Autor e Data ===
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(anchor="w", padx=30, pady=(0, 15))

        autor_label = ctk.CTkLabel(
            info_frame, text="Autor: Equipe Rico Educação",
            font=ctk.CTkFont(size=14),
            text_color=COR_TEXTO
        )
        data_label = ctk.CTkLabel(
            info_frame, text="Data: Abril de 2024",
            font=ctk.CTkFont(size=14),
            text_color=COR_TEXTO
        )
        autor_label.pack(side="left", padx=(0, 20))
        data_label.pack(side="left")

        # === Texto principal ===
        caixa_fundo = ctk.CTkFrame(self, fg_color=COR_CAIXA_TEXTO, corner_radius=12)
        caixa_fundo.pack(fill="both", expand=True, padx=30, pady=(0, 60))

        texto_box = ctk.CTkTextbox(
            caixa_fundo,
            font=ctk.CTkFont(size=16),
            text_color=COR_TEXTO,
            fg_color=COR_CAIXA_TEXTO,
            wrap="word",
            activate_scrollbars=True
        )

        texto = (
            "A bolsa de valores é o ambiente onde ocorrem as negociações de ações e outros ativos financeiros. "
            "No Brasil, a principal bolsa é a B3 (Brasil, Bolsa, Balcão).\n\n"
            "Empresas de capital aberto disponibilizam suas ações ao público por meio da bolsa, permitindo que investidores "
            "comprem pequenas partes desses negócios. Quando você compra uma ação, se torna sócio da empresa.\n\n"
            "A oscilação nos preços das ações acontece por diversos fatores: balanços da empresa, notícias, economia global, "
            "política e, principalmente, a relação entre oferta e demanda.\n\n"
            "A bolsa funciona de forma eletrônica e segura, com intermediação de corretoras. Com o avanço da tecnologia, "
            "qualquer pessoa com acesso à internet pode investir com poucos cliques."
        )

        texto_box.insert("1.0", texto)
        texto_box.configure(state="disabled")
        texto_box.pack(fill="both", expand=True, padx=20, pady=20)

        # === Botão voltar ===
        tamanho_seta = 40
        margem_inferior = 10
        margem_esquerda = 20

        arrow_path = os.path.join("view", "images", "arrow.png")
        if os.path.exists(arrow_path):
            arrow_image = Image.open(arrow_path)
            arrow_image = arrow_image.transpose(Image.FLIP_LEFT_RIGHT)
            arrow_image = arrow_image.resize((tamanho_seta, tamanho_seta), Image.Resampling.LANCZOS)
            self.ctk_arrow = ctk.CTkImage(light_image=arrow_image, dark_image=arrow_image)

            self.voltar_label = ctk.CTkLabel(self, image=self.ctk_arrow, text="", cursor="hand2")
            self.voltar_label.image = self.ctk_arrow
            self.voltar_label.place(x=margem_esquerda, y=self.winfo_height() - margem_inferior, anchor="sw")

            def on_resize(event):
                self.voltar_label.place(x=margem_esquerda, y=event.height - margem_inferior, anchor="sw")
            self.bind("<Configure>", on_resize)

            self.voltar_label.bind("<Button-1>", lambda e: self.voltar_callback() if self.voltar_callback else None)
        else:
            print("Imagem 'arrow.png' não encontrada.")

# Teste local
if __name__ == "__main__":
    def voltar():
        print("Voltar clicado (simulação).")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.geometry("700x500")
    root.title("Tela Info 3")
    tela = TelaInfo3(root, voltar_callback=voltar)
    tela.pack(fill="both", expand=True)
    root.mainloop()
