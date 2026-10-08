from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# =========================================================================================
# 1. SCHEMAS DE EMPRESA
# =========================================================================================
class EmpresaBase(BaseModel):
    nome_empresa: str = Field(..., max_length=150)
    cnpj: str = Field(..., max_length=18)

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================================================
# 2. SCHEMAS DE CATEGORIA
# =========================================================================================
class CategoriaBase(BaseModel):
    nome: str = Field(..., max_length=50)
    descricao: Optional[str] = Field(None, max_length=255)
    status_ativo: Optional[bool] = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = Field(None, max_length=255)
    status_ativo: Optional[bool] = None

class CategoriaResponse(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================================================
# 3. SCHEMAS DE MARCA
# =========================================================================================
class MarcaBase(BaseModel):
    nome: str = Field(..., max_length=50)
    descricao: Optional[str] = Field(None, max_length=255)
    status_ativo: Optional[bool] = True

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = Field(None, max_length=255)
    status_ativo: Optional[bool] = None

class MarcaResponse(MarcaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================================================
# 4. SCHEMAS DE UTILIZADOR (USUÁRIO)
# =========================================================================================
class UsuarioBase(BaseModel):
    nome_completo: str = Field(..., max_length=100)
    cpf: str = Field(..., max_length=14)
    cargo: str  # 'ADMINISTRADOR' ou 'FUNCIONARIO'
    data_admissao: date
    empresa_id: Optional[int] = None
    email: EmailStr
    telefone: str = Field(..., max_length=20)
    perfil: str # 'ADMINISTRADOR' ou 'FUNCIONARIO'
    status_ativo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8, max_length=128)

class UsuarioResponse(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
# Não herdamos de UsuarioBase para não se tornar obrigatório todos os campos
class UsuarioUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, max_length=14)
    cargo: Optional[str] = None  # 'ADMINISTRADOR' ou 'FUNCIONARIO'
    data_admissao: Optional[date] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    perfil: Optional[str] = None  # 'ADMINISTRADOR' ou 'FUNCIONARIO'
    status_ativo: Optional[bool] = None
    senha: Optional[str] = Field(None, min_length=8, max_length=128)


# =========================================================================================
# 5. SCHEMAS DE ITEM (PRODUTO)
# =========================================================================================
class ItemBase(BaseModel):
    nome: str = Field(..., max_length=100)
    quantidade: Optional[int] = Field(0, ge=0)
    categoria_id: int
    marca_id: Optional[int] = None
    preco_venda: float = Field(..., gt=0)
    preco_custo: float = Field(..., gt=0)
    limite_minimo: Optional[int] = Field(0, ge=0)
    descricao: Optional[str] = Field(None, max_length=255)
    imagem_item: Optional[str] = Field(None, max_length=255)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    quantidade: Optional[int] = Field(None, ge=0)
    categoria_id: Optional[int] = None
    marca_id: Optional[int] = None
    preco_venda: Optional[float] = Field(None, gt=0)
    preco_custo: Optional[float] = Field(None, gt=0)
    limite_minimo: Optional[int] = Field(None, ge=0)
    descricao: Optional[str] = Field(None, max_length=255)
    imagem_item: Optional[str] = Field(None, max_length=255)
    status_removido: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    status_removido: bool

    model_config = ConfigDict(from_attributes=True)


# =========================================================================================
# 6. SCHEMAS DE MOVIMENTAÇÃO DE ESTOQUE
# =========================================================================================
class MovimentacaoBase(BaseModel):
    item_id: int
    usuario_id: int
    tipo: str  # 'ENTRADA' ou 'SAIDA'
    quantidade: int = Field(..., gt=0)  # Garante que a quantidade é estritamente positiva

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(MovimentacaoBase):
    id: int
    data_hora: datetime

    model_config = ConfigDict(from_attributes=True)