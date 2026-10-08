from sqlalchemy import Boolean, Column, ForeignKey, ForeignKeyConstraint, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Item(Base):
    __tablename__ = "item"
    __table_args__ = (
        UniqueConstraint("id", "empresa_id", name="uq_item_id_empresa"),
        ForeignKeyConstraint(
            ["categoria_id", "empresa_id"],
            ["categoria.id", "categoria.empresa_id"],
            name="fk_item_categoria_empresa",
        ),
        ForeignKeyConstraint(
            ["marca_id", "empresa_id"],
            ["marca.id", "marca.empresa_id"],
            name="fk_item_marca_empresa",
        ),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)
    categoria_id = Column(Integer, nullable=False)
    marca_id = Column(Integer, nullable=True)
    preco_venda = Column(Numeric(10, 2), nullable=False)
    preco_custo = Column(Numeric(10, 2), nullable=False)
    limite_minimo = Column(Integer, default=0, nullable=False)
    status_removido = Column(Boolean, default=False, nullable=False)
    descricao = Column(String(255), nullable=True)
    imagem_item = Column(String(255), nullable=True)

    empresa = relationship("Empresa", back_populates="itens")
    categoria = relationship("Categoria", back_populates="itens", foreign_keys=[categoria_id])
    marca = relationship("Marca", back_populates="itens", foreign_keys=[marca_id])
    movimentacoes = relationship(
        "Movimentacao", back_populates="item", foreign_keys="Movimentacao.item_id"
    )
