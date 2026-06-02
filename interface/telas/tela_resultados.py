import json
import os

import customtkinter as ctk

from interface.componentes.cabecalho import Cabecalho
from interface.componentes.barra_resultados import BarraResultados
from interface.componentes.cards_resultados import (
    criar_cards_metricas,
    criar_cards_resumo_teste
)
from interface.componentes.comparacao_modelos import criar_aba_comparacao
from interface.componentes.graficos_resultados import criar_area_graficos
from interface.componentes.relatorio_classificacao import criar_relatorio_classificacao
from interface.tema.cores import Cores


class TelaResultados(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.modelos_config = {
            "EfficientNetB0": [
                os.path.join("persistencia", "data", "modelos", "efficientnetb0", "metricas.json"),
                os.path.join("persistencia", "data", "modelos", "EfficientNetB0", "metricas.json"),
                os.path.join("persistencia", "data", "modelos", "metricas_efficientnetb0.json"),
                os.path.join("persistencia", "data", "modelos", "metricas.json"),
            ],
            "MobileNetV2": [
                os.path.join("persistencia", "data", "modelos", "mobilenetv2", "metricas.json"),
                os.path.join("persistencia", "data", "modelos", "MobileNetV2", "metricas.json"),
                os.path.join("persistencia", "data", "modelos", "metricas_mobilenetv2.json"),
            ],
        }

        self.metricas_modelos = self.carregar_metricas_modelos()
        self.modelo_atual = ctk.StringVar(value=self.obter_primeiro_modelo_disponivel())
        self.metricas = self.metricas_modelos.get(self.modelo_atual.get())
        self.conteudo_modelo = None
        self.barra_resultados = None

        self.criar_layout()

    def carregar_json(self, caminho):
        if not os.path.exists(caminho):
            return None

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except Exception:
            return None

    def carregar_metricas_modelos(self):
        metricas_modelos = {}

        for nome_modelo, caminhos in self.modelos_config.items():
            for caminho in caminhos:
                dados = self.carregar_json(caminho)

                if dados:
                    dados["modelo"] = dados.get("modelo", nome_modelo)
                    dados["caminho_metricas"] = caminho
                    metricas_modelos[nome_modelo] = dados
                    break

        return metricas_modelos

    def obter_primeiro_modelo_disponivel(self):
        if self.metricas_modelos:
            return next(iter(self.metricas_modelos.keys()))
        return "EfficientNetB0"

    def criar_layout(self):
        cabecalho = Cabecalho(
            self,
            "Resultados dos Modelos",
            "Visualize os resultados individuais e compare o desempenho entre as arquiteturas treinadas."
        )
        cabecalho.pack(fill="x", pady=(0, 10))

        if not self.metricas_modelos:
            self.criar_mensagem_sem_resultados(self)
            return

        self.aba_atual = ctk.StringVar(value="modelo")

        self.barra_resultados = BarraResultados(
            self,
            modelos=self.modelos_config.keys(),
            variavel_modelo=self.modelo_atual,
            comando_alternar_modelo=self.alternar_modelo,
            comando_trocar_secao=self.trocar_secao_resultados
        )
        self.barra_resultados.pack(anchor="center", pady=(0, 10))

        self.container_abas = ctk.CTkFrame(self, fg_color="transparent")
        self.container_abas.pack(fill="both", expand=True)

        self.trocar_secao_resultados("modelo")

    def trocar_secao_resultados(self, secao):
        self.aba_atual.set(secao)

        if self.barra_resultados:
            self.barra_resultados.atualizar_estado(secao)

        for widget in self.container_abas.winfo_children():
            widget.destroy()

        if secao == "modelo":
            self.criar_aba_resultado_modelo(self.container_abas)
        else:
            criar_aba_comparacao(
                self.container_abas,
                self.modelos_config,
                self.metricas_modelos
            )

    def criar_aba_resultado_modelo(self, master):
        self.conteudo_modelo = ctk.CTkFrame(master, fg_color="transparent")
        self.conteudo_modelo.pack(fill="both", expand=True)

        self.atualizar_resultado_modelo()

    def alternar_modelo(self, modelo):
        self.modelo_atual.set(modelo)
        self.metricas = self.metricas_modelos.get(modelo)

        if (
            getattr(self, "aba_atual", None)
            and self.aba_atual.get() == "modelo"
            and self.conteudo_modelo
        ):
            self.atualizar_resultado_modelo()

    def atualizar_resultado_modelo(self):
        for widget in self.conteudo_modelo.winfo_children():
            widget.destroy()

        if not self.metricas:
            self.criar_mensagem_modelo_indisponivel(
                self.conteudo_modelo,
                self.modelo_atual.get()
            )
            return

        criar_cards_metricas(self.conteudo_modelo, self.metricas)
        criar_cards_resumo_teste(self.conteudo_modelo, self.metricas)
        criar_area_graficos(self.conteudo_modelo, self.metricas)
        criar_relatorio_classificacao(self.conteudo_modelo, self.metricas)

    def criar_mensagem_sem_resultados(self, master):
        card = ctk.CTkFrame(
            master,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=16,
            border_width=1,
            border_color=Cores.BORDA
        )
        card.pack(fill="x", padx=4, pady=10)

        ctk.CTkLabel(
            card,
            text="Nenhum resultado encontrado",
            font=("Arial", 20, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        ).pack(anchor="w", padx=22, pady=(22, 8))

        ctk.CTkLabel(
            card,
            text="Treine ao menos um modelo para gerar o arquivo de métricas e exibir os resultados nesta tela.",
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO,
            wraplength=850,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))

    def criar_mensagem_modelo_indisponivel(self, master, modelo):
        card = ctk.CTkFrame(
            master,
            fg_color=Cores.FUNDO_CARD,
            corner_radius=18,
            border_width=1,
            border_color=Cores.BORDA
        )
        card.pack(fill="x", padx=4, pady=10)

        ctk.CTkLabel(
            card,
            text=f"Resultados de {modelo} ainda não encontrados",
            font=("Arial", 20, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        ).pack(anchor="w", padx=22, pady=(22, 8))

        ctk.CTkLabel(
            card,
            text="Após treinar esse modelo, salve as métricas em persistencia/data/modelos/mobilenetv2/metricas.json ou em metricas_mobilenetv2.json.",
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO,
            wraplength=850,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))
