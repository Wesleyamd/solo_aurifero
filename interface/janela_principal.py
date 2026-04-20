import customtkinter as ctk


class JanelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solo Aurífero")
        self.geometry("1024x754")

        label = ctk.CTkLabel(self, text="Sistema de Análise de Solo com Wesley Carvalho")
        label.pack(pady=20)