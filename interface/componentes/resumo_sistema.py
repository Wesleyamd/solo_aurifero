import customtkinter as ctk
from interface.tema.cores import Cores


class ResumoSistema(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=Cores.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.criar_titulo()
        self.criar_itens()

    def criar_titulo(self):
        ctk.CTkLabel(
            self,
            text="Resumo do Sistema",
            font=("Segoe UI", 16, "bold"),
            text_color=Cores.DOURADO
        ).pack(anchor="w", padx=22, pady=(18, 14))

    def criar_itens(self):
        itens = [
            ("🛡", "Modelo de IA", "Rede Neural Convolucional (CNN)", "Ativo", Cores.VERDE),
            ("📁", "Base de Dados", "SQLite Local", "Conectado", Cores.VERDE),
            ("🖼", "Conjunto de Dados", "2 classes • 342 imagens", "Carregado", Cores.TEXTO_SECUNDARIO),
            ("📅", "Último Treinamento", "10/05/2025 • 18:45", "Atualizado", Cores.AZUL),
        ]

        for item in itens:
            self.item_resumo(*item)

    def item_resumo(self, icone, titulo, subtitulo, status, cor):
        linha = ctk.CTkFrame(
            self,
            fg_color=Cores.FUNDO_SECUNDARIO,
            corner_radius=12
        )
        linha.pack(fill="x", padx=22, pady=6)

        ctk.CTkLabel(
            linha,
            text=icone,
            width=54,
            height=54,
            font=("Segoe UI", 24),
            text_color=Cores.DOURADO
        ).pack(side="left", padx=10, pady=8)

        textos = ctk.CTkFrame(linha, fg_color="transparent")
        textos.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            textos,
            text=titulo,
            font=("Segoe UI", 14, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w", pady=(8, 0))

        ctk.CTkLabel(
            textos,
            text=subtitulo,
            font=("Segoe UI", 12),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            linha,
            text=status,
            width=86,
            height=26,
            corner_radius=8,
            fg_color="#1B2430",
            text_color=cor,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right", padx=14)