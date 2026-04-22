import customtkinter as ctk
from interface.tema.cores import Cores


class Cabecalho(ctk.CTkFrame):
    def __init__(self, master, titulo, subtitulo):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 28, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self,
            text=subtitulo,
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.subtitulo.pack(anchor="w", pady=(4, 0))