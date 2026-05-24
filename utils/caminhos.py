from pathlib import Path

# Raiz do projeto Solo Aurífero
BASE_DIR = Path(__file__).resolve().parent.parent

# Pastas principais de dados
DATA_DIR = BASE_DIR / "persistencia" / "data"
BANCO_DIR = DATA_DIR / "banco"
ANALISE_DIR = DATA_DIR / "analise"
DATASET_DIR = DATA_DIR / "dataset"
DATASET_POTENCIAL_DIR = DATASET_DIR / "potencial_aurifero"
DATASET_NAO_AURIFERO_DIR = DATASET_DIR / "nao_aurifero"
MODELOS_DIR = DATA_DIR / "modelos"

def criar_pastas_base():
    """Cria as pastas usadas pelo sistema, caso ainda não existam."""
    for pasta in [
        BANCO_DIR,
        ANALISE_DIR,
        DATASET_POTENCIAL_DIR,
        DATASET_NAO_AURIFERO_DIR,
        MODELOS_DIR,
    ]:
        pasta.mkdir(parents=True, exist_ok=True)
