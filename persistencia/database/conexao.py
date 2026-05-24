import sqlite3
from utils.caminhos import BANCO_DIR


class ConexaoBanco:
    CAMINHO_BANCO = BANCO_DIR / "solo.db"

    @staticmethod
    def conectar():
        BANCO_DIR.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(ConexaoBanco.CAMINHO_BANCO)
