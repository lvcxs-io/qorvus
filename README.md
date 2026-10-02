# Qorvus SIS

API para gerenciamento de estoque, com cadastro de empresas, usuários, categorias, marcas e itens, além do controle de movimentações de entrada e saída.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- SQLAlchemy 2
- MySQL 8
- PyMySQL
- Pydantic 
- Passlib e bcrypt

## Requisitos

- Python instalado
- MySQL 8 em execução

## Rodando no Windows

Execute os comandos a partir da pasta raiz do projeto, onde estão `requirements.txt` e `migrations/`.

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, permita scripts apenas na sessão atual e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Preparar o banco de dados

Execute os scripts SQL no MySQL Workbench, nesta ordem:

1. `migrations/V001__tabelas_base.sql` cria o banco `qorvus` e suas tabelas.
2. `migrations/V002__seed_loja.sql` insere dados de exemplo e deve ser executado depois do V001.

O banco configurado no projeto deve ser MySQL 8.

### 4. Configurar a conexão

Crie um arquivo `.env` na raiz do projeto, no mesmo nível de `requirements.txt`, com a URL de conexão:

```env
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost:3306/qorvus
```

Substitua `USUARIO` e `SENHA` pelas credenciais do seu MySQL. Se a senha tiver caracteres especiais, codifique-os para URL. O arquivo `.env` é ignorado pelo Git..

### 5. Iniciar a API

uvicorn app.main:app --reload

Com o servidor iniciado, acesse:

- API: http://127.0.0.1:8000
- Documentação interativa (Swagger): http://127.0.0.1:8000/docs
- Documentação alternativa (ReDoc): http://127.0.0.1:8000/redoc

## Estrutura do projeto

```text
qorvus.sis/
|-- backend/
|   `-- app/
|       |-- core/       # Configuração, conexão com banco e paginação
|       |-- models/     # Modelos SQLAlchemy
|       |-- routers/    # Rotas da API
|       `-- schemas/    # Schemas Pydantic
|-- migrations/         # Criação do banco e dados de exemplo
|-- requirements.txt
`-- .env                # Configuração local, não versionada
```


## Rotas principais

Os endpoints estão agrupados por recurso e podem ser explorados em `/docs`:

- `/empresas`
- `/usuarios`
- `/categorias`
- `/marcas`
- `/itens`
- `/movimentacoes`

O endpoint raiz `/` retorna o status da API.
