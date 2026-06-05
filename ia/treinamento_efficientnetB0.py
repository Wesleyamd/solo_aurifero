from pathlib import Path
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report


IMG_SIZE = (224, 224)
BATCH_SIZE = 16
SEED = 42


def treinar_efficientnet(pasta_dataset, pasta_modelos, epocas=10):
    """
    Treina um modelo EfficientNetB0 usando a estrutura:

    dataset/
    ├── potencial_aurifero/
    └── nao_aurifero/

    Retorna um dicionário com métricas e caminhos dos arquivos gerados.
    """
    pasta_dataset = Path(pasta_dataset)
    pasta_modelos = Path(pasta_modelos)
    pasta_modelos.mkdir(parents=True, exist_ok=True)

    if not pasta_dataset.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {pasta_dataset}")

    treino = tf.keras.utils.image_dataset_from_directory(
        pasta_dataset,
        validation_split=0.30,
        subset="training",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
    )

    validacao_teste = tf.keras.utils.image_dataset_from_directory(
        pasta_dataset,
        validation_split=0.30,
        subset="validation",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
    )

    nomes_classes = treino.class_names

    total_validacao = tf.data.experimental.cardinality(validacao_teste).numpy()
    qtd_validacao = max(1, total_validacao // 2)
    validacao = validacao_teste.take(qtd_validacao)
    teste = validacao_teste.skip(qtd_validacao)

    AUTOTUNE = tf.data.AUTOTUNE
    treino = treino.prefetch(AUTOTUNE)
    validacao = validacao.prefetch(AUTOTUNE)
    teste = teste.prefetch(AUTOTUNE)

    aumento_dados = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10),
    ])

    base = EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(224, 224, 3),
    )
    base.trainable = False

    entrada = layers.Input(shape=(224, 224, 3))
    x = aumento_dados(entrada)
    x = preprocess_input(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.20)(x)
    saida = layers.Dense(1, activation="sigmoid")(x)

    modelo = tf.keras.Model(entrada, saida)
    modelo.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
        )
    ]

    historico = modelo.fit(
        treino,
        validation_data=validacao,
        epochs=epocas,
        callbacks=callbacks,
    )

    y_real = []
    y_pred = []

    for imagens, labels in teste:
        probabilidades = modelo.predict(imagens, verbose=0).ravel()
        predicoes = (probabilidades >= 0.5).astype(int)
        y_pred.extend(predicoes.tolist())
        y_real.extend(labels.numpy().astype(int).ravel().tolist())

    if len(y_real) == 0:
        raise ValueError("Conjunto de teste vazio. Adicione mais imagens ao dataset.")

    matriz = confusion_matrix(y_real, y_pred).tolist()

    metricas = {
        "modelo": "EfficientNetB0",
        "classes": nomes_classes,
        "accuracy": round(float(accuracy_score(y_real, y_pred)), 4),
        "precision": round(float(precision_score(y_real, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_real, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_real, y_pred, zero_division=0)), 4),
        "matriz_confusao": matriz,
        "relatorio": classification_report(y_real, y_pred, target_names=nomes_classes, zero_division=0),
        "historico": {
            "accuracy": [float(v) for v in historico.history.get("accuracy", [])],
            "val_accuracy": [float(v) for v in historico.history.get("val_accuracy", [])],
            "loss": [float(v) for v in historico.history.get("loss", [])],
            "val_loss": [float(v) for v in historico.history.get("val_loss", [])],
        }
    }

    caminho_modelo = pasta_modelos / "modelo_efficientnetb0.keras"
    caminho_metricas = pasta_modelos / "metricas_efficientnetb0.json"
    caminho_classes = pasta_modelos / "classes_efficientnetb0.json"

    modelo.save(caminho_modelo)
    caminho_metricas.write_text(json.dumps(metricas, indent=4, ensure_ascii=False), encoding="utf-8")
    caminho_classes.write_text(json.dumps(nomes_classes, indent=4, ensure_ascii=False), encoding="utf-8")

    metricas["caminho_modelo"] = str(caminho_modelo)
    metricas["caminho_metricas"] = str(caminho_metricas)
    metricas["caminho_classes"] = str(caminho_classes)

    return metricas
