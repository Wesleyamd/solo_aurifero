import customtkinter as ctk
from interface.tema.cores import Cores


class CardResultado(ctk.CTkFrame):
    def __init__(self, master, titulo, descricao):
        super().__init__(
            master,
            corner_radius=18,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo.pack(anchor="w", padx=20, pady=(18, 6))

        self.descricao = ctk.CTkLabel(
            self,
            text=descricao,
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO,
            justify="left",
            wraplength=700
        )
        self.descricao.pack(anchor="w", padx=20, pady=(0, 18))