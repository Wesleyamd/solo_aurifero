import os

from utils.caminhos import DATASET_POTENCIAL_DIR, DATASET_NAO_AURIFERO_DIR


class DatasetRepository:

    EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png")

    @staticmethod
    def contar_imagens_pasta(pasta):
        if not pasta.exists():
            return 0

        return len([
            arquivo for arquivo in os.listdir(pasta)
            if arquivo.lower().endswith(DatasetRepository.EXTENSOES_IMAGEM)
        ])

    @staticmethod
    def contar_potencial_aurifero():
        return DatasetRepository.contar_imagens_pasta(DATASET_POTENCIAL_DIR)

    @staticmethod
    def contar_nao_aurifero():
        return DatasetRepository.contar_imagens_pasta(DATASET_NAO_AURIFERO_DIR)

    @staticmethod
    def resumo_dataset():
        potencial = DatasetRepository.contar_potencial_aurifero()
        nao_aurifero = DatasetRepository.contar_nao_aurifero()

        return {
            "potencial_aurifero": potencial,
            "nao_aurifero": nao_aurifero,
            "total": potencial + nao_aurifero
        }