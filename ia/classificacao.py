import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input as preprocess_efficientnet
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as preprocess_mobilenet

from utils.caminhos import MODELOS_DIR

IMG_SIZE = (224, 224)

MODELOS_CLASSIFICACAO = {
    "EfficientNetB0": {
        "modelo": "modelo_efficientnetb0.keras",
        "classes": "classes_efficientnetb0.json",
        "preprocess": preprocess_efficientnet,
    },
    "MobileNetV2": {
        "modelo": "modelo_mobilenetv2.keras",
        "classes": "classes_mobilenetv2.json",
        "preprocess": preprocess_mobilenet,
    },
    # Compatibilidade com versões antigas do projeto.
    "Legado": {
        "modelo": "modelo_solo.keras",
        "classes": "classes.json",
        "preprocess": preprocess_efficientnet,
    },
}


def _resolver_modelo(modelo_preferido=None):
    ordem = []

    if modelo_preferido in MODELOS_CLASSIFICACAO:
        ordem.append(modelo_preferido)

    ordem.extend(["EfficientNetB0", "Legado", "MobileNetV2"])

    for nome in ordem:
        config = MODELOS_CLASSIFICACAO[nome]
        caminho_modelo = MODELOS_DIR / config["modelo"]
        if caminho_modelo.exists():
            return nome, config, caminho_modelo

    raise FileNotFoundError("Modelo ainda não foi treinado.")


def classificar_imagem(caminho_imagem, modelo_preferido=None):
    nome_modelo, config, caminho_modelo = _resolver_modelo(modelo_preferido)
    caminho_classes = MODELOS_DIR / config["classes"]

    modelo = tf.keras.models.load_model(caminho_modelo)

    if caminho_classes.exists():
        classes = json.loads(caminho_classes.read_text(encoding="utf-8"))
    else:
        classes = ["nao_aurifero", "potencial_aurifero"]

    imagem = tf.keras.utils.load_img(caminho_imagem, target_size=IMG_SIZE)
    array = tf.keras.utils.img_to_array(imagem)
    array = np.expand_dims(array, axis=0)
    array = config["preprocess"](array)

    probabilidade = float(modelo.predict(array, verbose=0)[0][0])
    indice = 1 if probabilidade >= 0.5 else 0
    classe = classes[indice]
    confianca = probabilidade if indice == 1 else 1 - probabilidade

    if ("potencial" in classe or "aurifero" in classe) and "nao" not in classe:
        resultado = "Possível Potencial Aurífero"
    else:
        resultado = "Sem Potencial Aurífero"

    return resultado, round(confianca * 100, 2), classe
