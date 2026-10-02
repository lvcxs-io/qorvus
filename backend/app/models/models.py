from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, TIMESTAMP, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

# =========================================================================================
# 1. TABELA DE EMPRESAS
# =========================================================================================
class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_empresa = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)

    # Relacionamentos
    usuarios = relationship("Usuario", back_populates="empresa")


# =========================================================================================
# 2. TABELA DE CATEGORIAS
# =========================================================================================
class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)
    status_ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    itens = relationship("Item", back_populates="categoria")


# =========================================================================================
# 3. TABELA DE MARCAS
# =========================================================================================
class Marca(Base):
    __tablename__ = "marca"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)
    status_ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    itens = relationship("Item", back_populates="marca")


# =========================================================================================
# 4. TABELA DE USUÁRIOS
# =========================================================================================
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cargo = Column(Enum('ADMINISTRADOR', 'FUNCIONARIO', name='cargo_enum'), nullable=False)
    data_admissao = Column(Date, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=True)
    email = Column(String(70), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(Enum('ADMINISTRADOR', 'FUNCIONARIO', name='perfil_enum'), nullable=False)
    status_ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    empresa = relationship("Empresa", back_populates="usuarios")
    movimentacoes = relationship("Movimentacao", back_populates="usuario")


# =========================================================================================
# 5. TABELA DE ITENS (PRODUTOS)
# =========================================================================================
class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marca.id"), nullable=True)
    preco_venda = Column(Numeric(10, 2), nullable=False)
    preco_custo = Column(Numeric(10, 2), nullable=False)
    limite_minimo = Column(Integer, default=0, nullable=False)
    status_removido = Column(Boolean, default=False, nullable=False) # Soft Delete
    descricao = Column(String(255), nullable=True)
    imagem_item = Column(String(255), nullable=True)

    # Relacionamentos
    categoria = relationship("Categoria", back_populates="itens")
    marca = relationship("Marca", back_populates="itens")
    movimentacoes = relationship("Movimentacao", back_populates="item")


# =========================================================================================
# 6. TABELA DE MOVIMENTAÇÕES (ENTRADAS E SAÍDAS)
# =========================================================================================
class Movimentacao(Base):
    __tablename__ = "movimentacao"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    tipo = Column(Enum('ENTRADA', 'SAIDA', name='tipo_mov_enum'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_hora = Column(TIMESTAMP, default=datetime, nullable=False)

    # Regra de validação para garantir quantidade positiva na base
    __table_args__ = (
        CheckConstraint('quantidade > 0', name='ck_mov_quantidade'),
    )

    # Relacionamentos
    item = relationship("Item", back_populates="movimentacoes")
    usuario = relationship("Usuario", back_populates="movimentacoes")


# -----------------------------------------------------------------------------------------
# RESUMO PARA ENTENDERMOS:
# -----------------------------------------------------------------------------------------
# - CADA CLASSE REPRESENTA A TABELA NO NOSSO BANCO SQL 
# - COM OS TIPOS DE DADOS (BOOL, INT, PK, FK) MAPEADOS TAMBÉM
# - A PARTIR DAQUI CONSEGUIMOS QUE O PYTHON SE COMUNIQUE COM SQL E FAÇA AS CONSULTAS REFERENCIDAS