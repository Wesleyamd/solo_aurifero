class AnaliseService:
    @staticmethod
    def analisar_cor(caminho_imagem):
        if caminho_imagem:
            return "Imagem carregada com sucesso"
        return "Nenhuma imagem selecionada"