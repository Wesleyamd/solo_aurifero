import customtkinter as ctk
from interface.tema.cores import Cores


class BarraLateral(ctk.CTkFrame):
    def __init__(self, master, callback_mudar_tela):
        super().__init__(
            master,
            width=260,
            corner_radius=0,
            fg_color=Cores.FUNDO_SIDEBAR
        )
        self.pack_propagate(False)

        self.callback_mudar_tela = callback_mudar_tela
        self.botoes = {}

        self.criar_logo()
        self.criar_menu()
        self.criar_rodape()

    def criar_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=22, pady=(30, 28))

        ctk.CTkLabel(
            logo_frame,
            text="⛏",
            width=48,
            height=48,
            corner_radius=14,
            fg_color="#1B2430",
            text_color=Cores.DOURADO,
            font=("Segoe UI", 26, "bold")
        ).pack(side="left")

        textos = ctk.CTkFrame(logo_frame, fg_color="transparent")
        textos.pack(side="left", padx=12)

        ctk.CTkLabel(
            textos,
            text="SOLO",
            font=("Segoe UI", 20, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text="AURÍFERO",
            font=("Segoe UI", 13, "bold"),
            text_color=Cores.DOURADO
        ).pack(anchor="w")

    def criar_menu(self):
        ctk.CTkLabel(
            self,
            text="MENU PRINCIPAL",
            font=("Segoe UI", 11, "bold"),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(anchor="w", padx=24, pady=(0, 12))

        self.criar_botao("inicio", "🏠  Início")
        self.criar_botao("analise", "🖼  Analisar Solo")
        self.criar_botao("historico", "📋  Histórico")
        self.criar_botao("treinamento", "🧠  Treinar Modelo")
        self.criar_botao("resultados", "📊  Resultados")

    def criar_botao(self, chave, texto):
        botao = ctk.CTkButton(
            self,
            text=texto,
            height=48,
            corner_radius=12,
            fg_color="transparent",
            hover_color=Cores.CARD_HOVER,
            text_color=Cores.TEXTO_SECUNDARIO,
            anchor="w",
            cursor="hand2",
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.ao_clicar(chave)
        )
        botao.pack(fill="x", padx=16, pady=5)

        self.botoes[chave] = botao

    def criar_rodape(self):
        rodape = ctk.CTkFrame(
            self,
            fg_color=Cores.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Cores.BORDA
        )
        rodape.pack(side="bottom", fill="x", padx=16, pady=20)

        ctk.CTkLabel(
            rodape,
            text="Status do Sistema",
            font=("Segoe UI", 13, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w", padx=14, pady=(14, 4))

        ctk.CTkLabel(
            rodape,
            text="● Banco conectado\n● IA pronta para análise",
            font=("Segoe UI", 12),
            text_color=Cores.VERDE,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 14))

    def ao_clicar(self, chave):
        self.callback_mudar_tela(chave)

    def destacar_botao(self, chave_ativo):
        for chave, botao in self.botoes.items():
            if chave == chave_ativo:
                botao.configure(
                    fg_color=Cores.DOURADO,
                    text_color=Cores.TEXTO_ESCURO,
                    hover_color=Cores.DOURADO_CLARO
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    text_color=Cores.TEXTO_SECUNDARIO,
                    hover_color=Cores.CARD_HOVER
                )