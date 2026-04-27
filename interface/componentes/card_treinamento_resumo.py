import customtkinter as ctk

from interface.tema.cores import Cores


class CardTreinamentoResumo(ctk.CTkFrame):
    def __init__(self, master, titulo, valor="0"):
        super().__init__(
            master,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=18,
            border_width=1,
            border_color=Cores.BORDA,
            height=90
        )

        self.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_titulo.pack(anchor="w", padx=16, pady=(14, 4))

        self.label_valor = ctk.CTkLabel(
            self,
            text=valor,
            font=("Arial", 24, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.label_valor.pack(anchor="w", padx=16)

    def atualizar_valor(self, valor):
        self.label_valor.configure(text=str(valor))