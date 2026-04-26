import customtkinter as ctk

from interface.tema.cores import Cores
from interface.componentes.card_status import CardStatus

class GridStatus(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        cards = [
            ("🖼", "128", "Análises", "Total", Cores.DOURADO),
            ("📈", "88%", "Potencial", "Resultados", Cores.VERDE),
            ("🗄", "342", "Banco", "Imagens", Cores.AZUL),
            ("🧠", "Treinado", "Modelo", "Status", Cores.ROXO),
        ]

        for i, dados in enumerate(cards):
            card = CardStatus(self, *dados)
            card.grid(row=0, column=i, padx=8, sticky="ew")