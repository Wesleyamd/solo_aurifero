import customtkinter as ctk
from interface.tema.cores import Cores


class BarraLateral(ctk.CTkFrame):
    def __init__(self, master, callback_mudar_tela):
        super().__init__(
            master,
            width=240,
            corner_radius=0,
            fg_color=Cores.FUNDO_SIDEBAR
        )
        self.pack_propagate(False)

        self.callback_mudar_tela = callback_mudar_tela
        self.botoes = {}

        self.logo = ctk.CTkLabel(
            self,
            text="⛏ Solo Aurífero",
            font=("Arial", 24, "bold"),
            text_color=Cores.DESTAQUE
        )
        self.logo.pack(pady=(30, 8), padx=20, anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self,
            text="Sistema de análise de imagens de solo",
            font=("Arial", 10),
            text_color=Cores.TEXTO_SECUNDARIO,
            justify="left"
        )
        self.subtitulo.pack(padx=20, pady=(0, 30), anchor="w")

        self.criar_botao("analise", "Analisar Solo")
        self.criar_botao("historico", "Histórico de Análises")
        self.criar_botao("treinamento", "Treinar Modelo")

    def criar_botao(self, chave, texto):
        botao = ctk.CTkButton(
            self,
            text=texto,
            height=44,
            corner_radius=12,
            fg_color="transparent",
            hover_color=Cores.FUNDO_HOVER,
            text_color=Cores.TEXTO_PRINCIPAL,
            anchor="w",
            command=lambda: self.ao_clicar(chave)
        )
        botao.pack(fill="x", padx=16, pady=6)
        self.botoes[chave] = botao

    def ao_clicar(self, chave):
        self.destacar_botao(chave)
        self.callback_mudar_tela(chave)

    def destacar_botao(self, chave_ativo):
        for chave, botao in self.botoes.items():
            if chave == chave_ativo:
                botao.configure(
                    fg_color=Cores.DESTAQUE,
                    text_color="#111111"
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    text_color=Cores.TEXTO_PRINCIPAL
                )