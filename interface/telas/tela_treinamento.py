import os
import shutil
import uuid
import customtkinter as ctk
from tkinter import filedialog, messagebox

from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_treinamento_resumo import CardTreinamentoResumo
from interface.componentes.painel_treinamento import PainelTreinamento


class TelaTreinamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.pasta_potencial = os.path.join("data", "dataset", "potencial_aurifero")
        self.pasta_nao = os.path.join("data", "dataset", "nao_aurifero")
        self.pasta_modelos = os.path.join("data", "modelos")

        os.makedirs(self.pasta_potencial, exist_ok=True)
        os.makedirs(self.pasta_nao, exist_ok=True)
        os.makedirs(self.pasta_modelos, exist_ok=True)

        self.criar_layout()
        self.atualizar_status()

    def criar_layout(self):
        self.cabecalho = Cabecalho(
            self,
            "Treinar Modelo",
            "Prepare o dataset e acompanhe o status do modelo de IA."
        )
        self.cabecalho.pack(fill="x", pady=(0, 20))

        self.criar_cards_resumo()

        self.painel = PainelTreinamento(
            self,
            ao_adicionar_potencial=lambda: self.adicionar_imagens("potencial"),
            ao_adicionar_nao=lambda: self.adicionar_imagens("nao"),
            ao_atualizar=self.atualizar_status,
            ao_treinar=self.treinar_modelo
        )
        self.painel.pack(fill="x")

    def criar_cards_resumo(self):
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=(0, 20))

        self.card_potencial = CardTreinamentoResumo(
            self.frame_cards,
            "Aurífero",
            "0"
        )
        self.card_potencial.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.card_nao = CardTreinamentoResumo(
            self.frame_cards,
            "Não Aurífero",
            "0"
        )
        self.card_nao.pack(side="left", expand=True, fill="x", padx=6)

        self.card_total = CardTreinamentoResumo(
            self.frame_cards,
            "Total",
            "0"
        )
        self.card_total.pack(side="left", expand=True, fill="x", padx=6)

        self.card_modelo = CardTreinamentoResumo(
            self.frame_cards,
            "Modelo",
            "Não"
        )
        self.card_modelo.pack(side="left", expand=True, fill="x", padx=(6, 0))

    def adicionar_imagens(self, classe):
        caminhos = filedialog.askopenfilenames(
            title="Selecionar imagens",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png")
            ]
        )

        if not caminhos:
            return

        pasta = self.pasta_potencial if classe == "potencial" else self.pasta_nao
        copiadas = 0

        for caminho in caminhos:
            try:
                ext = os.path.splitext(caminho)[1]
                nome = f"{uuid.uuid4().hex}{ext}"
                destino = os.path.join(pasta, nome)

                shutil.copy2(caminho, destino)
                copiadas += 1
            except Exception as erro:
                print(f"Erro ao copiar imagem: {erro}")

        self.atualizar_status()

        messagebox.showinfo(
            "Sucesso",
            f"{copiadas} imagem(ns) adicionadas."
        )

    def contar_imagens(self, pasta):
        if not os.path.exists(pasta):
            return 0

        return len([
            arq for arq in os.listdir(pasta)
            if arq.lower().endswith((".jpg", ".jpeg", ".png"))
        ])

    def atualizar_status(self):
        total_p = self.contar_imagens(self.pasta_potencial)
        total_n = self.contar_imagens(self.pasta_nao)
        total = total_p + total_n

        caminho_modelo = os.path.join(
            self.pasta_modelos,
            "modelo_solo.pkl"
        )

        treinado = os.path.exists(caminho_modelo)

        self.card_potencial.atualizar_valor(total_p)
        self.card_nao.atualizar_valor(total_n)
        self.card_total.atualizar_valor(total)
        self.card_modelo.atualizar_valor("Sim" if treinado else "Não")

        self.painel.atualizar_status_modelo(treinado)

    def treinar_modelo(self):
        self.painel.iniciar_treinamento()

        self.after(800, lambda: self.painel.progresso(0.65))
        self.after(1500, lambda: self.painel.progresso(0.90))
        self.after(2200, self.finalizar_treinamento)

    def finalizar_treinamento(self):
        self.painel.finalizar_treinamento()

        messagebox.showinfo(
            "Treinamento",
            "Modelo treinado com sucesso (simulado)."
        )