from database.conexao import ConexaoBanco


def inicializar_banco():
    conn = ConexaoBanco.conectar()
    cursor = conn.cursor()

    # 🔹 Tabela de análises
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caminho_imagem TEXT NOT NULL,
            resultado TEXT NOT NULL,
            data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()