import customtkinter as ctk
from tkinter import simpledialog
import random
from PIL import Image
import os

from view.tela_dict import telaDictFrame

# Supondo que você terá estes arquivos na pasta 'view'
# from view.tela_inicial import telaInicialFrame
# from view.tela_dict import telaDictFrame
# from view.jogo import JogoGUI # Já definido neste arquivo

# --------------------------
# Configurações iniciais
# --------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CORES_RISCO = {
    "Baixo": "#2ECC71",
    "Médio": "#F1C40F",
    "Alto": "#E74C3C"
}

SALDO_INICIAL = 10.00

# Lista de empresas com dados originais
empresas = [
    {"nome": "Orbit Capital", "icone": "orbitcapital.png", "risco": "Médio", "quantidade": 0, "preco_base": 2.50,
     "lucro_unitario": 0.80},
    {"nome": "Nexora Group", "icone": "nexoragroup.png", "risco": "Baixo", "quantidade": 0, "preco_base": 2.80,
     "lucro_unitario": 0.60},
    {"nome": "Skyline Dynamics", "icone": "skylinedynamics.png", "risco": "Alto", "quantidade": 0, "preco_base": 1.80,
     "lucro_unitario": 1.20},
    {"nome": "Stratos Edge", "icone": "stratosedge.png", "risco": "Alto", "quantidade": 0, "preco_base": 1.90,
     "lucro_unitario": 1.10},
    {"nome": "Veltrix Corp", "icone": "veltrixcorp.png", "risco": "Alto", "quantidade": 0, "preco_base": 1.50,
     "lucro_unitario": 0.90},
    {"nome": "Greenline", "icone": "greenline.png", "risco": "Baixo", "quantidade": 0, "preco_base": 2.30,
     "lucro_unitario": 0.50},
    {"nome": "Broadpeak", "icone": "broadpeak.png", "risco": "Médio", "quantidade": 0, "preco_base": 2.60,
     "lucro_unitario": 0.75},
    {"nome": "Solidity", "icone": "solidity.png", "risco": "Alto", "quantidade": 0, "preco_base": 1.60,
     "lucro_unitario": 1.30},
    {"nome": "Greenpoint", "icone": "greenpoint.png", "risco": "Médio", "quantidade": 0, "preco_base": 2.00,
     "lucro_unitario": 0.90},
    {"nome": "Lucrative", "icone": "lucrative.png", "risco": "Baixo", "quantidade": 0, "preco_base": 2.90,
     "lucro_unitario": 0.65},
]

# Guardar dados originais para reset
for emp in empresas:
    emp['preco_base_original'] = emp['preco_base']
    emp['risco_original'] = emp['risco']


