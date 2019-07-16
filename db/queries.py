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


def verification_wrapper(func=None, check_if_closed=True):
    def _wrapper(query_func):
        @wraps(query_func)
        def wrapper(uuid, *args, **kwargs):
            where = UserInfo.uuid_hash == hash(uuid)
            with db.engine.begin() as conn:
                if not conn.execute(sa.select([1], where)).scalar():
                    raise UUIDNotFoundException('User with `%s` UUID was not found.' % uuid)
                if check_if_closed:
                    if not conn.execute(sa.select([1], sa.and_(where, UserInfo.status.is_(True)))).scalar():
                        raise ClosedBankAccountExeption('Bank account is closed for `%s` UUID.' % uuid)
            return query_func(uuid, *args, **kwargs)
        return wrapper
    if func is not None:
        return _wrapper(func)
    return _wrapper


@verification_wrapper
def add_sum(uuid: str, value: float):
    with MyFlock(), db.engine.begin() as conn:
        where = UserInfo.uuid_hash == hash(uuid)
        current_sum = conn.execute(sa.select([UserInfo.balance], where)).scalar()
        conn.execute(sa.update(UserInfo, where).values(balance=current_sum + value))


@verification_wrapper(check_if_closed=False)
def get_status(uuid: str):
    with db.engine.begin() as conn:
        where = UserInfo.uuid == uuid
        return conn.execute(sa.select([UserInfo.balance, UserInfo.status], where)).fetchone()


@verification_wrapper
def subtract_sum(uuid: str, value: float):
    with MyFlock(), db.engine.begin() as conn:
        where = UserInfo.uuid_hash == hash(uuid)
        current_sum, hold = conn.execute(sa.select([UserInfo.balance, UserInfo.hold], where)).fetchone()
        if current_sum - hold - value < 0:
            raise NotEnoughMoney('User with UUID `%s` does not have enough money for operation to be performed.' % uuid)
        conn.execute(sa.update(UserInfo, where).values(hold=UserInfo.hold + value))


def flush_hold():
    with MyFlock(), db.engine.begin() as conn:
        conn.execute(sa.update(UserInfo).values(balance=UserInfo.balance - UserInfo.hold, hold=0))
