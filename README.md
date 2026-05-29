#  Solo Aurífero

Sistema de análise de imagens de solo com potencial aurífero

---

##  Descrição

O **Solo Aurífero** é um sistema desktop desenvolvido em Python com o objetivo de analisar imagens de solo e indicar, de forma inicial, o potencial aurífero com base em características visuais.

O projeto faz parte do Trabalho de Conclusão de Curso (TCC) em Engenharia da Computação e tem como foco o uso de **visão computacional** e futuramente **aprendizado de máquina**.

---

##  Objetivos

* Analisar imagens de solo
* Identificar padrões visuais relevantes
* Classificar o solo quanto ao potencial aurífero
* Armazenar histórico de análises
* Evoluir para um modelo de IA treinado

---

## Tecnologias Utilizadas

* **Python** – linguagem principal de desenvolvimento.
* **CustomTkinter** – construção da interface gráfica moderna e responsiva.
* **TensorFlow / Keras** – treinamento e inferência dos modelos de Deep Learning.
* **EfficientNetB0** – modelo principal utilizado para classificação de imagens de solo.
* **MobileNetV2** – modelo utilizado para comparação experimental de desempenho.
* **OpenCV** – processamento e análise de imagens.
* **SQLite** – armazenamento local de dados e histórico de análises.
* **Pillow (PIL)** – manipulação e exibição de imagens.
* **NumPy** – operações numéricas e manipulação de matrizes.
* **Git e GitHub** – versionamento e gerenciamento do código-fonte.


---

##  Estrutura do projeto

O sistema segue uma estrutura modular organizada em camadas,
separando responsabilidades entre interface, regras de negócio,
inteligência artificial e persistência de dados.

```
solo_aurifero/
├── controller/           # Controladores responsáveis pelo fluxo da aplicação
│   ├── analise_controller.py
│   ├── historico_controller.py
│   └── treinamento_controller.py
│
├── ia/                   # Módulos de Inteligência Artificial
│   ├── preprocessamento.py
│   ├── extracao_caracteristicas.py
│   ├── treinamento.py
│   └── classificacao.py
│
├── interface/            # Interface gráfica do sistema
│   ├── telas/
│   ├── componentes/
│   ├── tema/
│   ├── app.py
│   └── janela_principal.py
│
├── negocio/              # Regras de negócio da aplicação
│   ├── analise_service.py
│   ├── treinamento_service.py
│   ├── historico_service.py
│   └── arquivo_service.py
│
├── persistencia/         # Camada de persistência de dados
│   ├── database/
│   ├── model/
│   ├── repository/
│   └── data/
│
├── docs/                 # Documentação do projeto
│
└── main.py               # Ponto de entrada da aplicação
```

---


### Diagrama de Casos de Uso (DCU)
![DCU](docs/DCU.png)

### Diagrama de Classes (DCL)
![DCL](docs/DCL.png)

##  Funcionalidades atuais

* Seleção de imagem
* Preview da imagem (com redimensionamento proporcional)
* Análise inicial (simples)
* Armazenamento das análises no banco
* Histórico com:

  * preview da imagem
  * resultado
  * data da análise
* Exclusão de análises
* Remoção automática da imagem salva

---

## 🖥 Interface

O sistema possui:

* Menu lateral moderno
* Tela de análise
* Tela de histórico
* Tela de treinamento (em desenvolvimento)

---

## ▶️ Como executar o projeto

### 1. Clonar o repositório

```
git clone https://github.com/Wesleyamd/solo_aurifero.git
```

### 2. Acessar a pasta

```
cd solo_aurifero
```

### 3. Criar ambiente virtual

```
python -m venv .venv
```

### 4. Ativar o ambiente

Windows:

```
.venv\Scripts\activate
```

### 5. Instalar dependências

```
pip install -r requirements.txt
```

### 6. Executar o sistema

```
python main.py
```

---

##  Estrutura de dados

As imagens analisadas são copiadas automaticamente para:

```
data/analise/
```

O banco de dados fica em:

```
data/banco/solo.db
```

---

## Funcionalidades Futuras

* Comparação entre diferentes arquiteturas de Deep Learning (EfficientNetB0, MobileNetV2 e outras).
* Ampliação da base de dados com imagens coletadas em diferentes regiões.
* Implementação de mapas de calor para interpretação visual das classificações.
* Geração automática de relatórios das análises realizadas.
* Exportação de resultados para PDF e planilhas.
* Integração com Firebase para armazenamento em nuvem.
* Desenvolvimento de aplicativo móvel para consulta das análises.
* Dashboard avançado com métricas de treinamento e desempenho dos modelos.
* Inclusão de novas classes de solo para aumentar a capacidade de generalização do sistema.
* Integração com dados geológicos e geoespaciais provenientes de bases públicas.


##  Autor

**Wesley Carvalho das Neves**
Engenharia da Computação - IFMT

---

##  Licença

Este projeto é acadêmico e está sendo desenvolvido para fins educacionais.
