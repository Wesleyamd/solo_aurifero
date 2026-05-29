import customtkinter as ctk
import re

from interface.tema.cores import Cores
from interface.componentes.item_analise import ItemAnalise
from persistencia.repository.analise_repository import AnaliseRepository


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

        ctk.CTkLabel(
            topo,
            text="Dados do SQLite",
            font=("Segoe UI", 12, "bold"),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(side="right")

    def criar_lista(self):
        registros = AnaliseRepository.listar_ultimas(3)

        if not registros:
            ctk.CTkLabel(
                self,
                text="Nenhuma análise registrada ainda.",
                font=("Segoe UI", 13),
                text_color=Cores.TEXTO_SECUNDARIO
            ).pack(anchor="w", padx=22, pady=(8, 22))
            return

        for analise_id, nome_analise, caminho_imagem, resultado, data_analise in registros:
            nome = nome_analise or "Análise sem nome"
            data = str(data_analise)

            possui_potencial = AnaliseRepository.eh_resultado_com_potencial(resultado)

            match = re.search(r"Confiança:\s*([\d.]+)", resultado)

            if match:
                confianca = float(match.group(1))
                porcentagem = f"{confianca:.0f}%"
            else:
                porcentagem = "--"

            cor = Cores.VERDE if possui_potencial else Cores.VERMELHO

            linha = ItemAnalise(
                self,
                nome,
                data,
                porcentagem,
                resultado,
                cor,
                caminho_imagem
            )

            linha.pack(fill="x", padx=22, pady=6)
