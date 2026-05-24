from persistencia.database.init_db import inicializar_banco
from interface.app import App

if __name__ == "__main__":
    inicializar_banco()

    app = App()
    app.run()