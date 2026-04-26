from repository.analise_repository import AnaliseRepository
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from interface.tema.cores import Cores
from service.analise_service import AnaliseService
from service.arquivo_service import ArquivoService


class SeletorImagem(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.caminho_original = None
        self.caminho_copia = None
        self.imagem_ctk = None

        # Card principal
        self.card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card.pack(fill="both", expand=True)

        # Título
        self.titulo = ctk.CTkLabel(
            self.card,
            text="Imagem do Solo",
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo.pack(anchor="w", padx=20, pady=(20, 5))

        # Área dos botões
        self.frame_botoes = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.frame_botoes.pack(fill="x", padx=20, pady=(10, 15))

        self.botao_selecionar = ctk.CTkButton(
            self.frame_botoes,
            text="Selecionar Imagem",
            command=self.carregar_imagem,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            height=40,
            corner_radius=10
        )
        self.botao_selecionar.pack(side="left")

        self.botao_analisar = ctk.CTkButton(
            self.frame_botoes,
            text="Analisar Solo",
            command=self.analisar_imagem,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            height=45,
            corner_radius=12,
            font=("Arial", 14, "bold"),
            state="disabled"
        )
        self.botao_analisar.pack(side="right")

        # Área da imagem
        self.frame_imagem = ctk.CTkFrame(
            self.card,
            fg_color=Cores.FUNDO_APP,
            corner_radius=16
        )
        self.frame_imagem.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        self.label_imagem = ctk.CTkLabel(
            self.frame_imagem,
            text="Nenhuma imagem selecionada",
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_imagem.pack(expand=True)

        # Resultado
        self.label_resultado = ctk.CTkLabel(
            self.card,
            text="Aguardando análise...",
            font=("Arial", 16, "bold"),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_resultado.pack(pady=(0, 20))

    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem do solo",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        self.caminho_original = caminho

        imagem = Image.open(caminho)

        largura_max = 800
        altura_max = 450
        imagem.thumbnail((largura_max, altura_max))

        self.imagem_ctk = ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=imagem.size
        )

        self.label_imagem.configure(
            image=self.imagem_ctk,
            text=""
        )

        self.label_resultado.configure(
            text="Imagem carregada. Clique em Analisar Solo.",
            text_color=Cores.TEXTO_SECUNDARIO
        )

        self.botao_analisar.configure(
            state="normal",
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER
        )

    def analisar_imagem(self):
        if not self.caminho_original:
            self.label_resultado.configure(
                text="Selecione uma imagem primeiro.",
                text_color="#c94f4f"
            )
            return

        self.caminho_copia = ArquivoService.salvar_copia_imagem(
            self.caminho_original
        )

        resultado = AnaliseService.analisar_cor(self.caminho_copia)

        AnaliseRepository.salvar(
            self.caminho_copia,
            resultado
        )

        if "Possível" in resultado:
            cor = "#c7a34b"
        else:
            cor = "#c94f4f"

        self.label_resultado.configure(
            text=resultado,
            text_color=cor
        )

        # Atualiza os cards da TelaAnalise automaticamente
        if hasattr(self.master, "atualizar_cards"):
            self.master.atualizar_cards()