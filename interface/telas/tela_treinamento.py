import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from controller.treinamento_controller import TreinamentoController
from interface.componentes.cabecalho import Cabecalho
from interface.componentes.card_treinamento_resumo import CardTreinamentoResumo
from interface.componentes.painel_treinamento import PainelTreinamento


class TelaTreinamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        TreinamentoController.preparar_pastas()

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

        self.card_potencial = CardTreinamentoResumo(self.frame_cards, "Aurífero", "0")
        self.card_potencial.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.card_nao = CardTreinamentoResumo(self.frame_cards, "Não Aurífero", "0")
        self.card_nao.pack(side="left", expand=True, fill="x", padx=6)

        self.card_total = CardTreinamentoResumo(self.frame_cards, "Total", "0")
        self.card_total.pack(side="left", expand=True, fill="x", padx=6)

        self.card_modelo = CardTreinamentoResumo(self.frame_cards, "Modelo", "Não")
        self.card_modelo.pack(side="left", expand=True, fill="x", padx=(6, 0))

    def adicionar_imagens(self, classe):
        caminhos = filedialog.askopenfilenames(
            title="Selecionar imagens",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
        )

        if not caminhos:
            return

        copiadas = TreinamentoController.adicionar_imagens(classe, caminhos)
        self.atualizar_status()

        messagebox.showinfo(
            "Sucesso",
            f"{copiadas} imagem(ns) adicionadas."
        )

    def obter_modelo_selecionado(self):
        if hasattr(self, "painel"):
            return self.painel.obter_modelo_selecionado()
        return "EfficientNetB0"

    def atualizar_status(self):
        modelo = self.obter_modelo_selecionado()
        resumo = TreinamentoController.obter_resumo(modelo)

        self.card_potencial.atualizar_valor(resumo["total_potencial"])
        self.card_nao.atualizar_valor(resumo["total_nao"])
        self.card_total.atualizar_valor(resumo["total"])
        self.card_modelo.atualizar_valor(f"{modelo}: {'Sim' if resumo['treinado'] else 'Não'}")

        self.painel.atualizar_status_modelo(resumo["treinado"])

    def treinar_modelo(self):
        if not TreinamentoController.validar_dataset(minimo_por_classe=20):
            messagebox.showwarning(
                "Dataset insuficiente",
                "Adicione pelo menos 20 imagens em cada classe antes de treinar."
            )
            return

        self.painel.iniciar_treinamento()
        self.painel.progresso(0.20)

        thread = threading.Thread(target=self.executar_treinamento, daemon=True)
        thread.start()

    def executar_treinamento(self):
        try:
            modelo = self.obter_modelo_selecionado()
            metricas = TreinamentoController.treinar_modelo(modelo=modelo, epocas=10)
            self.after(0, lambda: self.finalizar_treinamento(metricas))
        except Exception as erro:
            self.after(0, lambda: self.erro_treinamento(str(erro)))

    def finalizar_treinamento(self, metricas):
        self.painel.finalizar_treinamento()
        self.atualizar_status()

        mensagem = (
            f"Modelo {metricas.get('modelo', self.obter_modelo_selecionado())} treinado com sucesso!\n\n"
            f"Acurácia: {metricas['accuracy'] * 100:.2f}%\n"
            f"Precisão: {metricas['precision'] * 100:.2f}%\n"
            f"Recall: {metricas['recall'] * 100:.2f}%\n"
            f"F1-score: {metricas['f1_score'] * 100:.2f}%"
        )

        messagebox.showinfo("Treinamento concluído", mensagem)

    def erro_treinamento(self, erro):
        self.painel.atualizar_status_modelo(False)
        messagebox.showerror("Erro no treinamento", erro)
