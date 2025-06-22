import customtkinter as ctk
from tkinter import simpledialog
import random
from PIL import Image
import os # Import the os module for path manipulation

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
    {"nome": "Orbit Capital",     "icone": "orbitcapital.png",   "risco": "Médio", "quantidade": 0, "preco_base": 2.50, "lucro_unitario": 0.80},
    {"nome": "Nexora Group",      "icone": "nexoragroup.png",    "risco": "Baixo",  "quantidade": 0, "preco_base": 2.80, "lucro_unitario": 0.60},
    {"nome": "Skyline Dynamics",  "icone": "skylinedynamics.png","risco": "Alto",   "quantidade": 0, "preco_base": 1.80, "lucro_unitario": 1.20},
    {"nome": "Stratos Edge",      "icone": "stratosedge.png",    "risco": "Alto",   "quantidade": 0, "preco_base": 1.90, "lucro_unitario": 1.10},
    {"nome": "Veltrix Corp",      "icone": "veltrixcorp.png",    "risco": "Alto",   "quantidade": 0, "preco_base": 1.50, "lucro_unitario": 0.90},
    {"nome": "Greenline",         "icone": "greenline.png",      "risco": "Baixo",  "quantidade": 0, "preco_base": 2.30, "lucro_unitario": 0.50},
    {"nome": "Broadpeak",         "icone": "broadpeak.png",      "risco": "Médio",  "quantidade": 0, "preco_base": 2.60, "lucro_unitario": 0.75},
    {"nome": "Solidity",          "icone": "solidity.png",       "risco": "Alto",   "quantidade": 0, "preco_base": 1.60, "lucro_unitario": 1.30},
    {"nome": "Greenpoint",        "icone": "greenpoint.png",     "risco": "Médio",  "quantidade": 0, "preco_base": 2.00, "lucro_unitario": 0.90},
    {"nome": "Lucrative",         "icone": "lucrative.png",      "risco": "Baixo",  "quantidade": 0, "preco_base": 2.90, "lucro_unitario": 0.65},
]

# Guardar dados originais para reset
for emp in empresas:
    emp['preco_base_original'] = emp['preco_base']
    emp['risco_original']     = emp['risco']

class JogoGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Ações")
        self.geometry("360x700")
        self.configure(fg_color="#2E0068")

        self.saldo         = SALDO_INICIAL
        self.mes           = 1
        self.empresas      = empresas
        self.logo_images   = []
        self.active_popups = []

        # Define the path to your images folder
        self.image_path = os.path.join(os.path.dirname(__file__), "images")

        self.bind("<Configure>", self._on_main_move)
        self._criar_header()
        self._criar_frame_empresas()
        self._criar_footer()
        self.atualizar_lista_empresas()

        # Mostrar tutorial após inicializar
        self.after(500, self._mostrar_tutorial)

    def _criar_header(self):
        topo = ctk.CTkFrame(self, fg_color="#2E0068")
        topo.pack(fill="x", padx=20, pady=10)

        # Botão Home
        try:
            # Join the image path with the filename
            img = Image.open(os.path.join(self.image_path, "home.png"))
            self.home_image = ctk.CTkImage(img, size=(50,50))
        except FileNotFoundError:
            print(f"Warning: home.png not found at {os.path.join(self.image_path, 'home.png')}. Using default.")
            self.home_image = None # Or load a default image/text
        ctk.CTkButton(
            topo,
            image=self.home_image,
            text="",
            fg_color="transparent",
            hover_color="#4A0072",
            width=36,
            height=36,
            corner_radius=18,
            command=self._voltar_home
        ).pack(side="left", padx=(0,10))

        # Label Saldo
        saldo_frame = ctk.CTkFrame(topo, fg_color="#2E0068")
        saldo_frame.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(saldo_frame, text="Saldo", font=("Arial",10), text_color="white").pack(anchor="w")
        self.label_saldo = ctk.CTkLabel(
            saldo_frame,
            text=f"R$ {self.saldo:,.2f}".replace(",","."),
            font=("Arial",18,"bold"),
            text_color="white"
        )
        self.label_saldo.pack(anchor="w")

        # Label Meses
        mes_frame = ctk.CTkFrame(topo, fg_color="#2E0068")
        mes_frame.pack(side="right")
        ctk.CTkLabel(mes_frame, text="Meses", font=("Arial",10), text_color="white").pack()
        self.label_mes = ctk.CTkLabel(
            mes_frame,
            text=f"{self.mes}x",
            font=("Arial",14),
            fg_color="#D9D9D9",
            text_color="black",
            corner_radius=14,
            width=60,
            height=28
        )
        self.label_mes.pack()

    def _voltar_home(self):
        # Resetar estado inicial
        self.saldo = SALDO_INICIAL
        self.mes   = 1
        for emp in self.empresas:
            emp['quantidade']   = 0
            emp['preco_base']   = emp['preco_base_original']
            emp['risco']        = emp['risco_original']
        self.atualizar_tela()

    def _criar_frame_empresas(self):
        container = ctk.CTkFrame(self, fg_color="#2E0068")
        container.pack(fill="both", expand=True, pady=(0,10))
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
        estilo_btn = {"font":("Arial",12,"bold"), "width":120, "height":40, "corner_radius":12}
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
            font=("Arial",9,"bold"),
            corner_radius=6,
            height=20,
            width=80
        ).pack(pady=(8,4))

        content = ctk.CTkFrame(card, fg_color="white")
        content.pack(fill="x", padx=10, pady=(0,10))

        # Logo e quantidade
        logo_f = ctk.CTkFrame(content, fg_color="transparent")
        logo_f.pack(side="left", padx=5, fill="y")
        try:
            # Join the image path with the filename
            img = ctk.CTkImage(Image.open(os.path.join(self.image_path, empresa['icone'])), size=(64,64))
            self.logo_images.append(img)
            ctk.CTkLabel(logo_f, image=img, text="").pack(side="left", pady=5)
        except FileNotFoundError:
            print(f"Warning: {empresa['icone']} not found at {os.path.join(self.image_path, empresa['icone'])}. Using default.")
            ctk.CTkLabel(logo_f, text="📈", font=("Arial",30), text_color="black").pack(side="left", pady=5)
        ctk.CTkLabel(
            logo_f,
            text=f"{empresa['quantidade']}",
            fg_color="#4B2E83",
            text_color="white",
            font=("Arial",12,"bold"),
            width=40,
            height=40,
            corner_radius=20
        ).pack(side="left", padx=(6,0), pady=5)

        # Info nome e custo
        info_f = ctk.CTkFrame(content, fg_color="transparent")
        info_f.pack(side="left", padx=5, fill="both", expand=True)
        ctk.CTkLabel(info_f, text=empresa['nome'], font=("Arial",13,"bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(
            info_f,
            text=f"Custo: R$ {preco:,.2f}".replace(",","."),
            font=("Arial",9),
            text_color="black"
        ).pack(anchor="w", pady=(4,0))

        # Botões Comprar/Vender e lucro
        right_f = ctk.CTkFrame(content, fg_color="transparent")
        right_f.pack(side="right", padx=5, fill="y")
        ctk.CTkLabel(
            right_f,
            text=f"+ R$ {empresa['quantidade']*empresa['lucro_unitario']:,.2f}".replace(",","."),
            font=("Arial",12,"bold"),
            text_color="#2ECC71"
        ).pack(anchor="e")
        ctk.CTkButton(
            right_f,
            text="Comprar",
            font=("Arial",10,"bold"),
            fg_color="#27AE60",
            hover_color="#219653",
            command=lambda i=index: self.comprar(i)
        ).pack(fill="x", pady=(4,4))
        ctk.CTkButton(
            right_f,
            text="Vender",
            font=("Arial",10,"bold"),
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
            self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",","."))
        else:
            self._mostrar_popup("Saldo insuficiente", f"Você precisa de R$ {preco:,.2f}".replace(",","."),
                                "#E74C3C")

    def vender(self, index):
        emp = self.empresas[index]
        if emp['quantidade'] == 0:
            return self._mostrar_popup("Sem ações", "Você não possui ações dessa empresa.", "#E74C3C")
        qtd = simpledialog.askinteger("Vender ações",
                                      f"Quantas ações de {emp['nome']} quer vender?",
                                      minvalue=1, maxvalue=emp['quantidade'])
        if qtd is None:
            return
        total = self.calcular_preco(emp) * qtd
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
                                f"Você recebeu R$ {lucro:,.2f}".replace(",","."),
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
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",","."))
        self.label_mes.configure(text=f"{self.mes}x")
        self.atualizar_lista_empresas()

    def _mostrar_popup(self, titulo, mensagem, cor_cabecalho="#3498DB", callback=None):
        popup = ctk.CTkToplevel(self)
        popup.transient(self)
        popup.overrideredirect(True)
        popup.grab_set()

        is_special = titulo in ("Eventos do mês", "Lucro do mês")
        popup._popup_width = 320 if is_special else 300
        popup._popup_height= 200 if is_special else 180
        self._position_popup(popup)

        cont = ctk.CTkFrame(popup,
                           corner_radius=20 if is_special else 12,
                           fg_color="#2E0068" if is_special else "white")
        cont.pack(fill="both", expand=True)

        cab = ctk.CTkFrame(cont,
                          fg_color="#4B2E83" if is_special else cor_cabecalho,
                          corner_radius=20 if is_special else 12)
        cab.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(cab, text=titulo, font=("Arial",14,"bold"), text_color="white").pack(side="left", padx=12, pady=10)
        if titulo == "Eventos do mês":
            ctk.CTkLabel(cab, text="⌄", font=("Arial",14,"bold"), text_color="white").pack(side="right", padx=12, pady=10)

        body = ctk.CTkFrame(cont,
                           corner_radius=12,
                           fg_color="#2E0068" if is_special else "#F2F2F2")
        body.pack(fill="both", expand=True, padx=12, pady=(8,12) if is_special else (0,10))
        ctk.CTkLabel(body,
                     text=mensagem,
                     font=("Arial",11),
                     text_color="white" if is_special else "#2C3E50",
                     wraplength=296 if is_special else 260,
                     justify="left").pack(padx=10, pady=10)

        def fechar():
            popup.destroy()
            if callback: callback()

        btn = ctk.CTkButton(cont,
                            text="OK",
                            fg_color="#4B2E83" if is_special else cor_cabecalho,
                            hover_color="#3B1E6F" if is_special else None,
                            text_color="white",
                            font=("Arial",11,"bold"),
                            corner_radius=12 if is_special else 8,
                            command=fechar,
                            width=80,
                            height=32 if is_special else 30)
        btn.pack(pady=(0,12) if is_special else (0,10))

        popup.bind("<Escape>", lambda e: fechar())
        popup.lift()
        popup.attributes("-topmost", True)
        popup.after_idle(popup.attributes, "-topmost", False)
        self.active_popups.append(popup)

    def _position_popup(self, popup):
        rx, ry = self.winfo_rootx(), self.winfo_rooty()
        rw, rh = self.winfo_width(), self.winfo_height()
        pw, ph = popup._popup_width, popup._popup_height
        x = rx + (rw - pw)//2
        y = ry + (rh - ph)//2
        popup.geometry(f"{pw}x{ph}+{x}+{y}")

    def _on_main_move(self, event):
        for p in list(self.active_popups):
            if p.winfo_exists():
                self._position_popup(p)
            else:
                self.active_popups.remove(p)

    def _mostrar_tutorial(self):
        popup = ctk.CTkToplevel(self)
        popup.transient(self)
        popup.overrideredirect(True)
        popup.grab_set()
        popup._popup_width = 320
        popup._popup_height= 240
        self._position_popup(popup)

        cont = ctk.CTkFrame(popup, corner_radius=20, fg_color="#2E0068")
        cont.pack(fill="both", expand=True)

        cab = ctk.CTkFrame(cont, fg_color="#6A1B9A", corner_radius=20)
        cab.pack(fill="x")
        ctk.CTkLabel(cab, text="📘 Tutorial", font=("Arial",14,"bold"), text_color="white").pack(side="left", padx=12, pady=10)

        body = ctk.CTkFrame(cont, fg_color="#2E0068", corner_radius=12)
        body.pack(fill="both", expand=True, padx=12, pady=(8,12))
        ctk.CTkLabel(body,
                     text=(
                         "Invista em empresas, acumule lucros mensais e reaja a eventos de mercado.\n\n"
                         "• Clique em 'Comprar' ou 'Vender'.\n"
                         "• Avance o tempo para receber lucros.\n"
                         "• Cuidado com o risco!"
                     ),
                     font=("Arial",11),
                     text_color="white",
                     justify="left",
                     wraplength=296).pack(padx=10, pady=10)

        def fechar_tutorial():
            popup.destroy()

        ctk.CTkButton(cont,
                      text="Entendi",
                      fg_color="#6A1B9A",
                      hover_color="#4A0072",
                      text_color="white",
                      font=("Arial",11,"bold"),
                      corner_radius=12,
                      command=fechar_tutorial,
                      width=100,
                      height=32).pack(pady=(0,12))

        popup.bind("<Escape>", lambda e: fechar_tutorial())
        popup.lift()
        popup.attributes("-topmost", True)
        popup.after_idle(popup.attributes, "-topmost", False)
        self.active_popups.append(popup)

if __name__ == "__main__":
    app = JogoGUI()
    app.mainloop()
