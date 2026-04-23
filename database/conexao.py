import sqlite3
import os


class ConexaoBanco:
    @staticmethod
    def conectar():
        pasta = os.path.join("data", "banco")
        os.makedirs(pasta, exist_ok=True)

        caminho = os.path.join(pasta, "solo.db")
        return sqlite3.connect(caminho)