import os
import shutil
import uuid
import customtkinter as ctk
from tkinter import filedialog, messagebox

from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_resultado import CardResultado
from interface.tema.cores import Cores


class TelaTreinamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.pasta_potencial = os.path.join("data", "dataset", "potencial_aurifero")
        self.pasta_nao = os.path.join("data", "dataset", "nao_aurifero")
        self.pasta_modelos = os.path.join("data", "modelos")

        os.makedirs(self.pasta_potencial, exist_ok=True)
        os.makedirs(self.pasta_nao, exist_ok=True)
        os.makedirs(self.pasta_modelos, exist_ok=True)

        self.cabecalho = Cabecalho(
            self,
            "Treinar Modelo",
            "Prepare o dataset e acompanhe o status do modelo de IA."
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        self.card_info = CardResultado(
            self,
            "Treinamento do Modelo",
            "Adicione imagens nas duas classes: solo com potencial aurífero e solo sem potencial aurífero."
        )
        self.card_info.pack(fill="x", pady=(0, 20))

        self.card_status = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=Cores.FUNDO_CARD,
            border_width=1,
            border_color=Cores.BORDA
        )
        self.card_status.pack(fill="x", pady=(0, 20))

        self.titulo_status = ctk.CTkLabel(
            self.card_status,
            text="Status do Dataset",
            font=("Arial", 18, "bold"),
            text_color=Cores.TEXTO_PRINCIPAL
        )
        self.titulo_status.pack(anchor="w", padx=20, pady=(18, 8))

        self.label_potencial = ctk.CTkLabel(
            self.card_status,
            text="Potencial aurífero: 0 imagens",
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_potencial.pack(anchor="w", padx=20, pady=3)

        self.label_nao = ctk.CTkLabel(
            self.card_status,
            text="Não aurífero: 0 imagens",
            font=("Arial", 14),
            text_color=Cores.TEXTO_SECUNDARIO
        )
        self.label_nao.pack(anchor="w", padx=20, pady=3)

        self.label_modelo = ctk.CTkLabel(
            self.card_status,
            text="Modelo: Não treinado",
            font=("Arial", 15, "bold"),
            text_color="#c94f4f"
        )
        self.label_modelo.pack(anchor="w", padx=20, pady=(10, 18))

        self.frame_botoes_dataset = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes_dataset.pack(fill="x", pady=(0, 15))

        self.botao_add_potencial = ctk.CTkButton(
            self.frame_botoes_dataset,
            text="Adicionar imagens — Potencial aurífero",
            height=42,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=lambda: self.adicionar_imagens("potencial")
        )
        self.botao_add_potencial.pack(side="left", padx=(0, 10))

        self.botao_add_nao = ctk.CTkButton(
            self.frame_botoes_dataset,
            text="Adicionar imagens — Não aurífero",
            height=42,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=lambda: self.adicionar_imagens("nao")
        )
        self.botao_add_nao.pack(side="left")

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(fill="x")

        self.botao_atualizar = ctk.CTkButton(
            self.frame_botoes,
            text="Atualizar Status",
            height=42,
            corner_radius=12,
            command=self.atualizar_status
        )
        self.botao_atualizar.pack(side="left")

        self.botao_treinar = ctk.CTkButton(
            self.frame_botoes,
            text="Treinar Modelo",
            height=42,
            corner_radius=12,
            fg_color=Cores.DESTAQUE,
            hover_color=Cores.DESTAQUE_HOVER,
            text_color="#111111",
            command=self.treinar_modelo
        )
        self.botao_treinar.pack(side="right")

        self.atualizar_status()

    def adicionar_imagens(self, classe):
        caminhos = filedialog.askopenfilenames(
            title="Selecionar imagens",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminhos:
            return

        pasta_destino = self.pasta_potencial if classe == "potencial" else self.pasta_nao
        copiadas = 0

        for caminho_origem in caminhos:
            try:
                extensao = os.path.splitext(caminho_origem)[1].lower()
                nome_arquivo = f"{classe}_{uuid.uuid4().hex}{extensao}"
                caminho_destino = os.path.join(pasta_destino, nome_arquivo)

                shutil.copy2(caminho_origem, caminho_destino)
                copiadas += 1

            except Exception as erro:
                print(f"Erro ao copiar imagem: {erro}")

        self.atualizar_status()

        messagebox.showinfo(
            "Imagens adicionadas",
            f"{copiadas} imagem(ns) copiadas para o dataset."
        )

    def contar_imagens(self, pasta):
        if not os.path.exists(pasta):
            return 0

        extensoes = (".jpg", ".jpeg", ".png")
        return len([
            arquivo for arquivo in os.listdir(pasta)
            if arquivo.lower().endswith(extensoes)
        ])

    def atualizar_status(self):
        caminho_modelo = os.path.join(self.pasta_modelos, "modelo_solo.pkl")

        total_potencial = self.contar_imagens(self.pasta_potencial)
        total_nao = self.contar_imagens(self.pasta_nao)

        self.label_potencial.configure(
            text=f"Potencial aurífero: {total_potencial} imagens"
        )

        self.label_nao.configure(
            text=f"Não aurífero: {total_nao} imagens"
        )

        if os.path.exists(caminho_modelo):
            self.label_modelo.configure(
                text="Modelo: Treinado",
                text_color="#4caf50"
            )
        else:
            self.label_modelo.configure(
                text="Modelo: Não treinado",
                text_color="#c94f4f"
            )

    def treinar_modelo(self):
        self.label_modelo.configure(
            text="Treinamento ainda não implementado",
            text_color="#e0bb5c"
        )