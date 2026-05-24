from ia.extracao_caracteristicas import extrair_caracteristicas


class AnaliseService:
    @staticmethod
    def analisar_cor(caminho_imagem):
        if not caminho_imagem:
            return "Nenhuma imagem selecionada"

        caracteristicas = extrair_caracteristicas(caminho_imagem)

        media_h = caracteristicas[0]
        media_s = caracteristicas[1]
        media_v = caracteristicas[2]

        # Regra inicial simples para protótipo:
        # solos mais amarelados/alaranjados, com saturação e brilho moderados,
        # recebem indicação de possível potencial.
        if 10 <= media_h <= 45 and media_s >= 35 and media_v >= 50:
            return "Possível Potencial Aurífero"

        return "Sem Potencial Aurífero"
