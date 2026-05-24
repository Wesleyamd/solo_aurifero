import os
import customtkinter as ctk

from interface.tema.cores import Cores
from interface.componentes.card_status import CardStatus
from persistencia.repository.analise_repository import AnaliseRepository
from persistencia.repository.treinamento_repository import TreinamentoRepository
from utils.caminhos import DATASET_POTENCIAL_DIR, DATASET_NAO_AURIFERO_DIR


class GridStatus(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        total_analises = AnaliseRepository.contar()
        percentual_potencial = AnaliseRepository.percentual_potencial()
        total_dataset = self.contar_dataset()
        modelo_status = "Treinado" if TreinamentoRepository.modelo_treinado() else "Não treinado"

        cards = [
            ("🖼", str(total_analises), "Análises", "Total", Cores.DOURADO),
            ("📈", percentual_potencial, "Potencial", "Resultados", Cores.VERDE),
            ("🗄", str(total_dataset), "Banco", "Imagens", Cores.AZUL),
            ("🧠", modelo_status, "Modelo", "Status", Cores.ROXO),
        ]

        for i, dados in enumerate(cards):
            card = CardStatus(self, *dados)
            card.grid(row=0, column=i, padx=8, sticky="ew")

    def contar_dataset(self):
        total = 0

        for pasta in [DATASET_POTENCIAL_DIR, DATASET_NAO_AURIFERO_DIR]:
            if pasta.exists():
                total += len([
                    arq for arq in os.listdir(pasta)
                    if arq.lower().endswith((".jpg", ".jpeg", ".png"))
                ])

        return total
