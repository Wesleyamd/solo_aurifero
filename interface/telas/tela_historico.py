import customtkinter as ctk
from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_resultado import CardResultado


class TelaHistorico(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.cabecalho = Cabecalho(
            self,
            "Histórico de Análises",
            "Aqui serão exibidas as análises salvas no sistema."
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        self.card_info = CardResultado(
            self,
            "Nenhum histórico disponível",
            "As análises realizadas futuramente poderão ser salvas em banco de dados e exibidas nesta tela."
        )
        self.card_info.pack(fill="x", pady=(0, 20))