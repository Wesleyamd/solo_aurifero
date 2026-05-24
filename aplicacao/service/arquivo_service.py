import os
import shutil
from datetime import datetime

from utils.caminhos import ANALISE_DIR


class ArquivoService:
    @staticmethod
    def salvar_copia_imagem(caminho_origem):
        ANALISE_DIR.mkdir(parents=True, exist_ok=True)

        nome_original = os.path.basename(caminho_origem)
        nome_base, extensao = os.path.splitext(nome_original)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        novo_nome = f"{nome_base}_{timestamp}{extensao}"

        caminho_destino = ANALISE_DIR / novo_nome

        shutil.copy2(caminho_origem, caminho_destino)

        return str(caminho_destino)
