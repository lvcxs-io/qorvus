from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categoria"
    __table_args__ = (
        UniqueConstraint("empresa_id", "nome", name="uq_categoria_empresa_nome"),
        UniqueConstraint("id", "empresa_id", name="uq_categoria_id_empresa"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=True)
    status_ativo = Column(Boolean, default=True, nullable=False)

    empresa = relationship("Empresa", back_populates="categorias")
    itens = relationship("Item", back_populates="categoria", foreign_keys="Item.categoria_id")
