from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_empresa = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="empresa")
    categorias = relationship("Categoria", back_populates="empresa")
    marcas = relationship("Marca", back_populates="empresa")
    itens = relationship("Item", back_populates="empresa", foreign_keys="Item.empresa_id")
    movimentacoes = relationship(
        "Movimentacao", back_populates="empresa", foreign_keys="Movimentacao.empresa_id"
    )
