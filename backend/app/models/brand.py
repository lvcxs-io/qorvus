from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Marca(Base):
    __tablename__ = "marca"
    __table_args__ = (
        UniqueConstraint("empresa_id", "nome", name="uq_marca_empresa_nome"),
        UniqueConstraint("id", "empresa_id", name="uq_marca_id_empresa"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=True)
    status_ativo = Column(Boolean, default=True, nullable=False)

    empresa = relationship("Empresa", back_populates="marcas")
    itens = relationship("Item", back_populates="marca", foreign_keys="Item.marca_id")
