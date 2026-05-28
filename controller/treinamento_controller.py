import os
import shutil
import uuid

from ia.treinamento import treinar_efficientnet
from persistencia.repository.treinamento_repository import TreinamentoRepository
from utils.caminhos import (
    DATASET_DIR,
    DATASET_POTENCIAL_DIR,
    DATASET_NAO_AURIFERO_DIR,
    MODELOS_DIR,
)


class TreinamentoController:
    """Controla o fluxo de preparação do dataset e treinamento da IA."""

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
    def obter_resumo():
        total_potencial = TreinamentoController.contar_imagens_pasta(DATASET_POTENCIAL_DIR)
        total_nao = TreinamentoController.contar_imagens_pasta(DATASET_NAO_AURIFERO_DIR)
        total = total_potencial + total_nao
        treinado = TreinamentoController.modelo_treinado()

        return {
            "total_potencial": total_potencial,
            "total_nao": total_nao,
            "total": total,
            "treinado": treinado,
        }

    @staticmethod
    def modelo_treinado():
        caminho_modelo = MODELOS_DIR / "modelo_solo.keras"
        return caminho_modelo.exists() or TreinamentoRepository.modelo_treinado()

    @staticmethod
    def validar_dataset(minimo_por_classe=20):
        resumo = TreinamentoController.obter_resumo()
        return (
            resumo["total_potencial"] >= minimo_por_classe
            and resumo["total_nao"] >= minimo_por_classe
        )

    @staticmethod
    def treinar_modelo(epocas=10):
        metricas = treinar_efficientnet(
            pasta_dataset=DATASET_DIR,
            pasta_modelos=MODELOS_DIR,
            epocas=epocas,
        )

        resumo = TreinamentoController.obter_resumo()
        TreinamentoRepository.salvar(
            total_potencial=resumo["total_potencial"],
            total_nao_aurifero=resumo["total_nao"],
            modelo_gerado=MODELOS_DIR / "modelo_solo.keras",
        )

        return metricas
