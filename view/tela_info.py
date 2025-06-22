import customtkinter as ctk
from PIL import Image
import os
from utils import get_info_topico

# Cores para o design
COR_NAV = "#3F2A87"
COR_TITULO = "#FFC11E"
COR_TEXTO = "#FFFFFF"
COR_FUNDO = "#1E1B2E"
COR_CAIXA_TEXTO = "#2C2154"  # tom mais escuro do roxo

class TelaInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, topico, **kwargs):
        super().__init__(parent, **kwargs)
        self.topico = topico
        self.configure(fg_color=COR_FUNDO)

        # === Barra de navegação superior ===
        nav_bar = ctk.CTkFrame(self, height=60, fg_color=COR_NAV)
        nav_bar.pack(fill="x", side="top")

        img_path = os.path.join("view", "images", "ricoIconVertical.png")
        if os.path.exists(img_path):
            pil_image = Image.open(img_path)
            pil_image = pil_image.resize((180, 40), Image.Resampling.LANCZOS)
            nav_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(160, 40))

            label_img = ctk.CTkLabel(nav_bar, image=nav_img, text="")
            label_img.pack(side="left", padx=10, pady=10)
        else:
            print("Imagem 'ricoIconVertical.png' não encontrada.")

        # === Dados do tópico ===
        dados = get_info_topico(topico)
        titulo = dados.get("titulo", "Sem título")
        autor = dados.get("autor", "Desconhecido")
        data = dados.get("data", "Data não informada")
        texto = dados.get("descricao", "Sem descrição disponível.")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self, text=titulo,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COR_TITULO
        )
        self.label_titulo.pack(anchor="w", padx=30, pady=(30, 5))

        # Autor e Data (alinhados ao conteúdo)
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(anchor="w", padx=30, pady=(0, 15))

        autor_label = ctk.CTkLabel(
            info_frame, text=f"Autor: {autor}",
            font=ctk.CTkFont(size=14),
            text_color=COR_TEXTO
        )
        data_label = ctk.CTkLabel(
            info_frame, text=f"Data: {data}",
            font=ctk.CTkFont(size=14),
            text_color=COR_TEXTO
        )

        autor_label.pack(side="left", padx=(0, 20))
        data_label.pack(side="left")

        # Caixa de fundo para o texto
        caixa_fundo = ctk.CTkFrame(
            self, fg_color=COR_CAIXA_TEXTO,
            corner_radius=12
        )
        caixa_fundo.pack(fill="both", expand=True, padx=30, pady=(0, 60))

        # Texto principal
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

        # --- Botão de voltar ---
        tamanho_seta = 40
        margem_inferior = 10
        margem_esquerda = 20

        arrow_path = os.path.join("view", "images", "arrow.png")
        if os.path.exists(arrow_path):
            arrow_image = Image.open(arrow_path)
            arrow_image = arrow_image.transpose(Image.FLIP_LEFT_RIGHT)  # espelhar
            arrow_image = arrow_image.resize((tamanho_seta, tamanho_seta), Image.Resampling.LANCZOS)
            self.ctk_arrow = ctk.CTkImage(light_image=arrow_image, dark_image=arrow_image)

            self.voltar_label = ctk.CTkLabel(
                self, image=self.ctk_arrow, text="", cursor="hand2"
            )
            self.voltar_label.image = self.ctk_arrow
            self.voltar_label.place(x=margem_esquerda, y=self.winfo_height() - margem_inferior, anchor="sw")

            def on_resize(event):
                self.voltar_label.place(x=margem_esquerda, y=event.height - margem_inferior, anchor="sw")
            self.bind("<Configure>", on_resize)

            self.voltar_label.bind("<Button-1>", lambda e: parent.destroy())
        else:
            print("Imagem 'arrow.png' não encontrada.")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.geometry("700x500")
    root.title("Tela de Informação Teste")

    topico_teste = "guardar_investir"
    tela_info = TelaInfoFrame(root, topico=topico_teste)
    tela_info.pack(fill="both", expand=True)

    root.mainloop()
