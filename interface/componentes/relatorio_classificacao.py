import re

import customtkinter as ctk

from interface.tema.cores import Cores


def formatar_nome_classe(nome):
    nome = str(nome).replace("_", " ").strip().title()
    nome = nome.replace("Nao", "Não")
    return nome


def formatar_valor_percentual(valor):
    if valor is None:
        return "--"
    return f"{float(valor) * 100:.2f}%"


def criar_tabela(master, cabecalho, linhas, larguras=None):
    tabela = ctk.CTkFrame(
        master,
        fg_color=Cores.FUNDO_SECUNDARIO,
        corner_radius=12
    )
    tabela.pack(fill="x", padx=18, pady=(0, 18))

    larguras = larguras or [1] * len(cabecalho)
    for coluna, peso in enumerate(larguras):
        tabela.grid_columnconfigure(coluna, weight=int(peso * 10), uniform="colunas")

    for coluna, texto in enumerate(cabecalho):
        ctk.CTkLabel(
            tabela,
            text=texto,
            font=("Arial", 13, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL,
            anchor="w"
        ).grid(row=0, column=coluna, sticky="ew", padx=12, pady=(12, 8))

    for linha_indice, valores in enumerate(linhas, start=1):
        for coluna, valor in enumerate(valores):
            ctk.CTkLabel(
                tabela,
                text=str(valor),
                font=("Arial", 13),
                text_color=Cores.TEXTO_SECUNDARIO,
                anchor="w"
            ).grid(row=linha_indice, column=coluna, sticky="ew", padx=12, pady=7)


def criar_relatorio_classificacao(master, metricas):
    card = ctk.CTkFrame(
        master,
        fg_color=Cores.FUNDO_CARD,
        corner_radius=18,
        border_width=1,
        border_color=Cores.BORDA
    )
    card.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(
        card,
        text="Relatório de Classificação",
        font=("Arial", 17, "bold"),
        text_color=Cores.TEXTO_PRINCIPAL
    ).pack(anchor="w", padx=16, pady=(12, 7))

    linhas = obter_linhas_relatorio(metricas)

    if not linhas:
        ctk.CTkLabel(
            card,
            text="Relatório não disponível.",
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        ).pack(anchor="w", padx=18, pady=(0, 18))
        return

    criar_tabela(
        card,
        cabecalho=["Classe", "Precisão", "Recall", "F1-Score", "Amostras"],
        linhas=linhas,
        larguras=[2.4, 1, 1, 1, 0.8]
    )


def obter_linhas_relatorio(metricas):
    linhas_matriz = obter_linhas_relatorio_por_matriz(metricas)
    if linhas_matriz:
        return linhas_matriz

    relatorio = (metricas or {}).get("relatorio")

    if isinstance(relatorio, dict):
        linhas = []
        for chave, valores in relatorio.items():
            if chave in ["accuracy", "macro avg", "weighted avg"]:
                continue

            if isinstance(valores, dict):
                linhas.append([
                    formatar_nome_classe(chave),
                    formatar_valor_percentual(valores.get("precision")),
                    formatar_valor_percentual(valores.get("recall")),
                    formatar_valor_percentual(valores.get("f1-score")),
                    str(int(valores.get("support", 0))),
                ])

        return linhas

    if isinstance(relatorio, str):
        return converter_relatorio_texto_para_linhas(relatorio)

    return []


def obter_linhas_relatorio_por_matriz(metricas):
    matriz = (metricas or {}).get("matriz_confusao")
    if not matriz or len(matriz) < 2:
        return []

    classes = (metricas or {}).get("classes", ["nao_aurifero", "potencial_aurifero"])
    linhas = []
    total_classes = min(len(classes), len(matriz))

    for indice in range(total_classes):
        vp = matriz[indice][indice]
        suporte = sum(matriz[indice])
        previstos = sum(linha[indice] for linha in matriz)

        precisao = (vp / previstos) if previstos else 0
        recall = (vp / suporte) if suporte else 0
        f1 = (2 * precisao * recall / (precisao + recall)) if (precisao + recall) else 0

        linhas.append([
            formatar_nome_classe(classes[indice]),
            formatar_valor_percentual(precisao),
            formatar_valor_percentual(recall),
            formatar_valor_percentual(f1),
            str(suporte),
        ])

    return linhas


def converter_relatorio_texto_para_linhas(relatorio):
    linhas = []

    for linha in relatorio.splitlines():
        linha = linha.strip()

        if not linha or linha.startswith("precision"):
            continue

        if any(item in linha for item in ["accuracy", "macro avg", "weighted avg"]):
            continue

        partes = re.split(r"\s{2,}", linha)

        if len(partes) >= 5:
            nome = partes[0]

            try:
                precision = float(partes[1])
                recall = float(partes[2])
                f1 = float(partes[3])
                suporte = int(float(partes[4]))
            except ValueError:
                continue

            linhas.append([
                formatar_nome_classe(nome),
                formatar_valor_percentual(precision),
                formatar_valor_percentual(recall),
                formatar_valor_percentual(f1),
                str(suporte),
            ])

    return linhas
