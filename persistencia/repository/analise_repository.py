import os
from pathlib import Path

from persistencia.database.conexao import ConexaoBanco
from utils.caminhos import ANALISE_DIR


class AnaliseRepository:

    @staticmethod
    def salvar(nome_analise, caminho_imagem, resultado, data=None):
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        if data:
            cursor.execute("""
                INSERT INTO analises
                (nome_analise, caminho_imagem, resultado, data_analise)
                VALUES (?, ?, ?, ?)
            """, (
                nome_analise,
                str(caminho_imagem),
                resultado,
                data
            ))
        else:
            cursor.execute("""
                INSERT INTO analises
                (nome_analise, caminho_imagem, resultado)
                VALUES (?, ?, ?)
            """, (
                nome_analise,
                str(caminho_imagem),
                resultado
            ))

        conn.commit()
        conn.close()

    @staticmethod
    def listar_todas():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome_analise, caminho_imagem, resultado, data_analise
            FROM analises
            ORDER BY id DESC
        """)

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def listar_ultimas(limite=3):
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome_analise, caminho_imagem, resultado, data_analise
            FROM analises
            ORDER BY id DESC
            LIMIT ?
        """, (limite,))

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

        caminho_imagem = registro[0] if registro else None

        cursor.execute(
            "DELETE FROM analises WHERE id = ?",
            (analise_id,)
        )

        conn.commit()
        conn.close()

        if caminho_imagem:
            try:
                caminho_absoluto = Path(caminho_imagem).resolve()
                pasta_absoluta = ANALISE_DIR.resolve()

                if str(caminho_absoluto).startswith(str(pasta_absoluta)) and caminho_absoluto.exists():
                    os.remove(caminho_absoluto)
                    print(f"Imagem removida: {caminho_absoluto}")
                else:
                    print(f"Arquivo não removido: {caminho_absoluto}")
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
    def eh_resultado_com_potencial(resultado):
        if not resultado:
            return False

        resultado_normalizado = resultado.strip().lower()

        # Importante: não usar apenas "potencial" porque
        # "Sem Potencial Aurífero" também possui essa palavra.
        return (
            resultado_normalizado.startswith("possível potencial")
            or resultado_normalizado.startswith("possivel potencial")
            or resultado_normalizado.startswith("solo com potencial")
            or resultado_normalizado == "com potencial aurífero"
            or resultado_normalizado == "com potencial aurifero"
        )

    @staticmethod
    def contar_potencial():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT resultado FROM analises")
        resultados = cursor.fetchall()

        conn.close()

        return sum(
            1 for (resultado,) in resultados
            if AnaliseRepository.eh_resultado_com_potencial(resultado)
        )

    @staticmethod
    def percentual_potencial():
        total = AnaliseRepository.contar()
        if total == 0:
            return "0%"

        potencial = AnaliseRepository.contar_potencial()
        percentual = (potencial / total) * 100
        return f"{percentual:.0f}%"

    @staticmethod
    def ultimo_resultado():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT resultado
            FROM analises
            ORDER BY id DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]
        return "-"
