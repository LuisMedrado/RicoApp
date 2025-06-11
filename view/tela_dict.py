import customtkinter as ctk
import tela_inicial as modulo_inicial
from os import path, listdir
from PIL import Image
from pyglet import font as pfont

DIR_TELA = path.dirname(__file__)
PATH_FONTS = path.join(DIR_TELA, "fonts")
PATH_IMGS = path.join(DIR_TELA, "images")

COR_HEADER = "#3f2a87"
COR_SUBHEADER = "#7a6ef5"
COR_FUNDO = "#2d234d"
COR_TEXTO = "#E6E6F0"
COR_PESQUISA = "#E6E6F0"

modulo_inicial.carregar_fontes_globais()

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

class telaInicialFrame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RICO")
        self.configure(fg_color=COR_FUNDO)
        self.resizable(True, True)
        self.after(1, lambda: self.state("zoomed"))

        # SÓ UM PROTÓTIPO, PRA TESTAR OS ARTIGOS
        def get_articles():
            """Ainda temos que implementar aqui um request do model/get_articles e estruturar a saída"""
            return [
                # placeholders por enquanto
                "Quando comprar e vender ações?",
                "Entendendo os tipos de risco",
                "Como manter o saldo positivo",
                "Guardar também é investir?",
                "Como lucrar através das ações"
            ]

        # header
        header = ctk.CTkFrame(self, height=50, fg_color=COR_HEADER, corner_radius=0)
        header.pack(fill="x", side="top", pady=(0, 20))

        menu_icon = ctk.CTkLabel(header, text="☰", font=(ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold"), 22))
        menu_icon.pack(side="left", padx=(25, 0), pady=15)

        carregar_img(header, "ricoIconVertical.png", 60, "w")

        # barra de pesquisa

        # não sei se botamos uma query direto do banco aqui ou não, por segurança acho melhor não
        # acho melhor fazer uma lógica de retornar os artigos como texto na get_articles(), e salvar em uma lista* o resultado *(LER A LINHA 112). 
        # depois, percorrer a lista buscando pelo termo digitado
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=0, padx=20, fill="x")

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Como ficar rico com 5 reais...",
            fg_color=COR_PESQUISA,
            border_width=0,
            height=40,
            font=ctk.CTkFont(family="Roboto-Regular", size=16, weight="bold")
        )
        search_entry.pack(expand=True, fill="x")

        # container pros artigos, acho que vamos precisar de um scroll então já coloquei
        articles_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        articles_container.pack(pady=20, padx=20, fill="both", expand=True)

        # puxar os artigos nessa call
        articles_list = get_articles()

        for article in articles_list:
            # DEBUG teste clique nos artigos
            def article_click_handler(title=article):
                print(f"artigo clicado: {title}")

            # frame para cada artigo
            article_frame = ctk.CTkFrame(
                articles_container,
                fg_color=COR_HEADER,
                height=120,
                corner_radius=10,
                cursor="hand2" 
            )
            article_frame.pack(fill="x", pady=6)

            # listener do clique no frame
            article_frame.bind("<Button-1>", lambda event, title=article: article_click_handler(title))


            # título do artigo
            label = ctk.CTkLabel(
                article_frame,
                text=article,
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=80,
                pady=120
            )
            label.pack(side="left", fill="x", expand=False)
            # listener do clique no texto
            label.bind("<Button-1>", lambda event, title=article: article_click_handler(title))


            # setinha placeholder, trocar pelas imagens depois

            # vamos precisar ver como vamos retornar as imagens junto ao título dos artigos.
            # podemos fazer o retorno como um dicionário em vez de uma lista.
            # nesse caso, talvez teríamos um pouco mais de trabalho pra percorrer os artigos no algoritmo de busca.
            setinha_label = ctk.CTkLabel(
                article_frame,
                text=">",
                font=ctk.CTkFont(family="Roboto-Regular", size=36, weight="bold"),
                text_color=COR_TEXTO,
                padx=20
            )
            setinha_label.pack(side="right")
            # listener do clique na setinha
            setinha_label.bind("<Button-1>", lambda event, title=article: article_click_handler(title))


if __name__ == "__main__":
    app = telaInicialFrame()
    app.mainloop()