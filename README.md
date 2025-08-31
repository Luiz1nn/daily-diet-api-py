
# Daily Diet API

API REST em **Flask** para gerenciamento de refeições diárias.  
Permite registrar, listar, visualizar e editar refeições, incluindo a indicação se cada refeição está ou não dentro da dieta.  
Os dados são persistidos em banco **MySQL**.

---

## 🚀 Funcionalidades

- Registro de refeição com:
  - Nome
  - Descrição
  - Data e hora
  - Indicador **“dentro da dieta”**
- Edição de refeição (todas as propriedades)
- Listagem de refeições do usuário autenticado
- Visualização de uma refeição específica
- Autenticação de usuário e controle de sessão
- Persistência em banco de dados MySQL

---

## 🛠️ Stack Tecnológica

- **Python 3.12**
- **Flask** (API)
- **Flask-Login** (autenticação e sessões)
- **Flask SQLAlchemy** + **PyMySQL** (ORM e driver MySQL)
- **Docker Compose** (banco MySQL)
- **bcrypt** (hash de senha)

---

## 📦 Requisitos

- Python 3.12.x
- virtualenv
- Docker e Docker Compose

---

## ⚙️ Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/Luiz1nn/daily-diet-api-py.git
cd daily-diet-api-py
```

### 2. Criar e ativar o ambiente virtual

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ Banco de Dados com Docker

O projeto inclui um `docker-compose.yml` para subir um MySQL local.

### 1. Subir o MySQL

```bash
docker compose up -d
```

### 2. Credenciais padrão (conforme docker-compose)

- Host: **127.0.0.1**
- Porta: **3306**
- Banco: **daily-diet-db**
- Usuário: **admin**
- Senha: **admin123**

> O volume foi configurado no compose para persistência local.  
> Ajuste conforme sua máquina, se necessário.

---

## 🔧 Configuração da Aplicação

A aplicação já está configurada para apontar para o MySQL local acima.  
Se você subir o banco via Docker com o compose deste projeto, não precisa alterar variáveis para desenvolvimento.

---

## 🛠️ Inicializar o Schema do Banco (uma vez)

Antes do primeiro uso, crie as tabelas no MySQL:

```bash
# Garante que o container do MySQL está em execução
docker compose ps
```

```bash
# Cria as tabelas via SQLAlchemy
python -c "from app import app, db; from flask import current_app; ctx=app.app_context(); ctx.push(); db.create_all(); print('Tabelas criadas com sucesso'); ctx.pop()"
```

---

## ▶️ Iniciar a API

Com o ambiente virtual ativo e o banco rodando, execute:

```bash
python app.py
```

A API subirá em modo debug (desenvolvimento).  
Por padrão: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔗 Endpoints Principais

### Autenticação

- `POST /user` — cria usuário  
  **Body JSON:** `{ "username": "...", "password": "..." }`

- `POST /login` — autentica usuário  
  **Body JSON:** `{ "username": "...", "password": "..." }`

- `GET /logout` — encerra a sessão (requer login)

---

### Refeições (requer login)

- `POST /meal` — cria refeição  
  **Body JSON:** `{ "name": "...", "description": "...", "is_on_diet": true|false }`

- `GET /meal` — lista refeições do usuário autenticado

- `GET /meal/{id}` — obtém uma refeição específica

- `PUT /meal/{id}` — atualiza refeição  
  **Body JSON:** `{ "name": "...", "description": "...", "is_on_diet": true|false }`

> Todas as refeições são sempre associadas ao usuário autenticado.  
> A atualização de refeição verifica a propriedade da refeição.

---