import cv2
import numpy as np


def extrair_caracteristicas(caminho_imagem):
    """
    Extrai características simples da imagem:
    - médias de cor
    - desvio padrão de cor
    - histograma de cor
    """

    imagem = cv2.imread(caminho_imagem)

    if imagem is None:
        raise ValueError(f"Não foi possível carregar a imagem: {caminho_imagem}")

    # Redimensiona para padronizar
    imagem = cv2.resize(imagem, (224, 224))

    # Converte BGR para HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # Médias dos canais HSV
    media_h = np.mean(hsv[:, :, 0])
    media_s = np.mean(hsv[:, :, 1])
    media_v = np.mean(hsv[:, :, 2])

    # Desvios dos canais HSV
    desvio_h = np.std(hsv[:, :, 0])
    desvio_s = np.std(hsv[:, :, 1])
    desvio_v = np.std(hsv[:, :, 2])

    # Histograma HSV simplificado
    hist_h = cv2.calcHist([hsv], [0], None, [16], [0, 180]).flatten()
    hist_s = cv2.calcHist([hsv], [1], None, [16], [0, 256]).flatten()
    hist_v = cv2.calcHist([hsv], [2], None, [16], [0, 256]).flatten()

    # Normaliza histogramas
    hist_h = hist_h / hist_h.sum()
    hist_s = hist_s / hist_s.sum()
    hist_v = hist_v / hist_v.sum()

    caracteristicas = np.concatenate([
        [media_h, media_s, media_v],
        [desvio_h, desvio_s, desvio_v],
        hist_h,
        hist_s,
        hist_v
    ])

    return caracteristicas