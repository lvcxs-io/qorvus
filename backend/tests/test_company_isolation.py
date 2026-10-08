import os
import unittest
from datetime import date

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = (
    "test-only-jwt-secret-key-with-more-than-thirty-two-characters"
)

from fastapi import HTTPException
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import verify_password
from app.models import Categoria, Empresa, Item, Movimentacao, Usuario
from app.modules.auth.schemas import AuthResponse, CompanyOwnerRegistration, LoginRequest
from app.modules.auth.service import AuthService
from app.modules.inventory.schemas import DashboardSummaryResponse
from app.modules.inventory.schemas import MovementCreate
from app.modules.inventory.service import InventoryService


class CompanyIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:")

        @event.listens_for(self.engine, "connect")
        def enable_foreign_keys(connection, _record) -> None:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.db = self.session_factory()
        self.company_a, self.admin_a, self.item_a = self._create_company(
            "Loja A", "11111111111111", "admin-a@example.com", "11111111111"
        )
        self.company_b, self.admin_b, self.item_b = self._create_company(
            "Loja B", "22222222222222", "admin-b@example.com", "22222222222"
        )

    def tearDown(self) -> None:
        self.db.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_companies_can_create_categories_with_the_same_name(self) -> None:
        category_a = Categoria(
            empresa_id=self.company_a.id,
            nome="Acessórios",
            status_ativo=True,
        )
        category_b = Categoria(
            empresa_id=self.company_b.id,
            nome="Acessórios",
            status_ativo=True,
        )
        self.db.add_all([category_a, category_b])
        self.db.commit()
        self.assertNotEqual(category_a.id, category_b.id)

    def test_company_cannot_read_another_company_product(self) -> None:
        service = InventoryService(self.db, self.admin_a)
        with self.assertRaises(HTTPException) as error:
            service.get_item(self.item_b.id)
        self.assertEqual(error.exception.status_code, 404)

    def test_company_cannot_use_another_company_category(self) -> None:
        foreign_category = Categoria(
            empresa_id=self.company_b.id,
            nome="Categoria privada",
            status_ativo=True,
        )
        self.db.add(foreign_category)
        self.db.commit()

        service = InventoryService(self.db, self.admin_a)
        with self.assertRaises(HTTPException) as error:
            service.create_item(
                self._item_payload(categoria_id=foreign_category.id)
            )
        self.assertEqual(error.exception.status_code, 404)

    def test_database_rejects_cross_company_product_category(self) -> None:
        foreign_category = Categoria(
            empresa_id=self.company_b.id,
            nome="Categoria do banco",
            status_ativo=True,
        )
        self.db.add(foreign_category)
        self.db.flush()
        invalid_item = Item(
            empresa_id=self.company_a.id,
            nome="Produto inconsistente",
            quantidade=0,
            categoria_id=foreign_category.id,
            marca_id=None,
            preco_venda=10,
            preco_custo=5,
            limite_minimo=2,
            status_removido=False,
        )
        self.db.add(invalid_item)
        with self.assertRaises(IntegrityError):
            self.db.commit()
        self.db.rollback()

    def test_database_rejects_movement_by_another_company_user(self) -> None:
        movement = Movimentacao(
            empresa_id=self.company_a.id,
            item_id=self.item_a.id,
            usuario_id=self.admin_b.id,
            tipo="ENTRADA",
            quantidade=1,
        )
        self.db.add(movement)
        with self.assertRaises(IntegrityError):
            self.db.commit()
        self.db.rollback()

    def test_company_cannot_move_another_company_product(self) -> None:
        service = InventoryService(self.db, self.admin_a)
        with self.assertRaises(HTTPException) as error:
            service.create_movement(
                MovementCreate(
                    item_id=self.item_b.id,
                    tipo="ENTRADA",
                    quantidade=5,
                )
            )
        self.assertEqual(error.exception.status_code, 404)
        self.assertEqual(self.db.get(Item, self.item_b.id).quantidade, 8)

    def test_dashboard_summary_only_contains_authenticated_company_data(self) -> None:
        InventoryService(self.db, self.admin_a).create_movement(
            MovementCreate(
                item_id=self.item_a.id,
                tipo="ENTRADA",
                quantidade=4,
            )
        )

        summary_a = DashboardSummaryResponse.model_validate(
            InventoryService(self.db, self.admin_a).dashboard_summary()
        )
        summary_b = DashboardSummaryResponse.model_validate(
            InventoryService(self.db, self.admin_b).dashboard_summary()
        )

        self.assertEqual(summary_a.total_produtos, 1)
        self.assertEqual(summary_a.entradas_7_dias, 4)
        self.assertEqual(summary_a.movimentacoes_recentes[0].produto, self.item_a.nome)
        self.assertEqual(summary_b.entradas_7_dias, 0)
        self.assertEqual(summary_b.movimentacoes_recentes, [])

    def test_owner_registration_and_login_store_only_password_hash(self) -> None:
        registration = CompanyOwnerRegistration(
            nome_empresa="Empresa Nova",
            cnpj="33333333333333",
            nome_completo="Nova Responsável",
            cpf="33333333333",
            email="NOVA@EXAMPLE.COM",
            telefone="11999990000",
            senha="Senha-segura-2026",
        )
        auth_service = AuthService(self.db)
        session = auth_service.register_company_owner(registration)
        public_session = AuthResponse.model_validate(session).model_dump()
        user = (
            self.db.query(Usuario)
            .filter(Usuario.email == "nova@example.com")
            .one()
        )

        self.assertEqual(user.empresa.nome_empresa, "Empresa Nova")
        self.assertNotEqual(user.senha_hash, registration.senha)
        self.assertTrue(verify_password(registration.senha, user.senha_hash))
        self.assertFalse(verify_password("qualquer senha", "$2b$10HASH_FICTICIO"))
        self.assertEqual(session["user"].id, user.id)
        self.assertNotIn("senha_hash", public_session["user"])

        logged_in = auth_service.login(
            LoginRequest(email="nova@example.com", senha=registration.senha)
        )
        self.assertEqual(logged_in["user"].id, user.id)
        self.assertTrue(logged_in["access_token"])

    def test_login_rejects_invalid_password(self) -> None:
        with self.assertRaises(HTTPException) as error:
            AuthService(self.db).login(
                LoginRequest(email="admin-a@example.com", senha="senha-errada")
            )
        self.assertEqual(error.exception.status_code, 401)

    def test_duplicate_registration_rolls_back_company_creation(self) -> None:
        registration = CompanyOwnerRegistration(
            nome_empresa="Empresa Duplicada",
            cnpj="44444444444444",
            nome_completo="Responsável",
            cpf="44444444444",
            email="admin-a@example.com",
            telefone="11999990000",
            senha="Senha-segura-2026",
        )
        with self.assertRaises(HTTPException) as error:
            AuthService(self.db).register_company_owner(registration)

        self.assertEqual(error.exception.status_code, 409)
        self.assertIsNone(
            self.db.query(Empresa)
            .filter(Empresa.cnpj == registration.cnpj)
            .first()
        )

    def _create_company(
        self,
        company_name: str,
        cnpj: str,
        email: str,
        cpf: str,
    ) -> tuple[Empresa, Usuario, Item]:
        company = Empresa(nome_empresa=company_name, cnpj=cnpj)
        self.db.add(company)
        self.db.flush()
        user = Usuario(
            nome_completo=f"Admin {company_name}",
            cpf=cpf,
            cargo="ADMINISTRADOR",
            data_admissao=date.today(),
            empresa_id=company.id,
            email=email,
            telefone="11999990000",
            senha_hash="unused-test-hash",
            perfil="ADMINISTRADOR",
            status_ativo=True,
        )
        category = Categoria(
            empresa_id=company.id,
            nome="Categoria",
            status_ativo=True,
        )
        self.db.add_all([user, category])
        self.db.flush()
        item = Item(
            empresa_id=company.id,
            nome=f"Produto {company_name}",
            quantidade=8,
            categoria_id=category.id,
            marca_id=None,
            preco_venda=10,
            preco_custo=5,
            limite_minimo=2,
            status_removido=False,
        )
        self.db.add(item)
        self.db.commit()
        return company, user, item

    @staticmethod
    def _item_payload(categoria_id: int) -> object:
        from app.schemas.schemas import ItemCreate

        return ItemCreate(
            nome="Produto inválido",
            quantidade=0,
            categoria_id=categoria_id,
            marca_id=None,
            preco_venda=10,
            preco_custo=5,
            limite_minimo=2,
        )


if __name__ == "__main__":
    unittest.main()