class JogoGUI(ctk.CTkFrame):
    def __init__(self, master=None, parent_container=None, controller=None, **kwargs):
        super().__init__(master or parent_container, **kwargs)
        self.controller = controller
        self.configure(fg_color="#2E0068")

        # Inicialização de variáveis
        self.saldo = SALDO_INICIAL
        self.mes = 1
        self.empresas = empresas
        self.logo_images = []
        self.active_popups = []

        # Inicialização da sidebar
        self.sidebar_visible = False
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#3f2a87", corner_radius=0)
        # A sidebar é configurada e mostrada pela primeira vez em toggle_sidebar

        # Define o caminho para a pasta 'images'
        try:
            self.image_path = os.path.join(os.path.dirname(__file__), "images")
        except NameError:
            self.image_path = "images"

        # Criação do layout
        self._criar_header()
        self._criar_frame_empresas()
        self._criar_footer()
        self.atualizar_lista_empresas()

        # Mostrar tutorial após inicializar
        self.after(500, self._mostrar_tutorial)

    # ---------------------------------------------------
    # MÉTODOS DA NAVBAR/SIDEBAR FORNECIDOS PELO USUÁRIO
    # ---------------------------------------------------

    def setup_sidebar(self):
        """Configura a sidebar com seus widgets"""
        # Adiciona bind na sidebar para fechar ao clicar em qualquer lugar
        self.sidebar.bind("<Button-1>", lambda e: self.toggle_sidebar())

        # Label do menu
        menu_label = ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            font=ctk.CTkFont(family="Roboto-Regular", size=20, weight="bold"),
            text_color="white"
        )
        menu_label.pack(pady=(20, 10), padx=10)

        # Previne que o clique no label feche a sidebar
        menu_label.bind("<Button-1>", lambda e: "break")

        # Importações locais para evitar ciclos
        # NOTA: Estes imports exigem que você tenha os arquivos/classes correspondentes
        # no seu projeto, por exemplo, em uma pasta 'view'.
        from view.tela_inicial import telaInicialFrame
        # from view.tela_dict import telaDictFrame # Este não foi usado no seu snippet

        def create_button_command(command):
            def wrapper():
                command()  # Executa o comando original
                self.toggle_sidebar()  # Fecha a sidebar

            return wrapper

        buttons_data = [
            ("Dicionário", lambda: self.controller.mostrar_frame(telaDictFrame)),
            ("Sair", lambda: self.controller.mostrar_frame(telaInicialFrame)),
        ]

        for text, command in buttons_data:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=create_button_command(command),  # Wrap o comando original
                fg_color="#3f2a87",
                hover_color="#6457d1",
                height=40,
                corner_radius=8
            )
            btn.pack(pady=5, padx=10, fill="x")
            # Previne que o clique no botão propague para a sidebar
            btn.bind("<Button-1>", lambda e: "break", add="+")

    def animate_sidebar(self, show=True):
        """Anima a entrada/saída da sidebar"""
        if show:
            # Garante que a sidebar seja configurada apenas uma vez
            if not hasattr(self, "_sidebar_setup_done"):
                self.setup_sidebar()
                self._sidebar_setup_done = True

            self.sidebar.place(x=-200, y=0, relheight=1)  # Começa fora da tela
            self.sidebar.lift()
            for i in range(-200, 1, 20):  # Animação de entrada mais suave
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update_idletasks()
                self.after(5)
        else:
            for i in range(0, -201, -20):  # Animação de saída mais suave
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update_idletasks()
                self.after(5)
            self.sidebar.place_forget()

    def toggle_sidebar(self, event=None):
        """Alterna a visibilidade da sidebar com animação"""
        if self.sidebar_visible:
            self.animate_sidebar(show=False)
            self.sidebar_visible = False
        else:
            self.animate_sidebar(show=True)
            self.sidebar_visible = True

    # ------------------------------------------
    # MÉTODOS DE CRIAÇÃO DA INTERFACE DO JOGO
    # ------------------------------------------

    def _criar_header(self):
        """Cria o cabeçalho do jogo"""
        topo = ctk.CTkFrame(self, fg_color="#2E0068")
        topo.pack(fill="x", padx=20, pady=10)

        # Ícone do menu "☰" para abrir a sidebar
        self.menu_icon = ctk.CTkLabel(
            topo,
            text="☰",
            font=ctk.CTkFont(family="Roboto-Regular", size=22, weight="bold"),
            cursor="hand2",
            text_color="white"
        )
        self.menu_icon.pack(side="left", padx=(0, 15), pady=(0, 5))
        self.menu_icon.bind("<Button-1>", self.toggle_sidebar)

        # Botão Home (opcional, mantido da versão original)
        try:
            home_icon_path = os.path.join(self.image_path, "home.png")
            img = Image.open(home_icon_path)
            self.home_image = ctk.CTkImage(img, size=(30, 30))
            home_text = ""
        except (FileNotFoundError, NameError):
            self.home_image = None
            home_text = "🏠"

        ctk.CTkButton(
            topo,
            image=self.home_image,
            text=home_text,
            font=("Arial", 24),
            fg_color="transparent",
            hover_color="#4A0072",
            width=36,
            height=36,
            corner_radius=18,
            command=self._voltar_home
        ).pack(side="left", padx=(0, 10))

        # Label Saldo
        saldo_frame = ctk.CTkFrame(topo, fg_color="transparent")
        saldo_frame.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(saldo_frame, text="Saldo", font=("Arial", 10), text_color="white").pack(anchor="w")
        self.label_saldo = ctk.CTkLabel(
            saldo_frame,
            text=f"R$ {self.saldo:,.2f}".replace(",", "."),
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        self.label_saldo.pack(anchor="w")

        # Label Meses
        mes_frame = ctk.CTkFrame(topo, fg_color="transparent")
        mes_frame.pack(side="right")
        ctk.CTkLabel(mes_frame, text="Meses", font=("Arial", 10), text_color="white").pack()
        self.label_mes = ctk.CTkLabel(
            mes_frame,
            text=f"{self.mes}x",
            font=("Arial", 14),
            fg_color="#D9D9D9",
            text_color="black",
            corner_radius=14,
            width=60,
            height=28
        )
        self.label_mes.pack()

    def _voltar_home(self):
        """Reseta o estado do jogo e volta para a tela inicial."""
        self.saldo = SALDO_INICIAL
        self.mes = 1
        for emp in self.empresas:
            emp['quantidade'] = 0
            emp['preco_base'] = emp['preco_base_original']
            emp['risco'] = emp['risco_original']

        if hasattr(self, 'controller') and self.controller:
            # Este import precisa funcionar para o botão home funcionar
            from view.tela_inicial import telaInicialFrame
            self.controller.mostrar_frame(telaInicialFrame)
        else:
            # Fallback se não houver controller
            self.atualizar_tela()

    def _criar_frame_empresas(self):
        container = ctk.CTkFrame(self, fg_color="#2E0068")
        container.pack(fill="both", expand=True, pady=(0, 10))
        self.canvas_empresas = ctk.CTkScrollableFrame(
            container,
            fg_color="#2E0068",
            border_width=0,
            corner_radius=0
        )
        self.canvas_empresas.pack(fill="both", expand=True, padx=10, pady=5)

    def _criar_footer(self):
        rodape = ctk.CTkFrame(self, fg_color="#2E0068")
        rodape.pack(fill="x", pady=10)
        estilo_btn = {"font": ("Arial", 12, "bold"), "width": 120, "height": 40, "corner_radius": 12}
        ctk.CTkButton(
            rodape, text="⮕ Avançar", fg_color="white", text_color="black",
            hover_color="#DDDDDD", command=self.avancar_mes, **estilo_btn
        ).pack(anchor="center", padx=10, pady=4)

    def atualizar_lista_empresas(self):
        for w in self.canvas_empresas.winfo_children():
            w.destroy()
        self.logo_images.clear()
        for idx, emp in enumerate(self.empresas):
            preco = self.calcular_preco(emp)
            self._criar_card_empresa(idx, emp, preco)

    def _criar_card_empresa(self, index, empresa, preco):
        card = ctk.CTkFrame(self.canvas_empresas, fg_color="white", corner_radius=20)
        card.pack(pady=10, padx=10, fill="x")

        # Risco
        cor = CORES_RISCO.get(empresa['risco'], 'gray')
        ctk.CTkLabel(
            card,
            text=f"{empresa['risco']} risco",
            fg_color=cor,
            text_color="white",
            font=("Arial", 9, "bold"),
            corner_radius=6,
            height=20,
            width=80
        ).pack(pady=(8, 4))

        content = ctk.CTkFrame(card, fg_color="white")
        content.pack(fill="x", padx=10, pady=(0, 10))

        # Logo e quantidade
        logo_f = ctk.CTkFrame(content, fg_color="transparent")
        logo_f.pack(side="left", padx=5, fill="y")
        try:
            icon_path = os.path.join(self.image_path, empresa['icone'])
            if not os.path.exists(icon_path):
                raise FileNotFoundError
            img = ctk.CTkImage(Image.open(icon_path), size=(64, 64))
            self.logo_images.append(img)
            ctk.CTkLabel(logo_f, image=img, text="").pack(side="left", pady=5)
        except (FileNotFoundError, NameError):
            ctk.CTkLabel(logo_f, text="📈", font=("Arial", 30), text_color="black").pack(side="left", pady=5, padx=10)

        ctk.CTkLabel(
            logo_f,
            text=f"{empresa['quantidade']}",
            fg_color="#4B2E83",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=40,
            height=40,
            corner_radius=20
        ).pack(side="left", padx=(6, 0), pady=5)

        # Info nome e custo
        info_f = ctk.CTkFrame(content, fg_color="transparent")
        info_f.pack(side="left", padx=5, fill="both", expand=True)
        ctk.CTkLabel(info_f, text=empresa['nome'], font=("Arial", 13, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(
            info_f,
            text=f"Custo: R$ {preco:,.2f}".replace(",", "."),
            font=("Arial", 9),
            text_color="black"
        ).pack(anchor="w", pady=(4, 0))

        # Botões Comprar/Vender e lucro
        right_f = ctk.CTkFrame(content, fg_color="transparent")
        right_f.pack(side="right", padx=5, fill="y")
        ctk.CTkLabel(
            right_f,
            text=f"+ R$ {empresa['quantidade'] * empresa['lucro_unitario']:,.2f}".replace(",", "."),
            font=("Arial", 12, "bold"),
            text_color="#2ECC71"
        ).pack(anchor="e")
        ctk.CTkButton(
            right_f,
            text="Comprar",
            font=("Arial", 10, "bold"),
            fg_color="#27AE60",
            hover_color="#219653",
            command=lambda i=index: self.comprar(i)
        ).pack(fill="x", pady=(4, 4))
        ctk.CTkButton(
            right_f,
            text="Vender",
            font=("Arial", 10, "bold"),
            fg_color="#F1C40F",
            hover_color="#F39C12",
            command=lambda i=index: self.vender(i)
        ).pack(fill="x")

    def calcular_preco(self, emp):
        return emp['preco_base'] * (1.07 ** emp['quantidade'])

    def comprar(self, index):
        emp = self.empresas[index]
        preco = self.calcular_preco(emp)
        if self.saldo >= preco:
            self.saldo -= preco
            emp['quantidade'] += 1
            self.atualizar_lista_empresas()
            self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))
        else:
            self._mostrar_popup("Saldo insuficiente", f"Você precisa de R$ {preco:,.2f}".replace(",", "."),
                                "#E74C3C")

    def vender(self, index):
        emp = self.empresas[index]
        if emp['quantidade'] == 0:
            return self._mostrar_popup("Sem ações", "Você não possui ações dessa empresa.", "#E74C3C")

        main_window = self.winfo_toplevel()
        qtd = simpledialog.askinteger("Vender ações",
                                      f"Quantas ações de {emp['nome']} quer vender?",
                                      parent=main_window,
                                      minvalue=1, maxvalue=emp['quantidade'])
        if qtd is None:
            return

        preco_unitario = emp['preco_base'] * (1.07 ** (emp['quantidade'] - 1))
        total = preco_unitario * qtd

        emp['quantidade'] -= qtd
        self.saldo += total
        self.atualizar_lista_empresas()
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))

    def avancar_mes(self):
        self.mes += 1
        eventos = self._verificar_eventos()
        lucro = sum(e['quantidade'] * e['lucro_unitario'] for e in self.empresas)
        self.saldo += lucro

        def show_lucro():
            self._mostrar_popup("Lucro do mês",
                                f"Você recebeu R$ {lucro:,.2f}".replace(",", "."),
                                "#2ECC71", callback=self.atualizar_tela)

        if eventos:
            self._mostrar_popup("Eventos do mês",
                                "\n".join(eventos),
                                "#3498DB", callback=show_lucro)
        else:
            show_lucro()

    def _verificar_eventos(self):
        lista = []
        for e in self.empresas:
            if random.random() < 0.2:
                if random.choice([True, False]):
                    e['preco_base'] *= 0.7
                    e['risco'] = 'Alto'
                    lista.append(f"{e['nome']} teve queda de 30%! Risco ALTO agora.")
                else:
                    e['preco_base'] *= 1.25
                    e['risco'] = 'Baixo'
                    lista.append(f"{e['nome']} teve alta de 25%! Risco BAIXO agora.")
        return lista

    def atualizar_tela(self):
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))
        self.label_mes.configure(text=f"{self.mes}x")
        self.atualizar_lista_empresas()

    def _mostrar_popup(self, titulo, mensagem, cor_cabecalho="#3498DB", callback=None):
        main_window = self.winfo_toplevel()
        popup = ctk.CTkToplevel(main_window)
        popup.transient(main_window)
        popup.overrideredirect(True)
        popup.grab_set()

        is_special = titulo in ("Eventos do mês", "Lucro do mês")
        popup._popup_width = 320 if is_special else 300
        popup._popup_height = 200 if is_special else 180
        self._position_popup(popup)

        cont = ctk.CTkFrame(popup, corner_radius=20 if is_special else 12,
                            fg_color="#2E0068" if is_special else "white")
        cont.pack(fill="both", expand=True)

        cab = ctk.CTkFrame(cont, fg_color="#4B2E83" if is_special else cor_cabecalho,
                           corner_radius=20 if is_special else 12)
        cab.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(cab, text=titulo, font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=12,
                                                                                            pady=10)
        if titulo == "Eventos do mês":
            ctk.CTkLabel(cab, text="⌄", font=("Arial", 14, "bold"), text_color="white").pack(side="right", padx=12,
                                                                                             pady=10)

        body = ctk.CTkFrame(cont, corner_radius=12, fg_color="#2E0068" if is_special else "#F2F2F2")
        body.pack(fill="both", expand=True, padx=12, pady=(8, 12) if is_special else (0, 10))
        ctk.CTkLabel(body, text=mensagem, font=("Arial", 11), text_color="white" if is_special else "#2C3E50",
                     wraplength=296 if is_special else 260, justify="left").pack(padx=10, pady=10)

        def fechar():
            self.active_popups.remove(popup)
            popup.destroy()
            if callback: callback()

        btn = ctk.CTkButton(cont, text="OK", fg_color="#4B2E83" if is_special else cor_cabecalho,
                            hover_color="#3B1E6F" if is_special else None, text_color="white",
                            font=("Arial", 11, "bold"), corner_radius=12 if is_special else 8, command=fechar, width=80,
                            height=32 if is_special else 30)
        btn.pack(pady=(0, 12) if is_special else (0, 10))

        popup.bind("<Escape>", lambda e: fechar())
        popup.lift()
        self.active_popups.append(popup)

    def _position_popup(self, popup):
        main_window = self.winfo_toplevel()
        rx, ry = main_window.winfo_rootx(), main_window.winfo_rooty()
        rw, rh = main_window.winfo_width(), main_window.winfo_height()
        pw, ph = popup._popup_width, popup._popup_height
        x = rx + (rw - pw) // 2
        y = ry + (rh - ph) // 2
        popup.geometry(f"{pw}x{ph}+{x}+{y}")

    def _on_main_move(self, event):
        for p in list(self.active_popups):
            if p.winfo_exists():
                self._position_popup(p)
            else:
                self.active_popups.remove(p)

    def _mostrar_tutorial(self):
        main_window = self.winfo_toplevel()
        popup = ctk.CTkToplevel(main_window)
        popup.transient(main_window)
        popup.overrideredirect(True)
        popup.grab_set()
        popup._popup_width = 320
        popup._popup_height = 240
        self._position_popup(popup)

        cont = ctk.CTkFrame(popup, corner_radius=20, fg_color="#2E0068")
        cont.pack(fill="both", expand=True)

        cab = ctk.CTkFrame(cont, fg_color="#6A1B9A", corner_radius=20)
        cab.pack(fill="x")
        ctk.CTkLabel(cab, text="📘 Tutorial", font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=12,
                                                                                                  pady=10)

        body = ctk.CTkFrame(cont, fg_color="#2E0068", corner_radius=12)
        body.pack(fill="both", expand=True, padx=12, pady=(8, 12))
        ctk.CTkLabel(body, text=("Invista em empresas, acumule lucros mensais e reaja a eventos de mercado.\n\n"
                                 "• Clique em 'Comprar' ou 'Vender'.\n"
                                 "• Avance o tempo para receber lucros.\n"
                                 "• Cuidado com o risco!"),
                     font=("Arial", 11), text_color="white", justify="left", wraplength=296).pack(padx=10, pady=10)

        def fechar_tutorial():
            self.active_popups.remove(popup)
            popup.destroy()

        ctk.CTkButton(cont, text="Entendi", fg_color="#6A1B9A", hover_color="#4A0072", text_color="white",
                      font=("Arial", 11, "bold"), corner_radius=12, command=fechar_tutorial, width=100,
                      height=32).pack(pady=(0, 12))

        popup.bind("<Escape>", lambda e: fechar_tutorial())
        popup.lift()
        self.active_popups.append(popup)


