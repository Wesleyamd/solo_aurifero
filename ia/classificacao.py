from pathlib import Path
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

from utils.caminhos import MODELOS_DIR

IMG_SIZE = (224, 224)


def classificar_imagem(caminho_imagem):
    caminho_modelo = MODELOS_DIR / "modelo_solo.keras"
    caminho_classes = MODELOS_DIR / "classes.json"

    if not caminho_modelo.exists():
        raise FileNotFoundError("Modelo ainda não foi treinado.")

    modelo = tf.keras.models.load_model(caminho_modelo)

    if caminho_classes.exists():
        classes = json.loads(caminho_classes.read_text(encoding="utf-8"))
    else:
        classes = ["nao_aurifero", "potencial_aurifero"]

    imagem = tf.keras.utils.load_img(caminho_imagem, target_size=IMG_SIZE)
    array = tf.keras.utils.img_to_array(imagem)
    array = np.expand_dims(array, axis=0)
    array = preprocess_input(array)

    probabilidade = float(modelo.predict(array, verbose=0)[0][0])
    indice = 1 if probabilidade >= 0.5 else 0
    classe = classes[indice]
    confianca = probabilidade if indice == 1 else 1 - probabilidade

    if "potencial" in classe or "aurifero" in classe and "nao" not in classe:
        resultado = "Possível Potencial Aurífero"
    else:
        resultado = "Sem Potencial Aurífero"

    return resultado, round(confianca * 100, 2), classe
