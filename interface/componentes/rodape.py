import customtkinter as ctk
from interface.tema.cores import Cores


class Rodape(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=Cores.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Cores.BORDA,
            height=70
        )

        self.grid_propagate(False)

        ctk.CTkLabel(
            self,
            text=" ",
            font=("Segoe UI", 16, "italic"),
            text_color=Cores.TEXTO
        ).place(relx=0.5, rely=0.5, anchor="center")