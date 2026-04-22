import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from interface.tema.cores import Cores
from service.analise_service import AnaliseService


class SeletorImagem:
    def __init__(self, root):
        self.root = root
        self.imagem_ctk = None

        # Card principal
        self.card = ctk.CTkFrame(
            root,
            corner_radius=18,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        self.titulo = ctk.CTkLabel(
            self.card,
            text="Imagem do Solo",
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo.pack(anchor="w", padx=15, pady=(15, 5))

        # Botão
        self.botao = ctk.CTkButton(
            self.card,
            text="Selecionar Imagem",
            command=self.carregar_imagem,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111"
        )
        self.botao.pack(pady=10)

        # Label imagem
        self.label_imagem = ctk.CTkLabel(self.card, text="")
        self.label_imagem.pack(pady=10)

        # Resultado
        self.label_resultado = ctk.CTkLabel(
            self.card,
            text="Aguardando análise...",
            font=("Arial", 16, "bold")
        )
        self.label_resultado.pack(pady=10)

    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )

        if caminho:
            imagem = Image.open(caminho)

            largura_max = 800
            altura_max = 450

            # mantém proporção automaticamente
            imagem.thumbnail((largura_max, altura_max))

            self.imagem_ctk = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )

            self.label_imagem.configure(image=self.imagem_ctk)

            resultado = AnaliseService.analisar_cor(caminho)

            # 🎯 Badge de cor
            if "Possível" in resultado:
                cor = "#c7a34b"  # dourado
            else:
                cor = "#c94f4f"  # vermelho suave

            self.label_resultado.configure(
                text=resultado,
                text_color=cor
            )