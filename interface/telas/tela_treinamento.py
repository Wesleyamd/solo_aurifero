import customtkinter as ctk
from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_resultado import CardResultado


class TelaTreinamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.cabecalho = Cabecalho(
            self,
            "Treinar Modelo",
            "Nesta área ficará o treinamento do modelo de classificação."
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        self.card_info = CardResultado(
            self,
            "Treinamento ainda não implementado",
            "No futuro, esta tela permitirá carregar dataset, iniciar treinamento e acompanhar métricas do modelo."
        )
        self.card_info.pack(fill="x", pady=(0, 20))