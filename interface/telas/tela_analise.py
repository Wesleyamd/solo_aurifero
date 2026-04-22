import customtkinter as ctk
from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_resumo import CardResumo
from interface.componentes.seletor_imagem import SeletorImagem


class TelaAnalise(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Cabeçalho
        self.cabecalho = Cabecalho(
            self,
            "Analisar Solo",
            "Selecione uma imagem para análise do solo"
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        #  Cards de resumo
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=(0, 20))

        self.card1 = CardResumo(self.frame_cards, "Análises", "0")
        self.card1.pack(side="left", expand=True, fill="x", padx=5)

        self.card2 = CardResumo(self.frame_cards, "Modelo", "Não treinado")
        self.card2.pack(side="left", expand=True, fill="x", padx=5)

        self.card3 = CardResumo(self.frame_cards, "Último resultado", "-")
        self.card3.pack(side="left", expand=True, fill="x", padx=5)

        #  Área da imagem
        self.seletor = SeletorImagem(self)