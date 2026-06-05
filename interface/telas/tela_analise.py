import customtkinter as ctk

from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_resumo import CardResumo
from interface.componentes.seletor_imagem import SeletorImagem
from controller.analise_controller import AnaliseController


class TelaAnalise(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.combo_modelo = None

        self.criar_layout()
        self.atualizar_cards()

    def criar_layout(self):
        # Container principal
        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.container.pack(fill="both", expand=True, padx=0, pady=0)

        # Cabeçalho
        self.cabecalho = Cabecalho(
            self.container,
            "Analisar Solo",
            "Selecione uma imagem do solo para realizar a análise inteligente."
        )
        self.cabecalho.pack(fill="x", pady=(0, 22))

        # Cards de resumo
        self.frame_cards = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.frame_cards.pack(fill="x", pady=(0, 22))

        self.card1 = CardResumo(
            self.frame_cards,
            "Análises realizadas",
            "0"
        )
        self.card1.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.card2 = CardResumo(
            self.frame_cards,
            "Modelo utilizado",
            "EfficientNetB0"
        )
        self.card2.pack(side="left", expand=True, fill="x", padx=6)

        self.card3 = CardResumo(
            self.frame_cards,
            "Último resultado",
            "-"
        )
        self.card3.pack(side="left", expand=True, fill="x", padx=(6, 0))

        # Card principal da análise
        self.frame_analise = ctk.CTkFrame(
            self.container,
            fg_color="#111922",
            corner_radius=18,
            border_width=1,
            border_color="#233241"
        )
        self.frame_analise.pack(fill="both", expand=True)

        # Título da seção
        self.frame_topo = ctk.CTkFrame(
            self.frame_analise,
            fg_color="transparent"
        )
        self.frame_topo.pack(fill="x", padx=20, pady=(18, 8))

        self.titulo = ctk.CTkLabel(
            self.frame_topo,
            text="Imagem do Solo",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F8FAFC"
        )
        self.titulo.pack(side="left")

        self.status = ctk.CTkLabel(
            self.frame_topo,
            text="Aguardando imagem",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#94A3B8"
        )
        self.status.pack(side="right")

        self.combo_modelo = ctk.CTkComboBox(
            self.frame_topo,
            values=["EfficientNetB0", "MobileNetV2"],
            width=170,
            command=lambda _: self.atualizar_modelo_card()
        )
        self.combo_modelo.set("EfficientNetB0")
        self.combo_modelo.pack(side="right", padx=(0, 10))

        # Seletor de imagem
        # O seletor recebe o ComboBox para conseguir enviar o modelo selecionado
        # para o AnaliseController no momento da classificação.
        self.seletor = SeletorImagem(
            self.frame_analise,
            self.combo_modelo
        )
        self.seletor.pack(fill="both", expand=True, padx=20, pady=(8, 20))

    def atualizar_modelo_card(self):
        if self.combo_modelo:
            self.card2.atualizar_valor(self.combo_modelo.get())

    def atualizar_cards(self):
        total = AnaliseController.total_analises()
        ultimo = AnaliseController.ultimo_resultado()

        if not ultimo:
            ultimo = "-"

        self.card1.atualizar_valor(str(total))
        self.atualizar_modelo_card()
        self.card3.atualizar_valor(ultimo)
