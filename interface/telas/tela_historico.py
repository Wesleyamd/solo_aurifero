import os
import customtkinter as ctk
from PIL import Image

from interface.componentes.cabecalho import Cabecalho
from interface.tema.cores import Cores
from repository.analise_repository import AnaliseRepository


class TelaHistorico(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.imagens_preview = []
        self.imagem_modal = None
        self.janela_modal = None

        self.cabecalho = Cabecalho(
            self,
            "Histórico de Análises",
            "Visualize, abra e exclua análises salvas."
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        self.area_lista = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.area_lista.pack(fill="both", expand=True)

        self.carregar_historico()

    def carregar_historico(self):
        for widget in self.area_lista.winfo_children():
            widget.destroy()

        self.imagens_preview.clear()

        registros = AnaliseRepository.listar_todas()

        if not registros:
            vazio = ctk.CTkFrame(
                self.area_lista,
                corner_radius=18,
                fg_color=Cores.FUNDO_CARD,
                border_width=1,
                border_color=Cores.BORDA
            )
            vazio.pack(fill="x", padx=5, pady=10)

            label = ctk.CTkLabel(
                vazio,
                text="Nenhuma análise registrada até o momento.",
                text_color=Cores.TEXTO_SECUNDARIO,
                font=("Arial", 15)
            )
            label.pack(pady=25)
            return

        for analise_id, caminho_imagem, resultado, data_analise in registros:
            self.criar_card(analise_id, caminho_imagem, resultado, data_analise)

    def criar_card(self, analise_id, caminho_imagem, resultado, data_analise):
        card = ctk.CTkFrame(
            self.area_lista,
            corner_radius=18,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )
        card.pack(fill="x", pady=8, padx=5)

        frame_interno = ctk.CTkFrame(card, fg_color="transparent")
        frame_interno.pack(fill="x", padx=15, pady=15)

        # Preview com bordas arredondadas
        frame_preview = ctk.CTkFrame(
            frame_interno,
            width=230,
            height=170,
            corner_radius=16,
            fg_color=Cores.FUNDO_APP,
            border_width=1,
            border_color=Cores.BORDA
        )
        frame_preview.pack(side="left", padx=(0, 15))
        frame_preview.pack_propagate(False)

        preview_label = ctk.CTkLabel(
            frame_preview,
            text="",
            cursor="hand2"
        )
        preview_label.place(relx=0.5, rely=0.5, anchor="center")

        imagem_preview = self.criar_preview(caminho_imagem)
        if imagem_preview:
            preview_label.configure(image=imagem_preview)
            preview_label.bind(
                "<Button-1>",
                lambda event, caminho=caminho_imagem: self.abrir_modal_imagem(caminho)
            )
            self.imagens_preview.append(imagem_preview)
        else:
            preview_label.configure(
                text="Sem preview",
                text_color=Cores.TEXTO_SECUNDARIO,
                font=("Arial", 12)
            )

        # Informações
        frame_info = ctk.CTkFrame(frame_interno, fg_color="transparent")
        frame_info.pack(side="left", fill="both", expand=True)

        nome_arquivo = os.path.basename(caminho_imagem)

        titulo = ctk.CTkLabel(
            frame_info,
            text=nome_arquivo,
            font=("Arial", 17, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        titulo.pack(anchor="w")

        badge_frame = ctk.CTkFrame(
            frame_info,
            corner_radius=12,
            fg_color=self.cor_resultado_fundo(resultado)
        )
        badge_frame.pack(anchor="w", pady=(8, 8))

        badge = ctk.CTkLabel(
            badge_frame,
            text=resultado,
            font=("Arial", 12, "bold"),
            text_color=self.cor_resultado_texto(resultado)
        )
        badge.pack(padx=10, pady=4)

        caminho_label = ctk.CTkLabel(
            frame_info,
            text=f"Caminho: {caminho_imagem}",
            font=("Arial", 12),
            text_color=Cores.TEXTO_SECUNDARIO,
            wraplength=650,
            justify="left"
        )
        caminho_label.pack(anchor="w", pady=(0, 4))

        data_label = ctk.CTkLabel(
            frame_info,
            text=f"Data: {self.formatar_data(data_analise)}",
            font=("Arial", 13),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        data_label.pack(anchor="w", pady=(0, 10))

        # Botões
        frame_botoes = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_botoes.pack(anchor="w", pady=(5, 0))

        btn_ver = ctk.CTkButton(
            frame_botoes,
            text="Abrir imagem",
            width=120,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=lambda caminho=caminho_imagem: self.abrir_modal_imagem(caminho)
        )
        btn_ver.pack(side="left", padx=(0, 10))

        btn_excluir = ctk.CTkButton(
            frame_botoes,
            text="Excluir",
            width=100,
            corner_radius=12,
            fg_color="#7a2e2e",
            hover_color="#9a3a3a",
            command=lambda aid=analise_id: self.excluir_analise(aid)
        )
        btn_excluir.pack(side="left")

    def criar_preview(self, caminho_imagem):
        try:
            imagem = Image.open(caminho_imagem)
            imagem.thumbnail((220, 160))

            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )
        except Exception:
            return None

    def abrir_modal_imagem(self, caminho_imagem):
        try:
            if self.janela_modal and self.janela_modal.winfo_exists():
                self.janela_modal.destroy()

            self.janela_modal = ctk.CTkToplevel(self)
            self.janela_modal.title("Visualizar Imagem")
            self.janela_modal.geometry("1000x700")
            self.janela_modal.transient(self)
            self.janela_modal.grab_set()

            frame = ctk.CTkFrame(
                self.janela_modal,
                fg_color=Cores.FUNDO_APP
            )
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            titulo = ctk.CTkLabel(
                frame,
                text=os.path.basename(caminho_imagem),
                font=("Arial", 20, "bold"),
                text_color=Cores.TEXTO_PRINCIPAL
            )
            titulo.pack(pady=(10, 20))

            imagem = Image.open(caminho_imagem)
            imagem.thumbnail((900, 550))

            self.imagem_modal = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )

            label_imagem = ctk.CTkLabel(frame, text="", image=self.imagem_modal)
            label_imagem.pack(expand=True)

            btn_fechar = ctk.CTkButton(
                frame,
                text="Fechar",
                width=120,
                command=self.janela_modal.destroy
            )
            btn_fechar.pack(pady=20)

        except Exception:
            pass

    def excluir_analise(self, analise_id):
        AnaliseRepository.excluir(analise_id)
        self.carregar_historico()

    def formatar_data(self, data_analise):
        try:
            data, hora = data_analise.split(" ")
            ano, mes, dia = data.split("-")
            return f"{dia}/{mes}/{ano} às {hora}"
        except Exception:
            return data_analise

    def cor_resultado_fundo(self, resultado):
        resultado = resultado.lower()

        if "possível" in resultado or "alto" in resultado:
            return "#2f2a1f"
        elif "baixo" in resultado:
            return "#3a2020"
        return "#1f2a3a"

    def cor_resultado_texto(self, resultado):
        resultado = resultado.lower()

        if "possível" in resultado or "alto" in resultado:
            return "#e0bb5c"
        elif "baixo" in resultado:
            return "#ff8a8a"
        return "#8ec5ff"