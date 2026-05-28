from datetime import datetime

from negocio.arquivo_service import ArquivoService
from ia.classificacao import classificar_imagem
from persistencia.repository.analise_repository import AnaliseRepository


class AnaliseController:
    """Controla o fluxo de análise entre interface, IA e persistência."""

    @staticmethod
    def analisar(nome_analise, caminho_original):
        if not caminho_original:
            raise ValueError("Nenhuma imagem selecionada.")

        nome_analise = (nome_analise or "").strip()
        if not nome_analise:
            raise ValueError("Informe um nome para identificar esta análise.")

        caminho_copia = ArquivoService.salvar_copia_imagem(caminho_original)
        resultado, confianca, classe = classificar_imagem(caminho_copia)
        resultado_formatado = f"{resultado} - Confiança: {confianca}%"
        data_analise = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        AnaliseRepository.salvar(
            nome_analise,
            caminho_copia,
            resultado_formatado,
            data_analise,
        )

        return {
            "resultado": resultado_formatado,
            "resultado_base": resultado,
            "confianca": confianca,
            "classe": classe,
            "caminho_copia": caminho_copia,
            "tem_potencial": AnaliseRepository.eh_resultado_com_potencial(resultado_formatado),
        }

    @staticmethod
    def total_analises():
        return AnaliseRepository.contar()

    @staticmethod
    def ultimo_resultado():
        return AnaliseRepository.ultimo_resultado()
