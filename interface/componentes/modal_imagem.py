import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from interface.tema.cores import Cores


class ModalImagem:
    def __init__(self, master, caminho_imagem):
        self.master = master
        self.caminho_imagem = caminho_imagem
        self.imagem_modal = None
        self.janela = None

    def abrir(self):
        try:
            self.janela = ctk.CTkToplevel(self.master)
            self.janela.title("Visualizar Imagem")
            self.janela.geometry("1050x720")
            self.janela.transient(self.master)
            self.janela.grab_set()

            frame = ctk.CTkFrame(
                self.janela,
                fg_color=Cores.FUNDO_APP
            )
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            topo = ctk.CTkFrame(frame, fg_color="transparent")
            topo.pack(fill="x", pady=(5, 15))

            titulo = ctk.CTkLabel(
                topo,
                text=os.path.basename(self.caminho_imagem),
                font=("Arial", 22, "bold"),
                text_color=Cores.TEXTO_PRINCIPAL
            )
            titulo.pack(side="left")

            btn_fechar = ctk.CTkButton(
                topo,
                text="Fechar",
                width=100,
                height=34,
                corner_radius=12,
                fg_color="#2c3e50",
                hover_color="#34495e",
                command=self.janela.destroy
            )
            btn_fechar.pack(side="right")

            frame_img = ctk.CTkFrame(
                frame,
                fg_color=Cores.FUNDO_CARD,
                corner_radius=20,
                border_width=1,
                border_color=Cores.BORDA
            )
            frame_img.pack(fill="both", expand=True)

            imagem = Image.open(self.caminho_imagem)
            imagem.thumbnail((950, 570))

            self.imagem_modal = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )

            label = ctk.CTkLabel(
                frame_img,
                text="",
                image=self.imagem_modal
            )
            label.pack(expand=True, padx=20, pady=20)

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir a imagem.\n\n{erro}"
            )