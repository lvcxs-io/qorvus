from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Movimentacao(Base):
    __tablename__ = "movimentacao"
    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_mov_quantidade"),
        ForeignKeyConstraint(
            ["item_id", "empresa_id"],
            ["item.id", "item.empresa_id"],
            name="fk_mov_item_empresa",
        ),
        ForeignKeyConstraint(
            ["usuario_id", "empresa_id"],
            ["usuario.id", "usuario.empresa_id"],
            name="fk_mov_usuario_empresa",
        ),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False, index=True)
    item_id = Column(Integer, nullable=False)
    usuario_id = Column(Integer, nullable=False)
    tipo = Column(Enum("ENTRADA", "SAIDA", name="tipo_mov_enum"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_hora = Column(TIMESTAMP, default=datetime.now, nullable=False)

    empresa = relationship("Empresa", back_populates="movimentacoes")
    item = relationship("Item", back_populates="movimentacoes", foreign_keys=[item_id])
    usuario = relationship("Usuario", back_populates="movimentacoes", foreign_keys=[usuario_id])
