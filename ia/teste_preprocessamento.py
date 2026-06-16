from ia.pre_processamento import gerar_imagem_preprocessada

from pathlib import Path

if __name__ == "__main__":
    imagem_teste = Path(r"C:\Users\Wesley Carvalho\PycharmProjects\Solo_aurifero\persistencia\data\dataset\potencial_aurifero\1e327d08d2c148139f2dee3ae6181249.jpg")

    saida = imagem_teste.parent / "imagem_preprocessada.png"

    print("Iniciando teste...")

    caminho_saida = gerar_imagem_preprocessada(
        str(imagem_teste),
        str(saida)
    )

    print(f"Imagem salva em: {caminho_saida}")