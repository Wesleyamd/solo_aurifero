import customtkinter as ctk

from interface.tema.cores import Cores


class PainelTreinamento(ctk.CTkFrame):
    def __init__(
        self,
        master,
        ao_adicionar_potencial,
        ao_adicionar_nao,
        ao_atualizar,
        ao_treinar
    ):
        super().__init__(master, fg_color="transparent")

        self.ao_adicionar_potencial = ao_adicionar_potencial
        self.ao_adicionar_nao = ao_adicionar_nao
        self.ao_atualizar = ao_atualizar
        self.ao_treinar = ao_treinar

        self.criar_layout()

    def criar_layout(self):
        self.card_status = ctk.CTkFrame(
            self,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=20,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card_status.pack(fill="x", pady=(0, 20))

        self.label_titulo = ctk.CTkLabel(
            self.card_status,
            text="Painel de Treinamento",
            font=("Arial", 22, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.label_titulo.pack(anchor="w", padx=20, pady=(18, 10))

        self.label_status = ctk.CTkLabel(
            self.card_status,
            text="Modelo não treinado",
            font=("Arial", 16, "bold"),
            text_color="#ff6666"
        )
        self.label_status.pack(anchor="w", padx=20)

        self.label_info = ctk.CTkLabel(
            self.card_status,
            text="Adicione imagens nas duas classes para treinar.",
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_info.pack(anchor="w", padx=20, pady=(5, 12))

        self.frame_modelo = ctk.CTkFrame(
            self.card_status,
            fg_color="transparent"
        )
        self.frame_modelo.pack(fill="x", padx=20, pady=(0, 15))

        self.label_modelo = ctk.CTkLabel(
            self.frame_modelo,
            text="Modelo de IA:",
            font=("Arial", 13, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.label_modelo.pack(side="left", padx=(0, 10))

        self.modelo_var = ctk.StringVar(value="EfficientNetB0")
        self.combo_modelo = ctk.CTkComboBox(
            self.frame_modelo,
            values=["EfficientNetB0", "MobileNetV2"],
            variable=self.modelo_var,
            width=180,
            height=34,
            corner_radius=10,
            state="readonly",
            command=lambda _valor: self.ao_atualizar()
        )
        self.combo_modelo.pack(side="left")

        self.barra = ctk.CTkProgressBar(
            self.card_status,
            height=14,
            corner_radius=12,
            progress_color=Cores.DESTAQUE
        )
        self.barra.pack(fill="x", padx=20, pady=(0, 20))
        self.barra.set(0)

        self.criar_card_acoes()

    def criar_card_acoes(self):
        self.card_acoes = ctk.CTkFrame(
            self,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=20,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card_acoes.pack(fill="x", pady=(0, 10))

        self.titulo_acoes = ctk.CTkLabel(
            self.card_acoes,
            text="Ações do Dataset",
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo_acoes.pack(anchor="w", padx=20, pady=(16, 8))

        self.frame_acoes = ctk.CTkFrame(
            self.card_acoes,
            fg_color="transparent",
            height=60
        )
        self.frame_acoes.pack(fill="x", padx=20, pady=(0, 18))
        self.frame_acoes.pack_propagate(False)

        self.frame_esquerda = ctk.CTkFrame(
            self.frame_acoes,
            fg_color="transparent"
        )
        self.frame_esquerda.pack(side="left")

        self.frame_direita = ctk.CTkFrame(
            self.frame_acoes,
            fg_color="transparent"
        )
        self.frame_direita.pack(side="right")

        self.btn_add_potencial = ctk.CTkButton(
            self.frame_esquerda,
            text="📁 Adicionar Aurífero",
            width=170,
            height=44,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=self.ao_adicionar_potencial
        )
        self.btn_add_potencial.pack(side="left", padx=(0, 10), pady=8)

        self.btn_add_nao = ctk.CTkButton(
            self.frame_esquerda,
            text="📁 Adicionar Não Aurífero",
            width=190,
            height=44,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=self.ao_adicionar_nao
        )
        self.btn_add_nao.pack(side="left", pady=8)

        self.btn_atualizar = ctk.CTkButton(
            self.frame_direita,
            text="Atualizar",
            width=130,
            height=44,
            corner_radius=12,
            command=self.ao_atualizar
        )
        self.btn_atualizar.pack(side="left", padx=(0, 10), pady=8)

        self.btn_treinar = ctk.CTkButton(
            self.frame_direita,
            text="🤖 Treinar Modelo",
            width=190,
            height=44,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            font=("Arial", 14, "bold"),
            command=self.ao_treinar
        )
        self.btn_treinar.pack(side="left", pady=8)

    def obter_modelo_selecionado(self):
        return self.modelo_var.get()

    def atualizar_status_modelo(self, treinado):
        if treinado:
            self.label_status.configure(
                text="Modelo treinado",
                text_color="#55ff99"
            )
            self.barra.set(1)
        else:
            self.label_status.configure(
                text="Modelo não treinado",
                text_color="#ff6666"
            )
            self.barra.set(0)

    def iniciar_treinamento(self):
        self.label_status.configure(
            text="Treinando modelo...",
            text_color="#ffaa00"
        )
        self.barra.set(0.35)

    def progresso(self, valor):
        self.barra.set(valor)

    def finalizar_treinamento(self):
        self.barra.set(1)
        self.label_status.configure(
            text="Treinamento concluído",
            text_color="#55ff99"
        )