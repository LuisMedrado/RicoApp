import customtkinter as ctk
from os import path
from PIL import Image

# Import das telas info
from view.paginas.tela_info1 import TelaInfo1Frame
from view.paginas.tela_info2 import TelaInfo2
from view.paginas.tela_info3 import TelaInfo3
from view.paginas.tela_info4 import TelaInfo4
from view.paginas.tela_info5 import TelaInfo5

DIR_TELA = path.dirname(__file__)
PATH_IMGS = path.join(DIR_TELA, "images")

COR_HEADER = "#3f2a87"
COR_FUNDO = "#2d234d"
COR_TEXTO = "#E6E6F0"
COR_PESQUISA = "#E6E6F0"


def carregar_img(parent_frame, nome_img, tamanho, ancoragem):
    path_img = path.join(PATH_IMGS, nome_img)
    try:
        pil_original_image = Image.open(path_img)
        max_altura = tamanho
        original_width, original_height = pil_original_image.size
        aspect_ratio = original_width / float(original_height)

        img_altura_calc = max_altura
        img_larg_calc = int(img_altura_calc * aspect_ratio)

        pil_resized_image = pil_original_image.resize(
            (img_larg_calc, img_altura_calc), Image.Resampling.LANCZOS
        )

        ctk_porquinho_image = ctk.CTkImage(
            light_image=pil_resized_image,
            dark_image=pil_resized_image,
            size=(img_larg_calc, img_altura_calc),
        )

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

        # Lista de artigos
        self.articles_list = [
            "Quando comprar e vender ações?",
            "Entendendo os tipos de risco",
            "Como manter o saldo positivo",
            "Guardar também é investir?",
            "Como lucrar através das ações",
        ]

        # Dicionário que mapeia o título do artigo para a classe da tela info
        self.article_to_info = {
            self.articles_list[0]: TelaInfo1Frame,
            self.articles_list[1]: TelaInfo2,
            self.articles_list[2]: TelaInfo3,
            self.articles_list[3]: TelaInfo4,
            self.articles_list[4]: TelaInfo5,
        }

        # Header
        header = ctk.CTkFrame(self, height=50, fg_color=COR_HEADER, corner_radius=0)
        header.pack(fill="x", side="top", pady=(0, 20))

        menu_icon = ctk.CTkLabel(
            header,
            text="☰",
            font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"),
        )
        menu_icon.pack(side="left", padx=(25, 0), pady=15)

        carregar_img(header, "ricoIconVertical.png", 60, "w")

        # Barra de pesquisa
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=0, padx=20, fill="x")

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Como ficar rico com 5 reais...",
            fg_color=COR_PESQUISA,
            border_width=0,
            height=40,
            font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"),
        )
        search_entry.pack(expand=True, fill="x")

        # Container dos artigos com scroll
        articles_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        articles_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Cria a lista de artigos com clique para navegar para a tela info
        for article in self.articles_list:
            def article_click_handler(event, title=article):
                self.navegar_para_info(title)

            article_frame = ctk.CTkFrame(
                articles_container,
                fg_color=COR_HEADER,
                height=120,
                corner_radius=10,
                cursor="hand2",
            )
            article_frame.pack(fill="x", pady=6)

            article_frame.bind("<Button-1>", article_click_handler)

            label = ctk.CTkLabel(
                article_frame,
                text=article,
                font=ctk.CTkFont(family="Roboto-Regular", size=24, weight="bold"),
                text_color=COR_TEXTO,
                padx=20,
                pady=40,
            )
            label.pack(side="left", fill="x", expand=True)

            label.bind("<Button-1>", article_click_handler)

            setinha_label = ctk.CTkLabel(
                article_frame,
                text=">",
                font=ctk.CTkFont(family="Roboto-Regular", size=24, weight="bold"),
                text_color=COR_TEXTO,
                padx=20,
            )
            setinha_label.pack(side="right")
            setinha_label.bind("<Button-1>", article_click_handler)

    def navegar_para_info(self, artigo_titulo):
        info_frame_class = self.article_to_info.get(artigo_titulo)
        if info_frame_class:
            self.controller.mostrar_frame(info_frame_class)
        else:
            print(f"Tela info para o artigo '{artigo_titulo}' não encontrada.")
