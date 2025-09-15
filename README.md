# 💧 Water Tracker - Um Projeto Full Stack Educacional

![Badge Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Badge Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Badge JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Badge HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Badge CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Este projeto é um aplicativo de rastreamento de consumo de água (Water Tracker) desenvolvido com o principal objetivo de aprendizado. A jornada de criação desta aplicação serviu como um estudo prático sobre o desenvolvimento de uma aplicação Full Stack, desde a concepção da interface do usuário (Frontend) até a lógica do servidor, banco de dados e autenticação (Backend).

## ✨ Features

* **Autenticação de Usuários:** Sistema completo de registro e login com senhas criptografadas.
* **Autenticação via Token JWT:** A comunicação entre frontend e backend é protegida usando JSON Web Tokens.
* **Rastreamento de Consumo:** Interface interativa com um anel de progresso para acompanhar o consumo diário de água.
* **Metas Personalizadas:** O usuário pode definir e alterar sua meta diária de consumo.
* **Sistema de Streak:** O aplicativo rastreia a sequência de dias em que o usuário atinge sua meta, incentivando a consistência.
* **Página de Estatísticas:** Uma visão geral do progresso do usuário, incluindo o total de água consumida e a média diária.
* **Interface Responsiva:** Design limpo e moderno que se adapta a diferentes tamanhos de tela.

## 🛠️ Tecnologias Utilizadas

#### **Backend**
* **Python:** Linguagem principal para a lógica do servidor.
* **Flask:** Micro-framework web para a criação da API.
* **Flask-SQLAlchemy:** ORM para interação com o banco de dados.
* **Flask-Bcrypt:** Para a criptografia segura de senhas.
* **Flask-Cors:** Para gerenciar as permissões de acesso entre o frontend e o backend.
* **PyJWT:** Para a geração e validação de tokens de autenticação.
* **SQLite:** Banco de dados relacional simples, utilizado em um único arquivo.

#### **Frontend**
* **HTML5:** Estrutura das páginas.
* **CSS3:** Estilização, layout (Flexbox/Grid) e animações.
* **JavaScript (Vanilla):** Lógica do lado do cliente, manipulação do DOM e comunicação com a API (usando `fetch`).

## 📁 Estrutura do Projeto

O projeto é organizado em uma arquitetura desacoplada, com o frontend e o backend em pastas separadas para uma clara separação de responsabilidades.

water_tracker/
├── frontend/
│   ├── css/
│   ├── js/
│   └── (*.html)
└── backend/
|   ├── app.py
|   └── database.db
└── requirements.txt

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local.

#### **Pré-requisitos**
* [Python 3.x](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes do Python)
* Um editor de código como o [VS Code](https://code.visualstudio.com/) com a extensão **Live Server**.

#### **1. Clone o Repositório**
```bash
git clone [https://github.com/seu-usuario/water-tracker.git](https://github.com/AntonioSTO/water-tracker.git)
cd water-tracker
```

#### **2. Configuração do Backend**


```bash
# Navegue até a pasta do backend
cd backend

# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie o banco de dados
python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

#### **3. Executando a Aplicação**

Você precisará de dois terminais abertos.

    Terminal 1 (Backend):

        Certifique-se de estar na pasta backend com o ambiente virtual ativado.

        Inicie o servidor Flask: python app.py

    Terminal 2 (Frontend):

        Abra o projeto no VS Code.

        No painel de arquivos, navegue até frontend/, clique com o botão direito em login.html e selecione "Open with Live Server".

Seu navegador abrirá o aplicativo, pronto para uso!

🎯 Objetivo Educacional

Este projeto foi construído como um exercício prático para solidificar conhecimentos em:

    Criação de uma API RESTful com Flask.

    Modelagem e gerenciamento de um banco de dados com SQLAlchemy.

    Implementação de um sistema de autenticação seguro com senhas com hash e tokens JWT.

    Desenvolvimento de uma interface de usuário interativa com JavaScript puro (Vanilla JS).

    Comunicação assíncrona entre cliente e servidor usando a API Fetch.

    Organização de um projeto Full Stack em uma arquitetura desacoplada.

    Resolução de problemas comuns como CORS e gerenciamento de estado no lado do cliente.