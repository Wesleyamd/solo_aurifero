import os
from database.conexao import ConexaoBanco


class AnaliseRepository:
    @staticmethod
    def salvar(caminho_imagem, resultado):
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO analises (caminho_imagem, resultado)
            VALUES (?, ?)
        """, (caminho_imagem, resultado))

        conn.commit()
        conn.close()

    @staticmethod
    def listar_todas():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, caminho_imagem, resultado, data_analise
            FROM analises
            ORDER BY id DESC
        """)

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def excluir(analise_id):
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT caminho_imagem FROM analises WHERE id = ?",
            (analise_id,)
        )
        registro = cursor.fetchone()

        caminho_imagem = None
        if registro:
            caminho_imagem = registro[0]

        cursor.execute(
            "DELETE FROM analises WHERE id = ?",
            (analise_id,)
        )

        conn.commit()
        conn.close()

        if caminho_imagem:
            caminho_imagem = os.path.normpath(caminho_imagem)

            # segurança: só apaga se estiver dentro de data/analise
            pasta_analise = os.path.normpath(os.path.join("data", "analise"))

            try:
                caminho_absoluto = os.path.abspath(caminho_imagem)
                pasta_absoluta = os.path.abspath(pasta_analise)

                if caminho_absoluto.startswith(pasta_absoluta) and os.path.exists(caminho_absoluto):
                    os.remove(caminho_absoluto)
                    print(f"Imagem removida: {caminho_absoluto}")
                else:
                    print(f"Arquivo não removido. Caminho fora da pasta esperada ou inexistente: {caminho_absoluto}")
            except Exception as e:
                print(f"Erro ao remover imagem: {e}")

    @staticmethod
    def contar():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM analises")
        total = cursor.fetchone()[0]

        conn.close()
        return total

    @staticmethod
    def ultimo_resultado():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT resultado
                       FROM analises
                       ORDER BY id DESC LIMIT 1
                       """)

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]
        return "-"