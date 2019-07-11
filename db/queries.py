from functools import wraps

import sqlalchemy as sa

from db.models import db, UserInfo
from db.utils import MyFlock


class UUIDNotExistException(Exception):
    pass


class ClosedBankAccountExeption(Exception):
    pass


def verification_wrapper(query_func):
    @wraps(query_func)
    def wrapper(uuid, *args, **kwargs):
        where = UserInfo.uuid == uuid
        with db.engine.begin() as conn:
            if not conn.execute(sa.select([1], where)).scalar():
                raise UUIDNotExistException('User with `%s` UUID was not found.' % uuid)
            if not conn.execute(sa.select([1], sa.and_(where, UserInfo.status.is_(True)))):
                raise ClosedBankAccountExeption('Bank account is closed for `%s` UUID.' % uuid)
        return query_func(uuid, *args, **kwargs)
    return wrapper


@verification_wrapper
def add_sum(uuid: str, value: float):
    with db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        current_sum = conn.execute(sa.select([UserInfo.balance], where)).scalar()
        new_sum = current_sum + value
        conn.execute(sa.update(UserInfo, where).values(balance=new_sum))


@verification_wrapper
def get_status(uuid: str):
    with db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        return conn.execute(sa.select([UserInfo.balance, UserInfo.status], where)).fetchall()[0]
