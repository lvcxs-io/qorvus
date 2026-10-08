from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = (
        UniqueConstraint("id", "empresa_id", name="uq_usuario_id_empresa"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cargo = Column(Enum("ADMINISTRADOR", "FUNCIONARIO", name="cargo_enum"), nullable=False)
    data_admissao = Column(Date, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False, index=True)
    email = Column(String(70), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(Enum("ADMINISTRADOR", "FUNCIONARIO", name="perfil_enum"), nullable=False)
    status_ativo = Column(Boolean, default=True, nullable=False)

    empresa = relationship("Empresa", back_populates="usuarios")
    movimentacoes = relationship(
        "Movimentacao", back_populates="usuario", foreign_keys="Movimentacao.usuario_id"
    )
