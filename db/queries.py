import sqlalchemy as sa

from functools import wraps

from db.models import db, UserInfo
from db.utils import MyFlock


class UUIDNotFoundException(Exception):
    pass


class ClosedBankAccountExeption(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


def verification_wrapper(query_func):
    @wraps(query_func)
    def wrapper(uuid, *args, **kwargs):
        where = UserInfo.uuid == uuid
        with db.engine.begin() as conn:
            if not conn.execute(sa.select([1], where)).scalar():
                raise UUIDNotFoundException('User with `%s` UUID was not found.' % uuid)
            if not conn.execute(sa.select([1], sa.and_(where, UserInfo.status.is_(True)))).scalar():
                raise ClosedBankAccountExeption('Bank account is closed for `%s` UUID.' % uuid)
        return query_func(uuid, *args, **kwargs)
    return wrapper


@verification_wrapper
def add_sum(uuid: str, value: float):
    with MyFlock(), db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        current_sum = conn.execute(sa.select([UserInfo.balance], where)).scalar()
        conn.execute(sa.update(UserInfo, where).values(balance=current_sum + value))


def get_status(uuid: str):
    with db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        return conn.execute(sa.select([UserInfo.balance, UserInfo.status], where)).fetchone()


@verification_wrapper
def subtract_sum(uuid: str, value: float):
    with MyFlock(), db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        current_sum, hold = conn.execute(sa.select([UserInfo.balance, UserInfo.hold], where)).fetchone()
        if current_sum - hold - value < 0:
            raise NotEnoughMoney('User with UUID `%s` does not have enough money for operation to be performed.' % uuid)
        conn.execute(sa.update(UserInfo, where).values(balance=current_sum - hold - value))


def flush_hold():
    with MyFlock(), db.engine.begin() as conn:
        conn.execute(sa.update(UserInfo).values(balance=UserInfo.balance - UserInfo.hold, hold=0))
