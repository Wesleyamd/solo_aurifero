import customtkinter as ctk

from interface.componentes.card_treinamento_resumo import CardTreinamentoResumo


def formatar_percentual(metricas, chave):
    valor = (metricas or {}).get(chave)
    if valor is None:
        return "--"
    return f"{float(valor) * 100:.2f}%"


def calcular_total_teste(metricas):
    matriz = (metricas or {}).get("matriz_confusao", [])
    return sum(sum(linha) for linha in matriz) if matriz else 0


def calcular_acertos(metricas):
    matriz = (metricas or {}).get("matriz_confusao", [])
    if not matriz:
        return 0
    return sum(matriz[i][i] for i in range(min(len(matriz), len(matriz[0]))))


def calcular_erros(metricas):
    total = calcular_total_teste(metricas)
    acertos = calcular_acertos(metricas)
    return total - acertos


def calcular_falsos_positivos_negativos(metricas):
    matriz = (metricas or {}).get("matriz_confusao", [])
    if len(matriz) >= 2 and len(matriz[0]) >= 2:
        return matriz[0][1], matriz[1][0]
    return 0, 0


def criar_cards_metricas(master, metricas):
    frame_cards = ctk.CTkFrame(master, fg_color="transparent")
    frame_cards.pack(fill="x", pady=(0, 12))

    metricas_cards = [
        ("🎯 Acurácia", formatar_percentual(metricas, "accuracy")),
        ("🎖 Precisão", formatar_percentual(metricas, "precision")),
        ("🔍 Recall", formatar_percentual(metricas, "recall")),
        ("⚖ F1-score", formatar_percentual(metricas, "f1_score")),
    ]

    for indice, (titulo, valor) in enumerate(metricas_cards):
        padx = (0, 6) if indice == 0 else (6, 6)
        if indice == len(metricas_cards) - 1:
            padx = (6, 0)

        card = CardTreinamentoResumo(frame_cards, titulo, valor)
        card.pack(side="left", expand=True, fill="x", padx=padx)


def criar_cards_resumo_teste(master, metricas):
    frame_cards = ctk.CTkFrame(master, fg_color="transparent")
    frame_cards.pack(fill="x", pady=(0, 12))

    falso_positivo, falso_negativo = calcular_falsos_positivos_negativos(metricas)

    itens = [
        ("Imagens de teste", str(calcular_total_teste(metricas))),
        ("Classificações corretas", str(calcular_acertos(metricas))),
        ("Falsos positivos", str(falso_positivo)),
        ("Falsos negativos", str(falso_negativo)),
    ]

    for indice, (titulo, valor) in enumerate(itens):
        padx = (0, 6) if indice == 0 else (6, 6)
        if indice == len(itens) - 1:
            padx = (6, 0)

        card = CardTreinamentoResumo(frame_cards, titulo, valor)
        card.pack(side="left", expand=True, fill="x", padx=padx)


def obter_melhor_modelo(metricas_modelos):
    disponiveis = {
        nome: dados for nome, dados in metricas_modelos.items()
        if dados.get("accuracy") is not None
    }

    if not disponiveis:
        return None

    return max(
        disponiveis,
        key=lambda nome: (
            disponiveis[nome].get("f1_score", 0),
            disponiveis[nome].get("accuracy", 0)
        )
    )
