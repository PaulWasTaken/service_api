import sqlalchemy as sa

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TypeDecorator
from uuid import UUID

from sqlalchemy.ext.hybrid import hybrid_property

from api import app


db = SQLAlchemy(app)


class UUIDv4(TypeDecorator):
    impl = sa.types.String(36)

    @property
    def python_type(self):
        return UUID

    def process_bind_param(self, value, dialect):
        if value is not None:
            UUID(value, version=4)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = UUID(value, version=4)

        return value


class UserInfo(db.Model):
    uuid = sa.Column(UUIDv4(), primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    balance = sa.Column(sa.Float(precision=2), nullable=False)
    hold = sa.Column(sa.Float(precision=2), nullable=False)
    status = sa.Column(sa.Boolean(), nullable=False)


def form_db_entry(uuid: str, name: str, balance: int, hold: int, status: bool):
    return {
        'uuid': uuid,
        'name': name,
        'balance': balance,
        'hold': hold,
        'status': status
    }


def set_up_db():
    db.drop_all()
    db.create_all()
    with db.engine.begin() as conn:
        conn.execute(sa.insert(
            UserInfo, [
                form_db_entry('26c940a1-7228-4ea2-a3bc-e6460b172040', 'Петров Иван Сергеевич', 1700, 300, True),
                form_db_entry('7badc8f8-65bc-449a-8cde-855234ac63e1', 'Kazitsky Jason', 200, 200, True),
                form_db_entry('5597cc3d-c948-48a0-b711-393edf20d9c0', 'Пархоменко Антон Александрович', 100, 300, True),
                form_db_entry('867f0924-a917-4711-939b-90b179a96392', 'Петечкин Петр Измаилович', 1000000, 1, False),
                ]
            )
        )
