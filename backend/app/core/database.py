from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings  # Import relativo (.config) para encontrar o arquivo na mesma pasta

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
# -----------------------------------------------------------------------------------------
# RESUMO PRA ENTENDERMOS:
# -----------------------------------------------------------------------------------------
# ESSE ARQUIVO FAZ A LIGAÇÃO ENTRE A NOSSA API (FASTAPI) COM O NOSSO BANCO DE DADOS (MYSQL)
# COM O SQLALCHEMY "TRADUZIMOS" O CÓDIGO EM PYTHON PARA O SQL (ORM)
# DEPOIS:
# 1 - O 'engine' faz a comunicação direto com o MySQL usando a URL de configuração -> "mysql+pymysql://root:@Lucao2000@localhost:3306/qorvus"
# 2 - O 'SessionLocal' cria a sessão temporária para fazermos inserções, leituras e updates no CRUD.
# 3 - A 'Base' serve de molde para criarmos as nossas classes/tabelas na (models.py).
# 4 - O 'get_db()' garante que a conexão abre quando um cliente faz um pedido e fecha logo a seguir para poupar recursos.