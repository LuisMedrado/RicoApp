import customtkinter as ctk
from tkinter import simpledialog
import random
from PIL import Image
import os

# --- Constantes e Configurações Visuais (Layout Atual) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLOR_BACKGROUND = "#4E2E91"
COLOR_CARD_BACKGROUND = "#E9E4F4"
COLOR_CARD_TEXT = "#333333"
COLOR_ACCENT = "#6A45B3"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_GREEN = "#27AE60"
COLOR_YELLOW = "#F1C40F"
COR_HEADER_SIDEBAR = "#3f2a87"
COR_SUBHEADER_SIDEBAR = "#7a6ef5"

# --- DADOS E VALORES (DO CÓDIGO ANTIGO) ---
CORES_RISCO = {
    "Baixo": "#2ECC71",
    "Médio": "#F1C40F",
    "Alto": "#E74C3C"
}

SALDO_INICIAL = 10.00

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
        self.configure(fg_color=COLOR_BACKGROUND)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Variáveis de estado usando os dados do código antigo ---
        self.saldo = SALDO_INICIAL
        self.mes = 1
        self.empresas = empresas
        self.logo_images = {}  # Usar dicionário é mais seguro que lista para imagens
        self.active_popups = []

        # Variáveis da sidebar
        self.sidebar_visible = False
        self._sidebar_setup_done = False
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=COR_HEADER_SIDEBAR, corner_radius=0)

        try:
            self.image_path = os.path.join(os.path.dirname(__file__), "images")
        except NameError:
            self.image_path = "images"

        self._criar_painel_esquerdo()
        self._criar_painel_direito()
        self.atualizar_lista_empresas()

        # Reativando o tutorial do código antigo
        self.after(500, self._mostrar_tutorial)

    # --- Métodos da Sidebar ---
    def setup_sidebar(self):
        if self._sidebar_setup_done:
            return

        from view.tela_inicial import telaInicialFrame
        from view.tela_dict import telaDictFrame

        self.sidebar.bind("<Button-1>", lambda e: self.toggle_sidebar())
        menu_label = ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=20, weight="bold"),
                                  text_color=COLOR_TEXT_LIGHT)
        menu_label.pack(pady=(20, 10), padx=10)
        menu_label.bind("<Button-1>", lambda e: "break")

        def create_button_command(command):
            def wrapper():
                command()
                self.toggle_sidebar()

            return wrapper

        buttons_data = [
            ("Dicionário", lambda: self.controller.mostrar_frame(telaDictFrame)),
            ("Sair", lambda: self.controller.mostrar_frame(telaInicialFrame)),
        ]

        for text, command in buttons_data:
            btn = ctk.CTkButton(self.sidebar, text=text, command=create_button_command(command),
                                fg_color=COR_HEADER_SIDEBAR, hover_color=COR_SUBHEADER_SIDEBAR, height=40,
                                corner_radius=8)
            btn.pack(pady=5, padx=10, fill="x")
            btn.bind("<Button-1>", lambda e: "break", add="+")

        self._sidebar_setup_done = True

    def animate_sidebar(self, show=True):
        if show:
            self.setup_sidebar()
            self.sidebar.lift()
            for i in range(-200, 1, 20):
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update_idletasks()
                self.after(5)
        else:
            for i in range(0, -201, -20):
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update_idletasks()
                self.after(5)
            self.sidebar.place_forget()

    def toggle_sidebar(self, event=None):
        self.sidebar_visible = not self.sidebar_visible
        self.animate_sidebar(show=self.sidebar_visible)

    # --- Métodos de Criação do Layout ---
    def _criar_painel_esquerdo(self):
        painel_esquerdo = ctk.CTkFrame(self, fg_color="transparent")
        painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        top_bar_frame = ctk.CTkFrame(painel_esquerdo, fg_color="transparent")
        top_bar_frame.pack(pady=10, anchor="w", fill="x")

        self.menu_icon = ctk.CTkLabel(
            top_bar_frame, text="☰", font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLOR_TEXT_LIGHT, cursor="hand2"
        )
        self.menu_icon.pack(side="left", padx=(0, 15), pady=10)
        self.menu_icon.bind("<Button-1>", self.toggle_sidebar)

        try:
            avatar_path = os.path.join(self.image_path, "avatar.png")
            avatar_img = ctk.CTkImage(Image.open(avatar_path), size=(64, 64))
        except:
            avatar_img = None
        ctk.CTkLabel(top_bar_frame, image=avatar_img, text="").pack(side="left", padx=(0, 15))

        saldo_frame_text = ctk.CTkFrame(top_bar_frame, fg_color="transparent")
        saldo_frame_text.pack(side="left")
        ctk.CTkLabel(saldo_frame_text, text="Saldo", font=ctk.CTkFont(size=18), text_color=COLOR_TEXT_LIGHT).pack(
            anchor="w")
        self.label_saldo = ctk.CTkLabel(saldo_frame_text, text=f"R$ {self.saldo:,.2f}",
                                        font=ctk.CTkFont(size=22, weight="bold"), text_color=COLOR_TEXT_LIGHT)
        self.label_saldo.pack(anchor="w")

        ctk.CTkFrame(painel_esquerdo, fg_color="transparent").pack(pady=20, expand=True)

        ctk.CTkButton(
            painel_esquerdo, text="⏸ Parar", font=ctk.CTkFont(size=16, weight="bold"), command=self._voltar_home,
            fg_color=COLOR_CARD_BACKGROUND, text_color=COLOR_ACCENT, hover_color="#FFFFFF", corner_radius=12, height=50
        ).pack(fill="x", pady=5)
        ctk.CTkButton(
            painel_esquerdo, text="❯ Avançar", font=ctk.CTkFont(size=16, weight="bold"), command=self.avancar_mes,
            fg_color=COLOR_CARD_BACKGROUND, text_color=COLOR_ACCENT, hover_color="#FFFFFF", corner_radius=12, height=50
        ).pack(fill="x", pady=5)

    def _criar_painel_direito(self):
        painel_direito = ctk.CTkFrame(self, fg_color="transparent")
        painel_direito.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        mes_frame = ctk.CTkFrame(painel_direito, fg_color="transparent")
        mes_frame.pack(anchor="ne", pady=(0, 10))
        ctk.CTkLabel(mes_frame, text="Meses", font=ctk.CTkFont(size=14), text_color=COLOR_TEXT_LIGHT).pack()
        self.label_mes = ctk.CTkLabel(
            mes_frame, text=f"{self.mes}x", font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT,
            corner_radius=10, width=60, height=30
        )
        self.label_mes.pack()

        self.canvas_empresas = ctk.CTkScrollableFrame(
            painel_direito, fg_color="transparent", border_width=0, corner_radius=0
        )
        self.canvas_empresas.pack(fill="both", expand=True)

    def _criar_card_empresa(self, index, empresa, preco):
        card = ctk.CTkFrame(self.canvas_empresas, fg_color=COLOR_CARD_BACKGROUND, corner_radius=16)
        card.pack(pady=8, padx=10, fill="x")
        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(card, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="n")

        try:
            icon_path = os.path.join(self.image_path, empresa['icone'])
            img = ctk.CTkImage(Image.open(icon_path), size=(48, 48))
        except:
            img = None

        label_img = ctk.CTkLabel(left_frame, image=img, text="" if img else "📈")
        label_img.pack()

        ctk.CTkLabel(
            left_frame, text=f"{empresa['quantidade']}", fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT,
            font=ctk.CTkFont(size=11, weight="bold"), width=32, height=32, corner_radius=16
        ).pack(pady=5)

        right_frame = ctk.CTkFrame(card, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")
        right_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            right_frame, text=empresa['nome'], font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_CARD_TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="nw", pady=(0, 5))

        cor_risco = CORES_RISCO.get(empresa['risco'], 'gray')
        ctk.CTkLabel(
            right_frame, text=f"{empresa['risco']} risco", fg_color=cor_risco, text_color="white",
            font=ctk.CTkFont(size=10, weight="bold"), corner_radius=6, height=20
        ).grid(row=0, column=1, columnspan=2, sticky="ne", pady=(0, 5))

        lucro_mensal = empresa['quantidade'] * empresa['lucro_unitario']
        lucro_frame = ctk.CTkFrame(right_frame, fg_color=COLOR_ACCENT, corner_radius=8, height=30)
        lucro_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(25, 5))
        ctk.CTkLabel(
            lucro_frame, text=f"+ R$ {lucro_mensal:,.2f}", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXT_LIGHT
        ).pack(pady=5)

        action_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        action_frame.grid_columnconfigure((0, 2), weight=1)
        action_frame.grid_columnconfigure(1, weight=0)

        ctk.CTkButton(
            action_frame, text="Comprar", font=ctk.CTkFont(size=11, weight="bold"), fg_color=COLOR_GREEN,
            hover_color="#219653", command=lambda i=index: self.comprar(i), corner_radius=8, height=30
        ).grid(row=0, column=0, sticky="ew", padx=5)

        custo_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        custo_frame.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(custo_frame, text="Custo", font=ctk.CTkFont(size=10), text_color=COLOR_CARD_TEXT).pack()
        ctk.CTkLabel(custo_frame, text=f"{preco:,.2f}", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLOR_CARD_TEXT).pack()

        ctk.CTkButton(
            action_frame, text="Vender", font=ctk.CTkFont(size=11, weight="bold"), fg_color=COLOR_YELLOW,
            text_color=COLOR_CARD_TEXT, hover_color="#F39C12", command=lambda i=index: self.vender(i),
            corner_radius=8, height=30
        ).grid(row=0, column=2, sticky="ew", padx=5)

    # --- Métodos de Lógica ---
    def atualizar_lista_empresas(self):
        for w in self.canvas_empresas.winfo_children():
            w.destroy()
        for idx, emp in enumerate(self.empresas):
            preco = self.calcular_preco(emp)
            self._criar_card_empresa(idx, emp, preco)

    def _voltar_home(self):
        self.saldo = SALDO_INICIAL
        self.mes = 1
        for emp in self.empresas:
            emp['quantidade'] = 0
            emp['preco_base'] = emp['preco_base_original']
            emp['risco'] = emp['risco_original']
        if hasattr(self, 'controller') and self.controller:
            from view.tela_inicial import telaInicialFrame
            self.controller.mostrar_frame(telaInicialFrame)
        else:
            self.atualizar_tela()

    def calcular_preco(self, emp):
        return emp['preco_base'] * (1.07 ** emp['quantidade'])

    def comprar(self, index):
        emp = self.empresas[index]
        preco = self.calcular_preco(emp)
        if self.saldo >= preco:
            self.saldo -= preco
            emp['quantidade'] += 1
            self.atualizar_tela()
        else:
            self._mostrar_popup("Saldo insuficiente", f"Você precisa de R$ {preco:,.2f}", "#E74C3C")

    def vender(self, index):
        emp = self.empresas[index]
        if emp['quantidade'] == 0:
            return self._mostrar_popup("Sem ações", "Você não possui ações dessa empresa.", "#E74C3C")
        main_window = self.winfo_toplevel()
        qtd = simpledialog.askinteger("Vender ações", f"Quantas ações de {emp['nome']} quer vender?",
                                      parent=main_window, minvalue=1, maxvalue=emp['quantidade'])
        if qtd is None: return
        preco_unitario = emp['preco_base'] * (1.07 ** (emp['quantidade'] - 1))
        total = preco_unitario * qtd
        emp['quantidade'] -= qtd
        self.saldo += total
        self.atualizar_tela()

    def avancar_mes(self):
        self.mes += 1
        eventos = self._verificar_eventos()
        lucro = sum(e['quantidade'] * e['lucro_unitario'] for e in self.empresas)
        self.saldo += lucro

        def show_lucro():
            self._mostrar_popup("Lucro do mês", f"Você recebeu R$ {lucro:,.2f}", "#2ECC71",
                                callback=self.atualizar_tela)

        if eventos:
            self._mostrar_popup("Eventos do mês", "\n".join(eventos), "#3498DB", callback=show_lucro)
        else:
            show_lucro()

    def _verificar_eventos(self):
        lista = []
        for e in self.empresas:
            if random.random() < 0.2:
                if random.choice([True, False]):
                    e['preco_base'] *= 0.7;
                    e['risco'] = 'Alto'
                    lista.append(f"{e['nome']} teve queda de 30%! Risco ALTO agora.")
                else:
                    e['preco_base'] *= 1.25;
                    e['risco'] = 'Baixo'
                    lista.append(f"{e['nome']} teve alta de 25%! Risco BAIXO agora.")
        return lista

    def atualizar_tela(self):
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}")
        self.label_mes.configure(text=f"{self.mes}x")
        self.atualizar_lista_empresas()

    # --- MÉTODOS DE POPUP E TUTORIAL (DO CÓDIGO ANTIGO) ---
    def _mostrar_popup(self, titulo, mensagem, cor_cabecalho="#3498DB", callback=None):
        main_window = self.winfo_toplevel()
        popup = ctk.CTkToplevel(main_window)
        popup.transient(main_window)
        popup.overrideredirect(True)
        popup.grab_set()
        popup._popup_width, popup._popup_height = 600, 380
        self._position_popup(popup)
        cont = ctk.CTkFrame(popup, corner_radius=12, fg_color="white")
        cont.pack(fill="both", expand=True)
        cab = ctk.CTkFrame(cont, fg_color=cor_cabecalho, corner_radius=12)
        cab.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(cab, text=titulo, font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=12,
                                                                                            pady=10)
        body = ctk.CTkFrame(cont, corner_radius=12, fg_color="#F2F2F2")
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        ctk.CTkLabel(body, text=mensagem, font=("Arial", 11), text_color="#2C3E50", wraplength=260,
                     justify="left").pack(padx=10, pady=10)

        def fechar():
            if popup in self.active_popups:
                self.active_popups.remove(popup)
            popup.destroy()
            if callback: callback()

        btn = ctk.CTkButton(cont, text="OK", fg_color=cor_cabecalho, text_color="white", font=("Arial", 11, "bold"),
                            corner_radius=8, command=fechar, width=80, height=30)
        btn.pack(pady=(0, 10))
        popup.bind("<Escape>", lambda e: fechar())
        popup.lift()
        self.active_popups.append(popup)

    def _position_popup(self, popup):
        main_window = self.winfo_toplevel()
        if not main_window.winfo_viewable(): return  # Evita erro ao fechar a janela
        rx, ry = main_window.winfo_rootx(), main_window.winfo_rooty()
        rw, rh = main_window.winfo_width(), main_window.winfo_height()
        pw, ph = popup._popup_width, popup._popup_height
        x = rx + (rw - pw) // 2
        y = ry + (rh - ph) // 2
        popup.geometry(f"{pw}x{ph}+{x}+{y}")

    def _on_main_move(self, event=None):
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
        popup._popup_width, popup._popup_height = 320, 240
        self._position_popup(popup)
        cont = ctk.CTkFrame(popup, corner_radius=20, fg_color="#2E0068")
        cont.pack(fill="both", expand=True)
        cab = ctk.CTkFrame(cont, fg_color="#6A1B9A", corner_radius=20)
        cab.pack(fill="x", pady=2, padx=2)
        ctk.CTkLabel(cab, text="📘 Tutorial", font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=12,
                                                                                                  pady=10)
        body = ctk.CTkFrame(cont, fg_color="#2E0068", corner_radius=12)
        body.pack(fill="both", expand=True, padx=12, pady=(8, 12))
        ctk.CTkLabel(body, text=(
            "Invista em empresas, acumule lucros mensais e reaja a eventos de mercado.\n\n"
            "• Clique em 'Comprar' ou 'Vender'.\n"
            "• Avance o tempo para receber lucros.\n"
            "• Cuidado com o risco!"
        ), font=("Arial", 11), text_color="white", justify="left", wraplength=296).pack(padx=10, pady=10)

        def fechar_tutorial():
            if popup in self.active_popups:
                self.active_popups.remove(popup)
            popup.destroy()

        btn = ctk.CTkButton(cont, text="Entendi", fg_color="#6A1B9A", hover_color="#4A0072", text_color="white",
                            font=("Arial", 11, "bold"), corner_radius=12, command=fechar_tutorial, width=100,
                            height=32).pack(pady=(0, 12))
        popup.bind("<Escape>", lambda e: fechar_tutorial())
        popup.lift()
        self.active_popups.append(popup)


