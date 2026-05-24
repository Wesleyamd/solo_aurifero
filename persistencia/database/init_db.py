from persistencia.database.conexao import ConexaoBanco
from utils.caminhos import criar_pastas_base


def inicializar_banco():
    criar_pastas_base()

    conn = ConexaoBanco.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_analise TEXT,
            caminho_imagem TEXT NOT NULL,
            resultado TEXT NOT NULL,
            data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treinamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_potencial INTEGER NOT NULL DEFAULT 0,
            total_nao_aurifero INTEGER NOT NULL DEFAULT 0,
            total_imagens INTEGER NOT NULL DEFAULT 0,
            modelo_gerado TEXT,
            data_treinamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migração simples para bancos antigos já criados sem a coluna nome_analise.
    cursor.execute("PRAGMA table_info(analises)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "nome_analise" not in colunas:
        cursor.execute("ALTER TABLE analises ADD COLUMN nome_analise TEXT")

    conn.commit()
    conn.close()
