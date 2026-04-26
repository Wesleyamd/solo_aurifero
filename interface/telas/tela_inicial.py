import customtkinter as ctk
from interface.tema.cores import Cores
from interface.componentes.grid_status import GridStatus
from interface.componentes.resumo_sistema import ResumoSistema
from interface.componentes.lista_analises import ListaAnalises
from interface.componentes.banner_inicial import BannerInicial
from interface.componentes.rodape import Rodape


class TelaInicial(ctk.CTkFrame):
    def __init__(self, master, controlador=None):
        super().__init__(master, fg_color=Cores.FUNDO)
        self.controlador = controlador
        self.img_banner = None
        self.criar_grid_status()
        self.grid_columnconfigure(0, weight=1)

        self.criar_banner()
        self.criar_area_inferior()
        self.criar_rodape()

    def criar_banner(self):
        banner = BannerInicial(self, self.abrir_analise)
        banner.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 16))


    def criar_grid_status(self):
        grid = GridStatus(self)
        grid.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 16))


    def criar_area_inferior(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 16))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.criar_ultimas_analises(frame)
        self.criar_resumo_sistema(frame)

    def criar_ultimas_analises(self, master):
        lista = ListaAnalises(master)
        lista.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    def criar_resumo_sistema(self, master):
        resumo = ResumoSistema(master)
        resumo.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    def criar_rodape(self):
        rodape = Rodape(self)
        rodape.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 20))


    def abrir_analise(self):
        if self.controlador:
            self.controlador("analise")