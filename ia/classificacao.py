import json
import numpy as np
import tensorflow as tf

from utils.caminhos import MODELOS_DIR

IMG_SIZE = (224, 224)

MODELOS_CLASSIFICACAO = {
    "EfficientNetB0": {
        "modelo": "modelo_efficientnetb0.keras",
        "classes": "classes_efficientnetb0.json",
    },
    "MobileNetV2": {
        "modelo": "modelo_mobilenetv2.keras",
        "classes": "classes_mobilenetv2.json",
    },
}


def _resolver_modelo(modelo_preferido=None):
    """
    Resolve o modelo que será usado na classificação.

    Os modelos treinados já possuem o pré-processamento interno.
    Por isso, a imagem deve ser enviada em formato bruto RGB 224x224.
    """
    if not modelo_preferido:
        modelo_preferido = "EfficientNetB0"

    aliases = {
        "efficientnetb0": "EfficientNetB0",
        "mobilenetv2": "MobileNetV2",
        "mobileNetV2": "MobileNetV2",
        "MobileNetV2": "MobileNetV2",
    }

    modelo_preferido = aliases.get(str(modelo_preferido).strip(), modelo_preferido)

    if modelo_preferido not in MODELOS_CLASSIFICACAO:
        modelos_disponiveis = ", ".join(MODELOS_CLASSIFICACAO.keys())
        raise ValueError(f"Informe um modelo válido: {modelos_disponiveis}.")

    config = MODELOS_CLASSIFICACAO[modelo_preferido]
    caminho_modelo = MODELOS_DIR / config["modelo"]

    if caminho_modelo.exists():
        return modelo_preferido, config, caminho_modelo

    raise FileNotFoundError(f"Modelo {modelo_preferido} ainda não foi treinado.")


def classificar_imagem(caminho_imagem, modelo_preferido="EfficientNetB0"):
    nome_modelo, config, caminho_modelo = _resolver_modelo(modelo_preferido)
    caminho_classes = MODELOS_DIR / config["classes"]

    modelo = tf.keras.models.load_model(caminho_modelo)

    print(f"Modelo carregado: {caminho_modelo}")
    print(f"Modelo selecionado: {nome_modelo}")

    if caminho_classes.exists():
        classes = json.loads(caminho_classes.read_text(encoding="utf-8"))
    else:
        classes = ["nao_aurifero", "potencial_aurifero"]

    imagem = tf.keras.utils.load_img(
        caminho_imagem,
        target_size=IMG_SIZE,
        color_mode="rgb"
    )

    array = tf.keras.utils.img_to_array(imagem)
    array = np.expand_dims(array, axis=0)

    # Importante:
    # Não aplicar preprocess_input aqui.
    # Os modelos salvos já possuem preprocess_input dentro da arquitetura.
    probabilidade = float(modelo.predict(array, verbose=0)[0][0])

    indice = 1 if probabilidade >= 0.5 else 0
    classe = classes[indice]
    confianca = probabilidade if indice == 1 else 1 - probabilidade

    if ("potencial" in classe or "aurifero" in classe) and "nao" not in classe:
        resultado = "Possível Potencial Aurífero"
    else:
        resultado = "Sem Potencial Aurífero"

    return resultado, round(confianca * 100, 2), classe
