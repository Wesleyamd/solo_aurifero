import customtkinter as ctk

from interface.componentes.barra_lateral import BarraLateral
from interface.telas.tela_inicial import TelaInicial
from interface.telas.tela_analise import TelaAnalise
from interface.telas.tela_historico import TelaHistorico
from interface.telas.tela_treinamento import TelaTreinamento
from interface.tema.cores import Cores


class JanelaPrincipal:
    def __init__(self, root):
        self.root = root

        self.root.title("Solo Aurífero")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 950)
        self.root.configure(fg_color=Cores.FUNDO)

        self.frame_principal = ctk.CTkFrame(
            root,
            fg_color=Cores.FUNDO,
            corner_radius=0
        )
        self.frame_principal.pack(fill="both", expand=True)

        self.barra_lateral = BarraLateral(
            self.frame_principal,
            self.mostrar_tela
        )
        self.barra_lateral.pack(side="left", fill="y")

        self.area_conteudo = ctk.CTkFrame(
            self.frame_principal,
            fg_color=Cores.FUNDO,
            corner_radius=0
        )
        self.area_conteudo.pack(side="right", fill="both", expand=True)

        self.tela_atual = None

        self.mostrar_tela("inicio")

    def limpar_area_conteudo(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    def mostrar_tela(self, nome_tela):
        self.limpar_area_conteudo()

        if nome_tela == "inicio":
            self.tela_atual = TelaInicial(
                self.area_conteudo,
                self.mostrar_tela
            )

        elif nome_tela == "analise":
            self.tela_atual = TelaAnalise(self.area_conteudo)

        elif nome_tela == "historico":
            self.tela_atual = TelaHistorico(self.area_conteudo)

        elif nome_tela == "treinamento":
            self.tela_atual = TelaTreinamento(self.area_conteudo)

        else:
            return

        self.tela_atual.pack(
            fill="both",
            expand=True
        )

        self.barra_lateral.destacar_botao(nome_tela)