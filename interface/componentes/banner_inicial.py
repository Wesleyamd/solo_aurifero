import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance

from interface.tema.cores import Cores


class BannerInicial(ctk.CTkFrame):
    def __init__(self, master, ao_clicar_analise=None):
        super().__init__(
            master,
            fg_color=Cores.CARD,
            corner_radius=18,
            border_width=1,
            border_color=Cores.BORDA,
            height=270
        )

        self.ao_clicar_analise = ao_clicar_analise
        self.img_banner = None
        self.grid_propagate(False)

        self.largura = 1100
        self.altura = 270
        self.raio = 22

        self.criar_banner()

    def criar_banner(self):
        self.canvas = tk.Canvas(
            self,
            width=self.largura,
            height=self.altura,
            highlightthickness=0,
            bd=0,
            bg=Cores.CARD
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.criar_imagem_fundo()
        self.criar_textos()
        self.criar_botao()

    def criar_imagem_fundo(self):
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        caminho_imagem = os.path.join(base_dir, "assets", "fundo.png")

        if not os.path.exists(caminho_imagem):
            self.canvas.create_text(
                self.largura // 2,
                self.altura // 2,
                text="Imagem não encontrada",
                fill=Cores.VERMELHO,
                font=("Segoe UI", 18, "bold")
            )
            return

        img = Image.open(caminho_imagem).resize((self.largura, self.altura)).convert("RGBA")

        # Leve escurecimento geral para dar contraste
        img_rgb = img.convert("RGB")
        img_rgb = ImageEnhance.Brightness(img_rgb).enhance(0.78)
        img = img_rgb.convert("RGBA")

        # Degradê escuro lateral premium
        overlay = Image.new("RGBA", (self.largura, self.altura), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)

        for x in range(self.largura):
            alpha = int(50 * (1 - (x / self.largura) ** 1.8))
            draw_overlay.line((x, 0, x, self.altura), fill=(0, 0, 0, alpha))

        img = Image.alpha_composite(img, overlay)

        # Máscara arredondada
        mask = Image.new("L", (self.largura, self.altura), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle(
            (0, 0, self.largura, self.altura),
            radius=self.raio,
            fill=255
        )

        img.putalpha(mask)

        self.img_banner = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.img_banner, anchor="nw")

    def criar_textos(self):
        titulo = "Sistema de Análise\nde Solo Com Potencial Aurífero"

        # sombra suave
        self.canvas.create_text(
            60,
            52,
            text=titulo,
            fill="#000000",
            font=("Segoe UI", 34, "bold"),
            anchor="nw"
        )

        self.canvas.create_text(
            58,
            50,
            text=titulo,
            fill="#FFFFFF",
            font=("Segoe UI", 34, "bold"),
            anchor="nw"
        )


    def criar_botao(self):
        botao = ctk.CTkButton(
            self,
            text="▶  Iniciar Nova Análise",
            width=260,
            height=48,
            corner_radius=12,
            fg_color=Cores.DOURADO,
            hover_color=Cores.DOURADO_CLARO,
            text_color=Cores.TEXTO_ESCURO,
            font=("Segoe UI", 16, "bold"),
            command=self.abrir_analise
        )
        botao.place(x=58, y=178)

    def abrir_analise(self):
        if self.ao_clicar_analise:
            self.ao_clicar_analise()