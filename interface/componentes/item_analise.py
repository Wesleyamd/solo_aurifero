import customtkinter as ctk
from interface.tema.cores import Cores


class ItemAnalise(ctk.CTkFrame):
    def __init__(self, master, nome, data, porcentagem, resultado, cor):
        super().__init__(
            master,
            fg_color=Cores.FUNDO_SECUNDARIO,
            corner_radius=12,
            border_width=1,
            border_color=Cores.BORDA
        )

        thumb = ctk.CTkFrame(
            self,
            width=64,
            height=58,
            fg_color="#6B573A",
            corner_radius=8
        )
        thumb.pack(side="left", padx=10, pady=8)
        thumb.pack_propagate(False)

        ctk.CTkLabel(
            thumb,
            text="🪨",
            font=("Segoe UI", 24)
        ).place(relx=0.5, rely=0.5, anchor="center")

        textos = ctk.CTkFrame(self, fg_color="transparent")
        textos.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            textos,
            text=nome,
            font=("Segoe UI", 14, "bold"),
            text_color=Cores.TEXTO
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkLabel(
            textos,
            text=data,
            font=("Segoe UI", 12),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(anchor="w", pady=(4, 0))

        status = ctk.CTkFrame(self, fg_color="transparent")
        status.pack(side="right", padx=14)

        ctk.CTkLabel(
            status,
            text=porcentagem,
            width=70,
            height=26,
            corner_radius=8,
            fg_color=cor,
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="e")

        ctk.CTkLabel(
            status,
            text=resultado,
            font=("Segoe UI", 12, "bold"),
            text_color=cor
        ).pack(anchor="e", pady=(6, 0))