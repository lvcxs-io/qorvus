# Qorvus

Sistema para cadastro e gestão de estoque, usuários, categorias, marcas e movimentações.

Frontend em Angular 22 com tema monocromático preto e branco. Backend em FastAPI com JWT Bearer e isolamento por empresa.

## O que está pronto até o momento:

- Tela de login + cadastro de empresa com administrador
- Dashboard com resumo, gráfico de movimentações, estoque baixo e recentes
- Menu lateral: Visão geral, Catálogo, Histórico, Relatórios, Funcionários
- API com autenticação, isolamento multiempresa e testes de isolamento

## Requisitos

- Python 3.11+ com venv
- MySQL 8 em execução
- Node.js 22.22.3+, 24.15+ ou 26+ com npm
- Git

## Como rodar

Execute a partir da raiz do projeto (`qorvus/`).

### 1. Backend — ambiente virtual e dependências

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 2. Backend — banco de dados

No MySQL Workbench ou cliente MySQL, execute nesta ordem, uma vez cada:

1. `migrations/V001__tabelas_base.sql` — cria o schema `qorvus` completo (agora com isolamento multiempresa).
2. `migrations/V002__seed_loja.sql` — cria a Bella Vitta com catálogo e movimentações de demonstração.

> Rode os scripts com o cliente em UTF-8 para preservar acentos. Se aplicar via console com encoding errado, nomes como "Máscara" e "Reparação" podem sair com mojibake.

### 3. Backend — variáveis de ambiente

Crie `.env` na raiz do projeto, ao lado de `requirements.txt`:

```env
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost:3306/qorvus
JWT_SECRET_KEY=CHAVE_ALEATORIA_COM_PELO_MENOS_32_CARACTERES
```

- Troque `USUARIO` e `SENHA` pelos do seu MySQL.
- Codifique caracteres especiais da senha para URL (ex: `@` vira `%40`).
- Gere uma chave JWT aleatória e privada com 32+ caracteres.
- Nunca commite o `.env`; ele já está no `.gitignore`.

### 4. Backend — iniciar a API

```powershell
uvicorn --app-dir backend app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 5. Frontend — instalar e rodar

Em outro terminal:

```powershell
cd frontend
npm install
npm start
```

- App: http://localhost:4200
- A API base está fixa em `http://127.0.0.1:8000` em `frontend/src/app/core/api.ts`.
- Recuperação de senha ainda não existe.

## Primeiro acesso

Os usuários do seed têm hash fictício e não fazem login. Crie uma conta real:

1. Abra http://localhost:4200
2. Clique em "Criar uma conta"
3. Preencha empresa, CNPJ com 14 dígitos, responsável, CPF com 11 dígitos, e-mail, telefone e senha com 8+ caracteres
4. Você cai direto no dashboard da sua empresa

Para testar com os dados da Bella Vitta, crie um usuário administrador vinculado à empresa 1 ou cadastre movimentações pela API para popular o gráfico dos últimos 7 dias.

## Testes e build

Backend, a partir de `backend/`:

```powershell
python -m unittest discover -s tests -v
```

Frontend, a partir de `frontend/`:

```powershell
npm run build
```

## Estrutura

```text
qorvus/
|-- backend/
|   `-- app/
|       |-- core/       # Configuração, banco, autenticação e dependências
|       |-- models/     # Entidades SQLAlchemy, uma por arquivo
|       `-- modules/    # Rotas, schemas e casos de uso organizados por domínio
|-- frontend/           # Aplicação Angular
|-- migrations/         # V001 schema + V002 seed Bella Vitta
|-- requirements.txt
`-- .env                # Configuração local, não versionada
```

## Isolamento multiempresa

A empresa vem do usuário autenticado, nunca do frontend. Categorias, marcas, itens e movimentações são filtrados pela empresa da sessão, com chaves compostas no banco reforçando o isolamento.

Principais endpoints:

- `POST /auth/register` — cria empresa e administrador na mesma transação
- `POST /auth/login` — login por e-mail e senha
- `GET /auth/me` — identidade autenticada
- `GET /empresas/minha` — empresa da sessão
- `GET /dashboard/resumo` — métricas e série dos últimos 7 dias
- `/categorias`, `/marcas`, `/itens`, `/movimentacoes` — restritos à empresa
- `/usuarios` — gerenciamento pelo administrador

## Problemas comuns

- API não sobe sem `.env`: confira `DATABASE_URL` e `JWT_SECRET_KEY` com 32+ caracteres.
- `Access denied` no MySQL: usuário, senha ou charset da URL errados.
- Frontend mostra "Não foi possível conectar à API": confirme a API em http://127.0.0.1:8000.
- Build Angular falha: rode `npm install` de novo e confira a versão do Node.
- Dashboard vazio: o gráfico só mostra os últimos 7 dias; crie movimentações recentes.
