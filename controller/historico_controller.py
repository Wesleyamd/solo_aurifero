from persistencia.repository.analise_repository import AnaliseRepository


class HistoricoController:
    """Controla as operações da tela de histórico."""

    @staticmethod
    def listar():
        return AnaliseRepository.listar_todas()

    @staticmethod
    def excluir(analise_id):
        AnaliseRepository.excluir(analise_id)

    @staticmethod
    def contar():
        return AnaliseRepository.contar()
