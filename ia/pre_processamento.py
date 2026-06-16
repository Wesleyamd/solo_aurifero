import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.applications.efficientnet import preprocess_input

IMG_SIZE = (224, 224)


def gerar_imagem_preprocessada(
    caminho_imagem,
    caminho_saida="imagem_preprocessada.png"
):

    imagem = tf.keras.utils.load_img(
        caminho_imagem,
        target_size=IMG_SIZE,
        color_mode="rgb"
    )

    array = tf.keras.utils.img_to_array(imagem)
    array = np.expand_dims(array, axis=0)

    imagem_preparada = preprocess_input(array)

    img = imagem_preparada[0]

    img_visual = (img - img.min()) / (img.max() - img.min())

    plt.imsave(caminho_saida, img_visual)

    return caminho_saida