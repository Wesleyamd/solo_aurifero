import customtkinter as ctk
from interface.tema.cores import Cores


class CardStatus(ctk.CTkFrame):
    def __init__(self, master, icone, valor, titulo, subtitulo, cor):
        super().__init__(
            master,
            fg_color=Cores.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Cores.BORDA,
            height=115
        )

        self.grid_propagate(False)

        icone_box = ctk.CTkFrame(
            self,
            width=70,
            height=70,
            fg_color="#1B2430",
            corner_radius=16
        )
        icone_box.pack(side="left", padx=18, pady=20)
        icone_box.pack_propagate(False)

        ctk.CTkLabel(
            icone_box,
            text=icone,
            font=("Segoe UI", 30),
            text_color=cor
        ).place(relx=0.5, rely=0.5, anchor="center")

        textos = ctk.CTkFrame(self, fg_color="transparent")
        textos.pack(side="left", fill="both", expand=True, pady=18)

        ctk.CTkLabel(
            textos,
            text=valor,
            font=("Segoe UI", 26, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text=titulo,
            font=("Segoe UI", 14, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos,
            text=subtitulo,
            font=("Segoe UI", 12),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(anchor="w", pady=(4, 0))