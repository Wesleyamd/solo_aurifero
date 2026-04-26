import customtkinter as ctk

from interface.tema.cores import Cores
from interface.componentes.item_analise import ItemAnalise


class ListaAnalises(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=Cores.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.criar_cabecalho()
        self.criar_lista()

    def criar_cabecalho(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=22, pady=(18, 10))

        ctk.CTkLabel(
            topo,
            text="Últimas Análises",
            font=("Segoe UI", 16, "bold"),
            text_color=Cores.DOURADO
        ).pack(side="left")

        ctk.CTkButton(
            topo,
            text="Ver todas",
            width=80,
            height=28,
            fg_color="#1B2430",
            hover_color=Cores.CARD_HOVER,
            text_color=Cores.DOURADO,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right")

    def criar_lista(self):
        dados = [
            ("solo_0045.jpg", "15/05/2026 • 14:32", "82.4%", "Potencial Aurífero", Cores.VERDE),
            ("solo_0044.jpg", "15/05/2026 • 13:58", "18.7%", "Sem Potencial", Cores.VERMELHO),
            ("solo_0043.jpg", "15/05/2026 • 13:21", "76.1%", "Potencial Aurífero", Cores.VERDE),
        ]

        for item in dados:
            linha = ItemAnalise(self, *item)
            linha.pack(fill="x", padx=22, pady=6)