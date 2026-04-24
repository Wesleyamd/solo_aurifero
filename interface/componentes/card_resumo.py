import customtkinter as ctk
from interface.tema.cores import Cores


class CardResumo(ctk.CTkFrame):
    def __init__(self, master, titulo, valor):
        super().__init__(
            master,
            corner_radius=16,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.titulo.pack(anchor="w", padx=15, pady=(10, 2))

        self.valor = ctk.CTkLabel(
            self,
            text=valor,
            font=("Arial", 20, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.valor.pack(anchor="w", padx=15, pady=(0, 10))

    def atualizar_valor(self, novo_valor):
        self.valor.configure(text=novo_valor)