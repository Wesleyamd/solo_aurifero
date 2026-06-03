import os
import shutil
import uuid

from ia.treinamento_efficientnetB0 import treinar_efficientnet
from ia.treinamento_mobilenetV2 import treinar_mobilenet
from persistencia.repository.treinamento_repository import TreinamentoRepository
from utils.caminhos import (
    DATASET_DIR,
    DATASET_POTENCIAL_DIR,
    DATASET_NAO_AURIFERO_DIR,
    MODELOS_DIR,
)


class TreinamentoController:
    """Controla o fluxo de preparação do dataset e treinamento da IA."""

    MODELOS_DISPONIVEIS = {
        "EfficientNetB0": {
            "funcao": treinar_efficientnet,
            "arquivo_modelo": "modelo_efficientnetb0.keras",
        },
        "MobileNetV2": {
            "funcao": treinar_mobilenet,
            "arquivo_modelo": "modelo_mobilenetv2.keras",
        },
    }

    @staticmethod
    def preparar_pastas():
        for pasta in [DATASET_POTENCIAL_DIR, DATASET_NAO_AURIFERO_DIR, MODELOS_DIR]:
            pasta.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def pasta_classe(classe):
        if classe == "potencial":
            return DATASET_POTENCIAL_DIR
        if classe == "nao":
            return DATASET_NAO_AURIFERO_DIR
        raise ValueError("Classe inválida. Use 'potencial' ou 'nao'.")

    @staticmethod
    def adicionar_imagens(classe, caminhos):
        pasta = TreinamentoController.pasta_classe(classe)
        pasta.mkdir(parents=True, exist_ok=True)

        copiadas = 0
        for caminho in caminhos:
            try:
                extensao = os.path.splitext(caminho)[1].lower()
                if extensao not in [".jpg", ".jpeg", ".png"]:
                    continue

                nome = f"{uuid.uuid4().hex}{extensao}"
                destino = pasta / nome
                shutil.copy2(caminho, destino)
                copiadas += 1
            except Exception as erro:
                print(f"Erro ao copiar imagem: {erro}")

        return copiadas

    @staticmethod
    def contar_imagens_pasta(pasta):
        if not pasta.exists():
            return 0

        return len([
            arquivo for arquivo in os.listdir(pasta)
            if arquivo.lower().endswith((".jpg", ".jpeg", ".png"))
        ])

    @staticmethod
    def obter_resumo(modelo="EfficientNetB0"):
        total_potencial = TreinamentoController.contar_imagens_pasta(DATASET_POTENCIAL_DIR)
        total_nao = TreinamentoController.contar_imagens_pasta(DATASET_NAO_AURIFERO_DIR)
        total = total_potencial + total_nao
        treinado = TreinamentoController.modelo_treinado(modelo)

        return {
            "total_potencial": total_potencial,
            "total_nao": total_nao,
            "total": total,
            "treinado": treinado,
            "modelo": modelo,
        }

    @staticmethod
    def modelo_treinado(modelo="EfficientNetB0"):
        config = TreinamentoController.MODELOS_DISPONIVEIS.get(modelo)
        if not config:
            return False

        caminho_modelo = MODELOS_DIR / config["arquivo_modelo"]

        # Compatibilidade com versões antigas do projeto.
        if modelo == "EfficientNetB0":
            caminho_legado = MODELOS_DIR / "modelo_solo.keras"
            return caminho_modelo.exists() or caminho_legado.exists() or TreinamentoRepository.modelo_treinado()

        return caminho_modelo.exists()

    @staticmethod
    def validar_dataset(minimo_por_classe=20):
        resumo = TreinamentoController.obter_resumo()
        return (
            resumo["total_potencial"] >= minimo_por_classe
            and resumo["total_nao"] >= minimo_por_classe
        )

    @staticmethod
    def treinar_modelo(modelo="EfficientNetB0", epocas=10):
        if modelo not in TreinamentoController.MODELOS_DISPONIVEIS:
            raise ValueError(f"Modelo inválido: {modelo}")

        config = TreinamentoController.MODELOS_DISPONIVEIS[modelo]
        funcao_treinamento = config["funcao"]

        metricas = funcao_treinamento(
            pasta_dataset=DATASET_DIR,
            pasta_modelos=MODELOS_DIR,
            epocas=epocas,
        )

        resumo = TreinamentoController.obter_resumo(modelo)
        TreinamentoRepository.salvar(
            total_potencial=resumo["total_potencial"],
            total_nao_aurifero=resumo["total_nao"],
            modelo_gerado=metricas.get("caminho_modelo", MODELOS_DIR / config["arquivo_modelo"]),
        )

        return metricas
