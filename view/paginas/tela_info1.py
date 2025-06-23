import customtkinter as ctk
from PIL import Image
import os

# Cores
COR_NAV = "#3F2A87"
COR_TITULO = "#FFC11E"
COR_TEXTO = "#FFFFFF"
COR_FUNDO = "#1E1B2E"
COR_CAIXA_TEXTO = "#2C2154"

class TelaInfo1Frame(ctk.CTkFrame):
    def __init__(self, parent, voltar_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.voltar_callback = voltar_callback
        self.configure(fg_color=COR_FUNDO)

        # === Barra de navegação ===
        nav_bar = ctk.CTkFrame(self, height=60, fg_color=COR_NAV)
        nav_bar.pack(fill="x", side="top")

        img_path = os.path.join(os.path.dirname(__file__), "..", "images", "ricoIconVertical.png")
        if os.path.exists(img_path):
            pil_image = Image.open(img_path)
            pil_image = pil_image.resize((180, 40), Image.Resampling.LANCZOS)
            nav_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(160, 40))
            label_img = ctk.CTkLabel(nav_bar, image=nav_img, text="")
            label_img.pack(side="left", padx=10, pady=10)

        # Conteúdo fixo
        titulo = "Quando comprar e vender ações?"
        autor = "Maria Silva"
        data = "10/04/2024"
        texto = (
            "Descubra os principais sinais do mercado que indicam a hora certa de comprar e vender. "
            "Aprender a identificar os melhores momentos para operar pode maximizar seus lucros e reduzir perdas. "
            "Neste artigo, você conhecerá estratégias fundamentais de análise técnica e fundamentalista, "
            "além de dicas práticas para tomar decisões mais conscientes no mercado de ações."
        )

        # Título
        label_titulo = ctk.CTkLabel(
            self, text=titulo,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COR_TITULO
        )
        label_titulo.pack(anchor="w", padx=30, pady=(30, 5))

        # Autor e Data
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(anchor="w", padx=30, pady=(0, 15))

        ctk.CTkLabel(info_frame, text=f"Autor: {autor}", font=ctk.CTkFont(size=14), text_color=COR_TEXTO).pack(side="left", padx=(0, 20))
        ctk.CTkLabel(info_frame, text=f"Data: {data}", font=ctk.CTkFont(size=14), text_color=COR_TEXTO).pack(side="left")

        # Caixa de texto
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
        texto_box.insert("1.0", texto)
        texto_box.configure(state="disabled")
        texto_box.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão voltar (com redimensionamento dinâmico)
        arrow_path = os.path.join(os.path.dirname(__file__), "..", "images", "arrow.png")
        if os.path.exists(arrow_path):
            arrow_image = Image.open(arrow_path).transpose(Image.FLIP_LEFT_RIGHT)
            arrow_image = arrow_image.resize((40, 40), Image.Resampling.LANCZOS)
            self.ctk_arrow = ctk.CTkImage(light_image=arrow_image, dark_image=arrow_image)

            self.voltar_label = ctk.CTkLabel(self, image=self.ctk_arrow, text="", cursor="hand2")
            self.voltar_label.image = self.ctk_arrow
            self.voltar_label.place(x=20, y=self.winfo_height() - 10, anchor="sw")

            def on_resize(event):
                self.voltar_label.place(x=20, y=event.height - 10, anchor="sw")
            self.bind("<Configure>", on_resize)

            self.voltar_label.bind("<Button-1>", lambda e: self.voltar_para_dict())

    def voltar_para_dict(self):
        self.pack_forget()
        if self.voltar_callback:
            self.voltar_callback()
