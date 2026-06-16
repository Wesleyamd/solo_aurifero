from persistencia.repository.dataset_repository import DatasetRepository


class DatasetService:

    @staticmethod
    def obter_resumo_dataset():
        return DatasetRepository.resumo_dataset()