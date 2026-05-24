import os
import customtkinter as ctk
from PIL import Image

from interface.tema.cores import Cores
from interface.componentes.modal_imagem import ModalImagem


class CardHistorico(ctk.CTkFrame):
    def __init__(
        self,
        master,
        analise_id,
        nome_analise,
        caminho_imagem,
        resultado,
        data_analise,
        ao_excluir
    ):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )

        self.analise_id = analise_id
        self.nome_analise = nome_analise or os.path.basename(caminho_imagem)
        self.caminho_imagem = caminho_imagem
        self.resultado = resultado
        self.data_analise = data_analise
        self.ao_excluir = ao_excluir
        self.imagem_preview = None

        self.criar_layout()

    def criar_layout(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=16, pady=16)

        self.criar_preview(frame)
        self.criar_info(frame)

    def criar_preview(self, master):
        frame_preview = ctk.CTkFrame(
            master,
            width=190,
            height=135,
            corner_radius=18,
            fg_color=Cores.FUNDO_APP,
            border_width=1,
            border_color=Cores.BORDA
        )
        frame_preview.pack(side="left", padx=(0, 18))
        frame_preview.pack_propagate(False)

        label = ctk.CTkLabel(
            frame_preview,
            text="",
            cursor="hand2"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.imagem_preview = self.gerar_preview()

        if self.imagem_preview:
            label.configure(image=self.imagem_preview)
            label.bind(
                "<Button-1>",
                lambda event: self.abrir_imagem()
            )
        else:
            label.configure(
                text="Sem preview",
                text_color=Cores.TEXTO_SECUNDARIO,
                font=("Arial", 12)
            )

    def criar_info(self, master):
        frame_info = ctk.CTkFrame(master, fg_color="transparent")
        frame_info.pack(side="left", fill="both", expand=True)

        nome_arquivo = os.path.basename(self.caminho_imagem)

        titulo = ctk.CTkLabel(
            frame_info,
            text=self.nome_analise,
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        titulo.pack(anchor="w")

        arquivo = ctk.CTkLabel(
            frame_info,
            text=f"Imagem: {nome_arquivo}",
            font=("Arial", 12),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        arquivo.pack(anchor="w", pady=(3, 0))

        badge_frame = ctk.CTkFrame(
            frame_info,
            corner_radius=14,
            fg_color=self.cor_resultado_fundo()
        )
        badge_frame.pack(anchor="w", pady=(8, 8))

        badge = ctk.CTkLabel(
            badge_frame,
            text=self.resultado,
            font=("Arial", 12, "bold"),
            text_color=self.cor_resultado_texto()
        )
        badge.pack(padx=12, pady=5)

        data = ctk.CTkLabel(
            frame_info,
            text=f"📅 {self.formatar_data()}",
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        data.pack(anchor="w", pady=(0, 5))

        caminho = ctk.CTkLabel(
            frame_info,
            text=f"📁 {self.caminho_imagem}",
            font=("Arial", 12),
            text_color=Cores.TEXTO_SECUNDARIO,
            wraplength=700,
            justify="left"
        )
        caminho.pack(anchor="w", pady=(0, 10))

        self.criar_botoes(frame_info)

    def criar_botoes(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.pack(anchor="w", pady=(4, 0))

        btn_abrir = ctk.CTkButton(
            frame,
            text="Abrir imagem",
            width=130,
            height=34,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            font=("Arial", 12, "bold"),
            command=self.abrir_imagem
        )
        btn_abrir.pack(side="left", padx=(0, 10))

        btn_excluir = ctk.CTkButton(
            frame,
            text="Excluir",
            width=110,
            height=34,
            corner_radius=12,
            fg_color="#7f2d2d",
            hover_color="#a33434",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=lambda: self.ao_excluir(self.analise_id)
        )
        btn_excluir.pack(side="left")

    def gerar_preview(self):
        try:
            imagem = Image.open(self.caminho_imagem)
            imagem.thumbnail((175, 120))

            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )
        except Exception:
            return None

    def abrir_imagem(self):
        ModalImagem(self, self.caminho_imagem).abrir()

    def formatar_data(self):
        try:
            data, hora = self.data_analise.split(" ")
            ano, mes, dia = data.split("-")
            return f"{dia}/{mes}/{ano} às {hora}"
        except Exception:
            return self.data_analise

    def cor_resultado_fundo(self):
        resultado = self.resultado.lower()

        if "possível" in resultado or "possivel" in resultado or "solo com potencial" in resultado:
            return "#2f2a1f"

        if "sem potencial" in resultado or "baixo" in resultado:
            return "#3a2020"

        return "#1f2a3a"

    def cor_resultado_texto(self):
        resultado = self.resultado.lower()

        if "possível" in resultado or "possivel" in resultado or "solo com potencial" in resultado:
            return "#e0bb5c"

        if "sem potencial" in resultado or "baixo" in resultado:
            return "#ff8a8a"

        return "#8ec5ff"