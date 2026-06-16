from negocio.dataset_service import DatasetService


class DatasetController:

    @staticmethod
    def obter_resumo_dataset():
        return DatasetService.obter_resumo_dataset()