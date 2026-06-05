import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from interface.tema.cores import Cores
from controller.analise_controller import AnaliseController


class SeletorImagem(ctk.CTkFrame):
    def __init__(self, master, combo_modelo):
        super().__init__(master, fg_color="transparent")

        self.combo_modelo = combo_modelo

        self.caminho_original = None
        self.caminho_copia = None
        self.imagem_ctk = None

        self.criar_layout()

    def criar_layout(self):
        # Card principal
        self.card = ctk.CTkFrame(
            self,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=20,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card.pack(fill="both", expand=True)

        # Topo
        self.topo = ctk.CTkFrame(self.card, fg_color="transparent")
        self.topo.pack(fill="x", padx=20, pady=(18, 10))

        self.titulo = ctk.CTkLabel(
            self.topo,
            text="Imagem do Solo",
            font=("Arial", 22, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo.pack(side="left")

        self.status = ctk.CTkLabel(
            self.topo,
            text="Pronto para análise",
            font=("Arial", 13),
            text_color="#55ff99"
        )
        self.status.pack(side="right")

        # Nome da análise
        self.entry_nome = ctk.CTkEntry(
            self.card,
            placeholder_text="Digite um nome para a análise. Ex.: Solo área norte",
            height=42,
            font=("Arial", 14),
            fg_color=Cores.FUNDO_APP,
            border_color=Cores.BORDA,
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.entry_nome.pack(fill="x", padx=20, pady=(0, 15))

        # Botões
        self.frame_botoes = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.frame_botoes.pack(fill="x", padx=20, pady=(0, 15))

        self.botao_selecionar = ctk.CTkButton(
            self.frame_botoes,
            text="📁 Selecionar Imagem",
            command=self.carregar_imagem,
            width=220,
            height=44,
            font=("Arial", 14, "bold"),
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            corner_radius=12
        )
        self.botao_selecionar.pack(side="left")

        self.botao_analisar = ctk.CTkButton(
            self.frame_botoes,
            text="🚀 Analisar Solo",
            command=self.analisar_imagem,
            width=220,
            height=44,
            font=("Arial", 14, "bold"),
            fg_color="#2c3e50",
            hover_color="#34495e",
            text_color="white",
            corner_radius=12,
            state="disabled"
        )
        self.botao_analisar.pack(side="right")

        # Área imagem
        self.frame_imagem = ctk.CTkFrame(
            self.card,
            fg_color=Cores.FUNDO_APP,
            corner_radius=18,
            border_width=1,
            border_color=Cores.BORDA
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
            font=("Arial", 16),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_imagem.pack(expand=True)

        # Resultado
        self.label_resultado = ctk.CTkLabel(
            self.card,
            text="Aguardando análise...",
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_resultado.pack(pady=(5, 20))

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

        largura_max = 850
        altura_max = 480
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

        self.status.configure(
            text="Imagem carregada",
            text_color="#55ff99"
        )

        self.label_resultado.configure(
            text="Clique em Analisar Solo.",
            text_color=Cores.TEXTO_SECUNDARIO
        )

        self.botao_analisar.configure(
            state="normal",
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111"
        )

    def analisar_imagem(self):
        if not self.caminho_original:
            return

        nome_analise = self.entry_nome.get().strip()

        if not nome_analise:
            messagebox.showwarning(
                "Nome da análise",
                "Informe um nome para identificar esta análise."
            )
            self.entry_nome.focus()
            return

        self.label_resultado.configure(
            text="Analisando solo...",
            text_color="#ffaa00"
        )

        self.update()

        try:
            modelo = self.combo_modelo.get()

            dados = AnaliseController.analisar(
                nome_analise,
                self.caminho_original,
                modelo
            )
        except Exception as erro:
            self.label_resultado.configure(
                text="Não foi possível concluir a análise.",
                text_color="#f87171"
            )
            self.status.configure(
                text="Erro na análise",
                text_color="#f87171"
            )
            messagebox.showerror("Erro na análise", str(erro))
            return

        self.caminho_copia = dados["caminho_copia"]
        resultado = dados["resultado"]
        cor = "#4ade80" if dados["tem_potencial"] else "#f87171"

        self.label_resultado.configure(
            text=resultado,
            text_color=cor
        )

        self.status.configure(
            text="Análise concluída",
            text_color="#55ff99"
        )

        self.atualizar_tela_pai()

    def atualizar_tela_pai(self):
        widget = self.master

        while widget is not None:
            if hasattr(widget, "atualizar_cards"):
                widget.atualizar_cards()
                return

            widget = getattr(widget, "master", None)
