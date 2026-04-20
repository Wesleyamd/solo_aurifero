# 🟡 Solo Aurífero

Sistema desktop para análise e 
classificação de solo com potencial aurífero 
utilizando visão computacional e inteligência 
artificial.

---

## 📌 Sobre o projeto

O projeto tem como objetivo analisar imagens de solo e identificar padrões que possam indicar a presença de ouro (solo aurífero), utilizando técnicas de processamento de imagem e aprendizado de máquina.

O sistema permite:
- Selecionar imagens de solo
- Processar imagens com OpenCV
- Extrair características (cor, textura, etc.)
- Classificar o solo (aurífero ou não aurífero)
- Armazenar histórico de análises
- Treinar novos modelos de classificação

---

## 🖥️ Tecnologias utilizadas

- Python
- CustomTkinter (interface gráfica)
- OpenCV (processamento de imagem)
- NumPy
- SQLite (banco de dados)

---

## 🧠 Funcionalidades

- 📸 Seleção de imagem
- 🔍 Análise de solo
- 📊 Exibição de resultados
- 💾 Histórico de análises
- 🤖 Treinamento de modelo de IA

---

## 📂 Estrutura do projeto

```bash
solo_aurifero/
├── interface/
├── controller/
├── service/
├── model/
├── ia/
├── repository/
├── database/
├── assets/
├── data/
└── utils/