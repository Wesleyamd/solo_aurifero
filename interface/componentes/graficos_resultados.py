import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from interface.tema.cores import Cores


def criar_card_grafico(master, titulo):
    card = ctk.CTkFrame(
        master,
        fg_color=Cores.FUNDO_CARD,
        corner_radius=18,
        border_width=1,
        border_color=Cores.BORDA
    )

    ctk.CTkLabel(
        card,
        text=titulo,
        font=("Arial", 17, "bold"),
        text_color=Cores.TEXTO_PRINCIPAL
    ).pack(anchor="w", padx=16, pady=(12, 7))

    return card


def criar_area_graficos(master, metricas):
    frame_graficos = ctk.CTkFrame(master, fg_color="transparent")
    frame_graficos.pack(fill="both", expand=True, pady=(0, 12))

    grafico_historico = criar_card_grafico(
        frame_graficos,
        "Evolução do Treinamento"
    )
    grafico_historico.pack(side="left", fill="both", expand=True, padx=(0, 8))
    desenhar_grafico_historico(grafico_historico, metricas)

    grafico_matriz = criar_card_grafico(
        frame_graficos,
        "Matriz de Confusão"
    )
    grafico_matriz.pack(side="left", fill="both", expand=True, padx=(8, 0))
    desenhar_matriz_confusao(grafico_matriz, metricas)


def desenhar_grafico_historico(master, metricas):
    historico = (metricas or {}).get("historico", {})
    acc = historico.get("accuracy", [])
    val_acc = historico.get("val_accuracy", [])
    loss = historico.get("loss", [])
    val_loss = historico.get("val_loss", [])

    figura = Figure(figsize=(5.6, 3.5), dpi=100)
    eixo = figura.add_subplot(111)

    if acc:
        epocas = list(range(1, len(acc) + 1))
        eixo.plot(epocas, acc, marker="o", label="Acurácia treino")
    if val_acc:
        epocas = list(range(1, len(val_acc) + 1))
        eixo.plot(epocas, val_acc, marker="o", label="Acurácia validação")
    if loss:
        epocas = list(range(1, len(loss) + 1))
        eixo.plot(epocas, loss, linestyle="--", label="Loss treino")
    if val_loss:
        epocas = list(range(1, len(val_loss) + 1))
        eixo.plot(epocas, val_loss, linestyle="--", label="Loss validação")

    eixo.set_xlabel("Épocas")
    eixo.set_ylabel("Valor")
    eixo.set_title("Acurácia e perda por época")
    eixo.grid(True, alpha=0.3)
    eixo.legend(fontsize=8)
    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=(0, 12))


def desenhar_matriz_confusao(master, metricas):
    matriz = (metricas or {}).get("matriz_confusao", [[0, 0], [0, 0]])
    classes = (metricas or {}).get("classes", ["nao_aurifero", "potencial_aurifero"])
    classes = [classe.replace("_", " ").title().replace("Nao", "Não") for classe in classes]

    figura = Figure(figsize=(5.6, 3.5), dpi=100)
    eixo = figura.add_subplot(111)
    imagem = eixo.imshow(matriz, cmap="Greens")

    eixo.set_xticks(range(len(classes)))
    eixo.set_yticks(range(len(classes)))
    eixo.set_xticklabels(classes, rotation=20, ha="right")
    eixo.set_yticklabels(classes)
    eixo.set_xlabel("Classe prevista")
    eixo.set_ylabel("Classe real")
    eixo.set_title("Acertos e erros do modelo")

    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            eixo.text(
                j,
                i,
                str(valor),
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold"
            )

    figura.colorbar(imagem, ax=eixo, fraction=0.046, pad=0.04)
    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=(0, 12))


def criar_grafico_comparacao(master, metricas_modelos):
    modelos = []
    acuracias = []
    f1_scores = []

    for nome_modelo, metricas in metricas_modelos.items():
        modelos.append(nome_modelo)
        acuracias.append(float(metricas.get("accuracy", 0)) * 100)
        f1_scores.append(float(metricas.get("f1_score", 0)) * 100)

    if not modelos:
        return

    card = criar_card_grafico(master, "Gráfico Comparativo")
    card.pack(fill="both", expand=True, padx=4, pady=(0, 10))

    figura = Figure(figsize=(4.5, 3.6), dpi=100)
    eixo = figura.add_subplot(111)

    posicoes = list(range(len(modelos)))
    largura = 0.35

    eixo.bar(
        [p - largura / 2 for p in posicoes],
        acuracias,
        width=largura,
        label="Acurácia"
    )
    eixo.bar(
        [p + largura / 2 for p in posicoes],
        f1_scores,
        width=largura,
        label="F1-Score"
    )

    eixo.set_xticks(posicoes)
    eixo.set_xticklabels(modelos)
    eixo.set_ylim(0, 100)
    eixo.set_ylabel("Percentual (%)")
    eixo.set_title("Acurácia e F1-score por modelo")
    eixo.grid(True, axis="y", alpha=0.3)
    eixo.legend()
    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=card)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=(0, 12))
