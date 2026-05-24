import customtkinter as ctk
from tkinter import messagebox

from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_historico import CardHistorico
from interface.tema.cores import Cores
from persistencia.repository.analise_repository import AnaliseRepository


class TelaHistorico(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.criar_layout()
        self.carregar_historico()

    def criar_layout(self):
        self.cabecalho = Cabecalho(
            self,
            "Histórico de Análises",
            "Visualize, abra e exclua análises salvas."
        )
        self.cabecalho.pack(fill="x", pady=(0, 18))

        self.criar_topo_resumo()

        self.area_lista = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.area_lista.pack(fill="both", expand=True)

    def criar_topo_resumo(self):
        self.frame_resumo = ctk.CTkFrame(
            self,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=18,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.frame_resumo.pack(fill="x", pady=(0, 18))

        self.label_total = ctk.CTkLabel(
            self.frame_resumo,
            text="0 análises registradas",
            font=("Arial", 16, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.label_total.pack(side="left", padx=20, pady=16)

        self.label_info = ctk.CTkLabel(
            self.frame_resumo,
            text="Histórico local do sistema",
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_info.pack(side="right", padx=20, pady=16)

    def carregar_historico(self):
        self.limpar_lista()

        registros = AnaliseRepository.listar_todas()
        total = len(registros)

        self.atualizar_total(total)

        if not registros:
            self.criar_estado_vazio()
            return

        for registro in registros:
            analise_id, nome_analise, caminho_imagem, resultado, data_analise = registro

            card = CardHistorico(
                self.area_lista,
                analise_id,
                nome_analise,
                caminho_imagem,
                resultado,
                data_analise,
                self.excluir_analise
            )
            card.pack(fill="x", pady=8, padx=5)

    def limpar_lista(self):
        for widget in self.area_lista.winfo_children():
            widget.destroy()

    def atualizar_total(self, total):
        self.label_total.configure(
            text=f"{total} análise{'s' if total != 1 else ''} registrada{'s' if total != 1 else ''}"
        )

    def criar_estado_vazio(self):
        vazio = ctk.CTkFrame(
            self.area_lista,
            corner_radius=22,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )
        vazio.pack(fill="both", expand=True, padx=5, pady=15)

        icone = ctk.CTkLabel(
            vazio,
            text="📂",
            font=("Arial", 46)
        )
        icone.pack(pady=(40, 10))

        titulo = ctk.CTkLabel(
            vazio,
            text="Nenhuma análise salva",
            font=("Arial", 22, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        titulo.pack(pady=(0, 8))

        texto = ctk.CTkLabel(
            vazio,
            text="As imagens analisadas aparecerão aqui automaticamente.",
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        texto.pack(pady=(0, 40))

    def excluir_analise(self, analise_id):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir esta análise?"
        )

        if not confirmar:
            return

        AnaliseRepository.excluir(analise_id)
        self.carregar_historico()