# --- CLASSE PRINCIPAL DA APLICAÇÃO (PARA TESTE) ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Ações")
        self.geometry("1024x600")

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Imports locais para evitar erro de inicialização
        from view.tela_inicial import telaInicialFrame
        from view.tela_dict import telaDictFrame

        for F in (JogoGUI, telaInicialFrame, telaDictFrame):
            frame = F(master=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(JogoGUI)
        # Bind do evento de mover janela aqui, depois que o frame já existe
        self.bind("<Configure>", self.on_window_move)

    def mostrar_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()

    def on_window_move(self, event):
        frame_jogo = self.frames.get(JogoGUI)
        if frame_jogo and frame_jogo.winfo_ismapped():
            frame_jogo._on_main_move(event)


if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Pasta 'images' criada. Por favor, adicione os ícones nela.")


    # --- Mocks para tornar o arquivo executável e testável ---
    class MockTela(ctk.CTkFrame):
        def __init__(self, master, controller):
            super().__init__(master, fg_color=COLOR_BACKGROUND)
            label = ctk.CTkLabel(self, text=f"Tela de {self.__class__.__name__}", font=("Arial", 30))
            label.pack(pady=100)
            ctk.CTkButton(self, text="Voltar para o Jogo", command=lambda: controller.mostrar_frame(JogoGUI)).pack()


    class telaInicialFrame(MockTela):
        pass


    class telaDictFrame(MockTela):
        pass


    class View:
        pass


    view = View()
    view.tela_inicial = type("tela_inicial", (), {"telaInicialFrame": telaInicialFrame})
    view.tela_dict = type("tela_dict", (), {"telaDictFrame": telaDictFrame})

    import sys

    sys.modules['view'] = view
    sys.modules['view.tela_inicial'] = view.tela_inicial
    sys.modules['view.tela_dict'] = view.tela_dict

    app = App()
    app.mainloop()