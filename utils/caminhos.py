from pathlib import Path

# Raiz do projeto Solo_Aurifero.
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "persistencia" / "data"
DATASET_DIR = DATA_DIR / "dataset"
DATASET_POTENCIAL_DIR = DATASET_DIR / "potencial_aurifero"
DATASET_NAO_AURIFERO_DIR = DATASET_DIR / "nao_aurifero"

MODELOS_DIR = DATA_DIR / "modelos"
BANCO_DIR = DATA_DIR / "banco"
ANALISE_DIR = DATA_DIR / "analises"


def criar_pastas_base():
    """Cria as pastas principais usadas pela aplicação."""
    for pasta in [
        DATA_DIR,
        DATASET_DIR,
        DATASET_POTENCIAL_DIR,
        DATASET_NAO_AURIFERO_DIR,
        MODELOS_DIR,
        BANCO_DIR,
        ANALISE_DIR,
    ]:
        pasta.mkdir(parents=True, exist_ok=True)
