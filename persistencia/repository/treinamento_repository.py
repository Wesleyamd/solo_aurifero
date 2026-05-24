from persistencia.database.conexao import ConexaoBanco


class TreinamentoRepository:
    @staticmethod
    def salvar(total_potencial, total_nao_aurifero, modelo_gerado):
        total_imagens = total_potencial + total_nao_aurifero

        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO treinamentos (
                total_potencial,
                total_nao_aurifero,
                total_imagens,
                modelo_gerado
            )
            VALUES (?, ?, ?, ?)
        """, (
            total_potencial,
            total_nao_aurifero,
            total_imagens,
            str(modelo_gerado) if modelo_gerado else None
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def ultimo_treinamento():
        conn = ConexaoBanco.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT total_potencial, total_nao_aurifero, total_imagens, modelo_gerado, data_treinamento
            FROM treinamentos
            ORDER BY id DESC
            LIMIT 1
        """)

        resultado = cursor.fetchone()
        conn.close()
        return resultado

    @staticmethod
    def modelo_treinado():
        ultimo = TreinamentoRepository.ultimo_treinamento()
        return ultimo is not None
