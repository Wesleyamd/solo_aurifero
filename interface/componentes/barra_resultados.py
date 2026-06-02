import customtkinter as ctk

from interface.tema.cores import Cores


class BarraResultados(ctk.CTkFrame):
    def __init__(
        self,
        master,
        modelos,
        variavel_modelo,
        comando_alternar_modelo,
        comando_trocar_secao
    ):
        super().__init__(
            master,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=16,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.comando_trocar_secao = comando_trocar_secao

        self.seletor_modelo = ctk.CTkOptionMenu(
            self,
            values=list(modelos),
            variable=variavel_modelo,
            command=comando_alternar_modelo,
            width=135,
            height=30,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            dropdown_font=("Arial", 12),
            fg_color=Cores.FUNDO_SECUNDARIO,
            button_color=Cores.DOURADO,
            button_hover_color=Cores.DOURADO_CLARO,
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.seletor_modelo.pack(side="left", padx=(6, 4), pady=5)

        self.btn_resultado_modelo = ctk.CTkButton(
            self,
            text="📊 Resultado por Modelo",
            width=190,
            height=30,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=lambda: self.comando_trocar_secao("modelo")
        )
        self.btn_resultado_modelo.pack(side="left", padx=4, pady=5)

        self.btn_comparacao = ctk.CTkButton(
            self,
            text="📈 Comparação entre Modelos",
            width=215,
            height=30,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=lambda: self.comando_trocar_secao("comparacao")
        )
        self.btn_comparacao.pack(side="left", padx=(4, 6), pady=5)

        self.atualizar_estado("modelo")

    def atualizar_estado(self, secao):
        ativo_fg = Cores.DOURADO
        ativo_texto = "#0B1117"
        inativo_fg = Cores.FUNDO_SECUNDARIO
        inativo_texto = Cores.TEXTO_PRINCIPAL

        if secao == "modelo":
            self.btn_resultado_modelo.configure(
                fg_color=ativo_fg,
                hover_color=Cores.DOURADO_CLARO,
                text_color=ativo_texto
            )
            self.btn_comparacao.configure(
                fg_color=inativo_fg,
                hover_color=Cores.FUNDO_HOVER,
                text_color=inativo_texto
            )
        else:
            self.btn_resultado_modelo.configure(
                fg_color=inativo_fg,
                hover_color=Cores.FUNDO_HOVER,
                text_color=inativo_texto
            )
            self.btn_comparacao.configure(
                fg_color=ativo_fg,
                hover_color=Cores.DOURADO_CLARO,
                text_color=ativo_texto
            )
