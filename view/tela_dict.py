import customtkinter as ctk
from os import path
from PIL import Image
from pyglet import font as pfont
from view.utils import carregar_fontes_globais

DIR_TELA = path.dirname(__file__)
PATH_FONTS = path.join(DIR_TELA, "fonts")
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

        img_altura_calc = max_altura
        img_larg_calc = int(img_altura_calc * aspect_ratio)

        pil_resized_image = pil_original_image.resize((img_larg_calc, img_altura_calc), Image.Resampling.LANCZOS)

        ctk_porquinho_image = ctk.CTkImage(light_image=pil_resized_image,
                                           dark_image=pil_resized_image,
                                           size=(img_larg_calc, img_altura_calc))

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

        self.sidebar_visible = False
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=COR_HEADER, corner_radius=0)

        # header
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

        self.setup_sidebar()

        # Barra de pesquisa
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=0, padx=20, fill="x")

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Como ficar rico com 5 reais...",
            fg_color=COR_PESQUISA,
            text_color="1E1B2E",
            border_width=0,
            height=40,
            font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
        )
        search_entry.pack(expand=True, fill="x")

        # Container para artigos
        articles_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        articles_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Carregar artigos
        articles_list = self.get_articles()
        self.create_article_widgets(articles_container, articles_list)

    def get_articles(self):
        """Retorna lista de artigos (placeholder)"""
        return [
            "Quando comprar e vender ações?",
            "Entendendo os tipos de risco",
            "Como manter o saldo positivo",
            "Guardar também é investir?",
            "Como lucrar através das ações"
        ]

    def setup_sidebar(self):
        from view.jogo import JogoGUI
        ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            font=ctk.CTkFont(family="Roboto-Regular", size=20, weight="bold"),
            text_color=COR_TEXTO
        ).pack(pady=(20, 10), padx=10)



        # Importações locais para evitar ciclos
        from view.tela_inicial import telaInicialFrame
        from view.tela_dict import telaDictFrame  # auto-import para exemplificar (poderia ser outra tela)
        # Adapte os imports conforme suas telas existentes!

        buttons_data = [
            ("Jogo", lambda: self.controller.mostrar_frame(JogoGUI)),
            ("Sair", lambda: self.controller.mostrar_frame(telaInicialFrame)),

            # Adicione outros botões, conectando com as telas que desejar
            # ("Configurações", lambda: self.controller.mostrar_frame(SuaTelaConfig)),
        ]
        for text, command in buttons_data:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color=COR_SUBHEADER,
                hover_color="#6457d1",
                height=40,
                corner_radius=8
            ).pack(pady=5, padx=10, fill="x")

    def animate_sidebar(self, show=True):
        """Anima a entrada/saída da sidebar"""
        if show:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar.lift()
            for i in range(-200, 1, 10):
                self.sidebar.place(x=i, rely=0, relheight=1)
                self.update()
                self.after(10)
        else:
            for i in range(0, -201, -10):
                self.sidebar.place(x=i, rely=0, relheight=1)
                self.update()
                self.after(10)
            self.sidebar.pack_forget()

    def toggle_sidebar(self, event=None):
        """Alterna a visibilidade da sidebar com animação"""
        if self.sidebar_visible:
            self.animate_sidebar(show=False)
            self.sidebar_visible = False
        else:
            self.animate_sidebar(show=True)
            self.sidebar_visible = True

    def create_article_widgets(self, container, articles):
        """Cria os widgets para cada artigo"""
        for article in articles:
            article_frame = ctk.CTkFrame(
                container,
                fg_color=COR_HEADER,
                height=120,
                corner_radius=10,
                cursor="hand2"
            )
            article_frame.pack(fill="x", pady=6)
            article_frame.bind("<Button-1>", lambda event, title=article: self.article_click_handler(title))

            label = ctk.CTkLabel(
                article_frame,
                text=article,
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=80,
                pady=120
            )
            label.pack(side="left", fill="x", expand=False)
            label.bind("<Button-1>", lambda event, title=article: self.article_click_handler(title))

            setinha_label = ctk.CTkLabel(
                article_frame,
                text=">",
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=20
            )
            setinha_label.pack(side="right")
            setinha_label.bind("<Button-1>", lambda event, title=article: self.article_click_handler(title))

    def article_click_handler(self, title):
        print(f"artigo clicado: {title}")