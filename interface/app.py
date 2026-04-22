import customtkinter as ctk
from interface.janela_principal import JanelaPrincipal


class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Solo Aurífero")
        self.root.geometry("1280x720")
        self.root.minsize(1000, 650)

        self.janela = JanelaPrincipal(self.root)

    def run(self):
        self.root.mainloop()