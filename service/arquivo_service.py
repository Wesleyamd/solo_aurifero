import os
import shutil
from datetime import datetime


class ArquivoService:
    @staticmethod
    def salvar_copia_imagem(caminho_origem):
        pasta_destino = os.path.join("data", "analise")
        os.makedirs(pasta_destino, exist_ok=True)

        nome_original = os.path.basename(caminho_origem)
        nome_base, extensao = os.path.splitext(nome_original)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        novo_nome = f"{nome_base}_{timestamp}{extensao}"

        caminho_destino = os.path.join(pasta_destino, novo_nome)

        shutil.copy2(caminho_origem, caminho_destino)

        return caminho_destino