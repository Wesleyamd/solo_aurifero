import customtkinter as ctk

from interface.componentes.cards_resultados import (
    calcular_acertos,
    calcular_erros,
    calcular_total_teste,
    formatar_percentual,
    obter_melhor_modelo
)
from interface.componentes.graficos_resultados import criar_grafico_comparacao
from interface.componentes.relatorio_classificacao import criar_tabela
from interface.tema.cores import Cores


def criar_aba_comparacao(master, modelos_config, metricas_modelos):
    card = ctk.CTkFrame(
        master,
        fg_color=Cores.FUNDO_CARD,
        corner_radius=18,
        border_width=1,
        border_color=Cores.BORDA
    )
    card.pack(fill="x", padx=4, pady=(2, 12))

    ctk.CTkLabel(
        card,
        text="Comparação entre Modelos",
        font=("Arial", 18, "bold"),
        text_color=Cores.TEXTO_PRINCIPAL
    ).pack(anchor="w", padx=18, pady=(14, 4))

    ctk.CTkLabel(
        card,
        text="Compare as principais métricas de desempenho dos modelos treinados.",
        font=("Arial", 13),
        text_color=Cores.TEXTO_SECUNDARIO
    ).pack(anchor="w", padx=18, pady=(0, 10))

    linhas = []
    for nome_modelo in modelos_config.keys():
        metricas = metricas_modelos.get(nome_modelo)

        if metricas:
            linhas.append([
                nome_modelo,
                formatar_percentual(metricas, "accuracy"),
                formatar_percentual(metricas, "precision"),
                formatar_percentual(metricas, "recall"),
                formatar_percentual(metricas, "f1_score"),
                str(calcular_total_teste(metricas)),
                str(calcular_acertos(metricas)),
                str(calcular_erros(metricas)),
            ])
        else:
            linhas.append([nome_modelo, "--", "--", "--", "--", "--", "--", "--"])

    criar_tabela(
        card,
        cabecalho=["Modelo", "Acurácia", "Precisão", "Recall", "F1-Score", "Teste", "Acertos", "Erros"],
        linhas=linhas,
        larguras=[1.8, 1, 1, 1, 1, 0.8, 0.8, 0.8]
    )

    melhor = obter_melhor_modelo(metricas_modelos)
    if melhor:
        ctk.CTkLabel(
            card,
            text=f"Melhor desempenho geral: {melhor}  |  Critério: maior F1-score e acurácia no teste",
            font=("Arial", 14, "bold"),
            text_color=Cores.DOURADO
        ).pack(anchor="w", padx=18, pady=(0, 18))

    criar_grafico_comparacao(master, metricas_modelos)
