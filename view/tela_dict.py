import customtkinter as ctk
from os import path
from os import path
from PIL import Image
from view.utils import carregar_fontes_globais
from controller import dict_control as dc

DIR_TELA = path.dirname(__file__)
PATH_IMGS = path.join(DIR_TELA, "images")

COR_HEADER = "#3f2a87"
COR_SUBHEADER = "#7a6ef5"
COR_FUNDO = "#2d234d"
COR_TEXTO = "#E6E6F0"
COR_PESQUISA = "#E6E6F0"

carregar_fontes_globais()


def carregar_img(parent_frame, nome_img, tamanho, ancoragem):
    nome_arquivo_imagem = nome_img
    path_img = path.join(PATH_IMGS, nome_arquivo_imagem)
    try:
        pil_original_image = Image.open(path_img)
        max_altura = tamanho
        original_width, original_height = pil_original_image.size
        aspect_ratio = original_width / float(original_height)
    nome_arquivo_imagem = nome_img
    path_img = path.join(PATH_IMGS, nome_arquivo_imagem)
    try:
        pil_original_image = Image.open(path_img)
        max_altura = tamanho
        original_width, original_height = pil_original_image.size
        aspect_ratio = original_width / float(original_height)

        img_altura_calc = max_altura
        img_larg_calc = int(img_altura_calc * aspect_ratio)
        img_altura_calc = max_altura
        img_larg_calc = int(img_altura_calc * aspect_ratio)

        pil_resized_image = pil_original_image.resize((img_larg_calc, img_altura_calc), Image.Resampling.LANCZOS)
        pil_resized_image = pil_original_image.resize((img_larg_calc, img_altura_calc), Image.Resampling.LANCZOS)

        ctk_porquinho_image = ctk.CTkImage(light_image=pil_resized_image,
                                           dark_image=pil_resized_image,
                                           size=(img_larg_calc, img_altura_calc))
        ctk_porquinho_image = ctk.CTkImage(light_image=pil_resized_image,
                                           dark_image=pil_resized_image,
                                           size=(img_larg_calc, img_altura_calc))

        label_img = ctk.CTkLabel(parent_frame, image=ctk_porquinho_image, text="")
        label_img.pack(anchor=ancoragem, pady=(5, 15))
    except FileNotFoundError:
        print(f"ERRO imagem '{path_img}' não encontrada.")
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        label_img = ctk.CTkLabel(parent_frame, image=ctk_porquinho_image, text="")
        label_img.pack(anchor=ancoragem, pady=(5, 15))
    except FileNotFoundError:
        print(f"ERRO imagem '{path_img}' não encontrada.")
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")


class telaDictFrame(ctk.CTkFrame):
    def __init__(self, parent_container, controller, **kwargs):
        super().__init__(parent_container, **kwargs)
        self.controller = controller
        self.configure(fg_color=COR_FUNDO)

        self.janela_aberta = None

        saida_artigos = dc.carregar_artigos()

        if saida_artigos == True:
            print("Erro ao retornar artigos do banco.")
            return

        articles_list = saida_artigos

        header = ctk.CTkFrame(self, height=50, fg_color=COR_HEADER, corner_radius=0)
        header.pack(fill="x", side="top", pady=(0, 20))

        self.menu_icon = ctk.CTkLabel(
            header,
            text="☰",
            font=(ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"), 22),
            cursor="hand2"
        )
        self.menu_icon.pack(side="left", padx=(25, 0), pady=15)
        self.menu_icon.bind("<Button-1>", self.toggle_sidebar)
        carregar_img(header, "ricoIconVertical.png", 60, "w")

        # search_frame = ctk.CTkFrame(self, fg_color="transparent")
        # search_frame.pack(pady=0, padx=20, fill="x")

        # search_entry = ctk.CTkEntry(
        #     search_frame,
        #     placeholder_text="Como ficar rico com 5 reais...",
        #     fg_color=COR_PESQUISA,
        #     border_width=0,
        #     height=40,
        #     font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
        # )
        # search_entry.pack(expand=True, fill="x")

        articles_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        articles_container.pack(pady=20, padx=20, fill="both", expand=True)

        for artigo in articles_list:
            artigo_id = artigo[0]
            artigo_titulo = artigo[1]

            # Frame do artigo
            article_frame = ctk.CTkFrame(
                articles_container,
                fg_color=COR_HEADER,
                height=120,
                corner_radius=10,
                cursor="hand2"
                cursor="hand2"
            )
            article_frame.pack(fill="x", pady=6)

            # Clique no frame
            article_frame.bind("<Button-1>", self.create_click_handler(artigo_id))

            # Título do artigo
            label = ctk.CTkLabel(
                article_frame,
                text=artigo_titulo,
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=80,
                pady=120
            )
            label.pack(side="left", fill="x", expand=False)
            label.bind("<Button-1>", self.create_click_handler(artigo_id))

            # Setinha
            setinha_label = ctk.CTkLabel(
                article_frame,
                text=">",
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=20
            )
            setinha_label.pack(side="right")
            setinha_label.bind("<Button-1>", self.create_click_handler(artigo_id))

    def create_click_handler(self, artigo_id):
        def handler(event):
            from view.tela_info import TelaInfoFrame

            if self.janela_aberta is None or not self.janela_aberta.winfo_exists():
                self.janela_aberta = ctk.CTkToplevel()
                self.janela_aberta.geometry("1200x800")
                self.janela_aberta.title("Detalhes do Artigo")

                tela_info = TelaInfoFrame(self.janela_aberta, id_artigo=artigo_id)
                tela_info.pack(fill="both", expand=True)

                self.after(100, lambda: [self.janela_aberta.lift(), self.janela_aberta.focus_force()])
            else:
                self.janela_aberta.lift()
                self.janela_aberta.focus_force()

        return handler


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("1200x800")

    tela = telaDictFrame(app, controller=None)
    tela.pack(fill="both", expand=True)

    app.mainloop()