# --------------------------
# Classe Principal da Aplicação
# --------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Ações")
        self.geometry("360x700")

        # Container para os frames
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Cria uma instância de JogoGUI
        # Passando 'self' como controller
        frame = JogoGUI(master=container, controller=self)
        self.frames[JogoGUI] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Adicione outros frames aqui se necessário, por exemplo:
        # from view.tela_inicial import telaInicialFrame
        # frame_inicial = telaInicialFrame(master=container, controller=self)
        # self.frames[telaInicialFrame] = frame_inicial
        # frame_inicial.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(JogoGUI)  # Mostra o frame inicial

        # Associa o evento de mover a janela à função de reposicionar popups do frame
        self.bind("<Configure>", self.on_window_move)

    def mostrar_frame(self, page_name):
        '''Mostra um frame para a página solicitada'''
        frame = self.frames[page_name]
        frame.tkraise()

    def on_window_move(self, event):
        # Chama a função correspondente dentro do frame do jogo visível
        # (Idealmente, isso deveria ser gerenciado de forma mais robusta se houver muitos popups em frames diferentes)
        current_frame = self.frames[JogoGUI]  # Simplificação
        current_frame._on_main_move(event)


if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Pasta 'images' criada. Por favor, adicione os ícones das empresas nela.")


    # Para o código funcionar, você precisará de uma estrutura como esta:
    # │
    # ├── main.py (onde a classe App está)
    # └── view/
    #     ├── __init__.py
    #     ├── jogo.py (onde a classe JogoGUI está)
    #     └── tela_inicial.py (onde a classe telaInicialFrame estaria)

    # Como estamos executando um único arquivo, criamos uma classe 'mock' para telaInicialFrame
    class telaInicialFrame(ctk.CTkFrame):
        def __init__(self, master, controller):
            super().__init__(master)
            self.configure(fg_color="black")
            label = ctk.CTkLabel(self, text="Tela Inicial (Mock)\nFeche para sair.", font=("Arial", 20))
            label.pack(pady=100, padx=50)
            btn = ctk.CTkButton(self, text="Sair do App", command=controller.destroy)
            btn.pack()


    # E modificamos a App para incluir este frame mock
    original_app_init = App.__init__


    def new_app_init(self):
        original_app_init(self)
        container = self.winfo_children()[0]
        frame_inicial = telaInicialFrame(master=container, controller=self)
        self.frames[telaInicialFrame] = frame_inicial
        frame_inicial.grid(row=0, column=0, sticky="nsew")
        self.mostrar_frame(JogoGUI)  # Garante que o jogo comece primeiro


    App.__init__ = new_app_init

    app = App()
    app.mainloop()