import customtkinter as ctk
from tkinter import simpledialog
import random
from PIL import Image

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

empresas = [
    {
        "nome": "Orbit Capital",
        "icone": "orbitcapital.png",
        "risco": "Médio",
        "quantidade": 0,
        "preco_base": 2.50,
        "lucro_unitario": 0.80
    },
    {
        "nome": "Nexora Group",
        "icone": "nexoragroup.png",
        "risco": "Baixo",
        "quantidade": 0,
        "preco_base": 2.80,
        "lucro_unitario": 0.60
    },
    {
        "nome": "Skyline Dynamics",
        "icone": "skylinedynamics.png",
        "risco": "Alto",
        "quantidade": 0,
        "preco_base": 1.80,
        "lucro_unitario": 1.20
    },
    {
        "nome": "Stratos Edge",
        "icone": "stratosedge.png",
        "risco": "Alto",
        "quantidade": 0,
        "preco_base": 1.90,
        "lucro_unitario": 1.10
    },
    {
        "nome": "Veltrix Corp",
        "icone": "veltrixcorp.png",
        "risco": "Alto",
        "quantidade": 0,
        "preco_base": 1.50,
        "lucro_unitario": 0.90
    },
    {
        "nome": "Greenline",
        "icone": "greenline.png",
        "risco": "Baixo",
        "quantidade": 0,
        "preco_base": 2.30,
        "lucro_unitario": 0.50
    },
    {
        "nome": "Broadpeak",
        "icone": "broadpeak.png",
        "risco": "Médio",
        "quantidade": 0,
        "preco_base": 2.60,
        "lucro_unitario": 0.75
    },
    {
        "nome": "Solidity",
        "icone": "solidity.png",
        "risco": "Alto",
        "quantidade": 0,
        "preco_base": 1.60,
        "lucro_unitario": 1.30
    },
    {
        "nome": "Greenpoint",
        "icone": "greenpoint.png",
        "risco": "Médio",
        "quantidade": 0,
        "preco_base": 2.00,
        "lucro_unitario": 0.90
    },
    {
        "nome": "Lucrative",
        "icone": "lucrative.png",
        "risco": "Baixo",
        "quantidade": 0,
        "preco_base": 2.90,
        "lucro_unitario": 0.65
    }
]

class JogoGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Ações")
        self.geometry("360x700")
        self.configure(fg_color="#2E0068")

        self.saldo = SALDO_INICIAL
        self.mes = 1
        self.empresas = empresas
        self.logo_images = []
        self.active_popups = []

        self.bind("<Configure>", self._on_main_move)
        self._criar_header()
        self._criar_frame_empresas()
        self._criar_footer()
        self.atualizar_lista_empresas()

    def _criar_header(self):
        topo = ctk.CTkFrame(self, fg_color="#2E0068")
        topo.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(topo, text="👤", text_color="white", font=("Arial", 28)).pack(side="left", padx=(0, 10))

        saldo_frame = ctk.CTkFrame(topo, fg_color="#2E0068")
        saldo_frame.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(saldo_frame, text="Saldo", font=("Arial", 10), text_color="white").pack(anchor="w")
        self.label_saldo = ctk.CTkLabel(
            saldo_frame,
            text=f"R$ {self.saldo:,.2f}".replace(",", "."),
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        self.label_saldo.pack(anchor="w")

        mes_frame = ctk.CTkFrame(topo, fg_color="#2E0068")
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
            rodape, text="🔘 Parar", fg_color="white", text_color="black",
            hover_color="#DDDDDD", command=self.quit, **estilo_btn
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            rodape, text="⮕ Avançar", fg_color="white", text_color="black",
            hover_color="#DDDDDD", command=self.avancar_mes, **estilo_btn
        ).pack(side="right", padx=15)

    def atualizar_lista_empresas(self):
        for child in self.canvas_empresas.winfo_children():
            child.destroy()
        self.logo_images.clear()
        for i, empresa in enumerate(self.empresas):
            preco_atual = self.calcular_preco(empresa)
            self._criar_card_empresa(i, empresa, preco_atual)

    def _criar_card_empresa(self, index, empresa, preco):
        card = ctk.CTkFrame(self.canvas_empresas, fg_color="white", corner_radius=20)
        card.pack(pady=10, padx=10, fill="x")

        cor_risco = CORES_RISCO.get(empresa["risco"], "gray")
        ctk.CTkLabel(
            card,
            text=f"{empresa['risco']} risco",
            fg_color=cor_risco,
            text_color="white",
            font=("Arial", 9, "bold"),
            corner_radius=6,
            height=20,
            width=80
        ).pack(pady=(8, 4))

        content_frame = ctk.CTkFrame(card, fg_color="white")
        content_frame.pack(fill="x", padx=10, pady=(0, 10))

        frame_logo = ctk.CTkFrame(content_frame, fg_color="transparent")
        frame_logo.pack(side="left", padx=5, fill="y")
        try:
            img = ctk.CTkImage(Image.open(empresa["icone"]), size=(64, 64))
            self.logo_images.append(img)
            ctk.CTkLabel(frame_logo, image=img, text="").pack(side="left", padx=(0, 6), pady=5)
        except Exception:
            ctk.CTkLabel(frame_logo, text="📈", font=("Arial", 30), text_color="black").pack(side="left", padx=(0, 6), pady=5)

        ctk.CTkLabel(
            frame_logo,
            text=f"{empresa['quantidade']}",
            width=40,
            height=40,
            fg_color="#4B2E83",
            text_color="white",
            font=("Arial", 12, "bold"),
            corner_radius=20
        ).pack(side="left", pady=5)

        frame_info = ctk.CTkFrame(content_frame, fg_color="transparent")
        frame_info.pack(side="left", padx=5, fill="both", expand=True)
        ctk.CTkLabel(
            frame_info, text=empresa["nome"], font=("Arial", 13, "bold"),
            text_color="black", anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            frame_info,
            text=f"Custo: R$ {preco:,.2f}".replace(",", "."),
            font=("Arial", 9),
            text_color="black",
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))

        frame_direito = ctk.CTkFrame(content_frame, fg_color="transparent")
        frame_direito.pack(side="right", padx=5, fill="y")
        ctk.CTkLabel(
            frame_direito,
            text=f"+ R$ {empresa['quantidade'] * empresa['lucro_unitario']:,.2f}".replace(",", "."),
            font=("Arial", 12, "bold"),
            text_color="#2ECC71",
            anchor="e"
        ).pack(anchor="e")

        ctk.CTkButton(
            frame_direito,
            text="Comprar",
            font=("Arial", 10, "bold"),
            fg_color="#27AE60",
            text_color="white",
            hover_color="#219653",
            corner_radius=8,
            command=lambda i=index: self.comprar(i)
        ).pack(fill="x", pady=(4, 4))

        ctk.CTkButton(
            frame_direito,
            text="Vender",
            font=("Arial", 10, "bold"),
            fg_color="#F1C40F",
            text_color="black",
            hover_color="#F39C12",
            corner_radius=8,
            command=lambda i=index: self.vender(i)
        ).pack(fill="x")

    def calcular_preco(self, empresa):
        return empresa["preco_base"] * (1.07 ** empresa["quantidade"])

    def comprar(self, index):
        emp = self.empresas[index]
        preco = self.calcular_preco(emp)
        if self.saldo >= preco:
            self.saldo -= preco
            emp["quantidade"] += 1
            self.atualizar_lista_empresas()
            self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))
        else:
            self._mostrar_popup(
                titulo="Saldo insuficiente",
                mensagem=f"Você precisa de R$ {preco:,.2f} para comprar.".replace(",", "."),
                cor_cabecalho="#E74C3C"
            )

    def vender(self, index):
        emp = self.empresas[index]
        if emp["quantidade"] == 0:
            self._mostrar_popup(
                titulo="Sem ações",
                mensagem="Você não possui ações dessa empresa.",
                cor_cabecalho="#E74C3C"
            )
            return

        qtd = simpledialog.askinteger(
            "Vender ações",
            f"Quantas ações de {emp['nome']} você quer vender?",
            minvalue=1,
            maxvalue=emp["quantidade"]
        )
        if qtd is None:
            return

        valor_unit = self.calcular_preco(emp)
        valor_tot = valor_unit * qtd
        emp["quantidade"] -= qtd
        self.saldo += valor_tot
        self.atualizar_lista_empresas()
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))

    def avancar_mes(self):
        self.mes += 1
        eventos = self._verificar_eventos()
        lucro = sum(emp["quantidade"] * emp["lucro_unitario"] for emp in self.empresas)
        self.saldo += lucro

        def mostrar_lucro():
            self._mostrar_popup(
                titulo="Lucro do mês",
                mensagem=f"Você recebeu R$ {lucro:,.2f} neste mês.".replace(",", "."),
                cor_cabecalho="#2ECC71",
                callback=self.atualizar_tela
            )

        if eventos:
            texto = "\n".join(eventos)
            self._mostrar_popup(
                titulo="Eventos do mês",
                mensagem=texto,
                cor_cabecalho="#3498DB",
                callback=mostrar_lucro
            )
        else:
            mostrar_lucro()

    def _verificar_eventos(self):
        lista = []
        for emp in self.empresas:
            if random.random() < 0.20:
                tipo = random.choice(["positivo", "negativo"])
                if tipo == "negativo":
                    emp["preco_base"] *= 0.70
                    emp["risco"] = "Alto"
                    lista.append(f"{emp['nome']} teve queda de 30%! Risco ALTO agora.")
                else:
                    emp["preco_base"] *= 1.25
                    emp["risco"] = "Baixo"
                    lista.append(f"{emp['nome']} teve alta de 25%! Risco BAIXO agora.")
        return lista

    def atualizar_tela(self):
        self.label_saldo.configure(text=f"R$ {self.saldo:,.2f}".replace(",", "."))
        self.label_mes.configure(text=f"{self.mes}x")
        self.atualizar_lista_empresas()

    def _mostrar_popup(self, titulo, mensagem, cor_cabecalho="#3498DB", callback=None):
        # Popups especiais de Evento e Lucro do mês
        if titulo in ("Eventos do mês", "Lucro do mês"):
            popup = ctk.CTkToplevel(self)
            popup.transient(self)
            popup.overrideredirect(True)
            popup.grab_set()
            popup._popup_width = 320
            popup._popup_height = 200
            self._position_popup(popup)

            cont = ctk.CTkFrame(popup, corner_radius=20, fg_color="#2E0068", border_width=0)
            cont.pack(fill="both", expand=True)

            cab = ctk.CTkFrame(cont, fg_color="#4B2E83", corner_radius=20)
            cab.pack(fill="x")
            ctk.CTkLabel(
                cab, text=titulo, font=("Arial", 14, "bold"),
                text_color="white"
            ).pack(side="left", padx=12, pady=10)
            if titulo == "Eventos do mês":
                ctk.CTkLabel(
                    cab, text="⌄", font=("Arial", 14, "bold"),
                    text_color="white"
                ).pack(side="right", padx=12, pady=10)

            body = ctk.CTkFrame(cont, fg_color="#2E0068", corner_radius=12)
            body.pack(fill="both", expand=True, padx=12, pady=(8, 12))
            ctk.CTkLabel(
                body,
                text=mensagem,
                font=("Arial", 11),
                text_color="white",
                justify="left",
                wraplength=296
            ).pack(padx=10, pady=10)

            def fechar():
                if popup in self.active_popups:
                    self.active_popups.remove(popup)
                popup.destroy()
                if callback:
                    callback()

            ctk.CTkButton(
                cont,
                text="OK",
                fg_color="#4B2E83",
                hover_color="#3B1E6F",
                text_color="white",
                font=("Arial", 11, "bold"),
                corner_radius=12,
                command=fechar,
                width=80,
                height=32
            ).pack(pady=(0, 12))

            popup.bind("<Escape>", lambda e: fechar())
            popup.lift()
            popup.attributes("-topmost", True)
            popup.after_idle(popup.attributes, "-topmost", False)
            self.active_popups.append(popup)
            return

        # Popup padrão
        popup = ctk.CTkToplevel(self)
        popup.transient(self)
        popup.overrideredirect(True)
        popup.grab_set()
        popup._popup_width = 300
        popup._popup_height = 180
        self._position_popup(popup)

        cont = ctk.CTkFrame(popup, corner_radius=12, fg_color="white")
        cont.pack(fill="both", expand=True)

        cab = ctk.CTkFrame(cont, fg_color=cor_cabecalho, corner_radius=12)
        cab.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(cab, text=titulo, font=("Arial", 14, "bold"), text_color="white").pack(padx=10, pady=8)

        body = ctk.CTkFrame(cont, fg_color="#F2F2F2", corner_radius=8)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        ctk.CTkLabel(body, text=mensagem, font=("Arial", 11), text_color="#2C3E50", justify="left", wraplength=260).pack(padx=10, pady=10)

        def fechar_padrao():
            if popup in self.active_popups:
                self.active_popups.remove(popup)
            popup.destroy()
            if callback:
                callback()

        ctk.CTkButton(
            cont,
            text="OK",
            fg_color=cor_cabecalho,
            text_color="white",
            font=("Arial", 11, "bold"),
            corner_radius=8,
            command=fechar_padrao,
            width=80,
            height=30
        ).pack(pady=(0, 10))

        popup.bind("<Escape>", lambda e: fechar_padrao())
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
        for popup in list(self.active_popups):
            if popup.winfo_exists():
                self._position_popup(popup)
            else:
                self.active_popups.remove(popup)

if __name__ == "__main__":
    app = JogoGUI()
    app.mainloop()
