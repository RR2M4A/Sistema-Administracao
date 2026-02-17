# Sistema de Gestão de Atendimentos - Administração Regional do Gama

![Status do Projeto](https://img.shields.io/badge/status-Finalizado-green)

<div align="center" alt="imagem do readme">
    <img src="https://github.com/user-attachments/assets/1ab76b87-75c4-4fd2-8f5f-a38c6e3191fe" width="750px" height="300">
</div>

Este sistema foi desenvolvido para a **Administração Regional do Gama** (Distrito Federal) com o intuito de modernizar e centralizar o registro de atendimentos presenciais feitos à população local. A ferramenta permite um acompanhamento mais preciso das demandas da comunidade, facilitando a gestão pública e a transparência.

## 🚀 Funcionalidades Principais

- **Registro de Atendimento:** Cadastro detalhado de cidadãos e suas demandas específicas.
- **Painel Administrativo:** Interface intuitiva para servidores gerenciarem os registros.
- **Organização por Data:** Filtros e histórico para acompanhamento de fluxos.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework Web:** Django
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript

## 📂 Estrutura do Projeto

- `core/`: Contém a lógica de negócio, modelos de banco de dados e as views do sistema.
- `config/`: Configurações principais do Django (`settings.py`, `urls.py`).

## ⚙️ Como Executar o Projeto

### Pré-requisitos
- Python 3.8.6+ instalado
- Pip (gerenciador de pacotes)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/RR2M4A/Sistema-Administracao.git
   cd Sistema-Administracao

2.  Ative um ambiente virtual, e faça o download das dependências:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. Realize as migrações do banco de dados:
    ```bash
    python3 manage.py migrate
    ```
4. Crie um usuário admin:
    ```bash
    python3 manage.py createsuperuser
    ```
5. Inicie o servidor:
    ```bash
    python manage.py run server
    ```