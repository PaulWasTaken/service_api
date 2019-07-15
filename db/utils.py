from fcntl import flock, LOCK_EX, LOCK_UN

from core.log import get_logger

logger = get_logger('db_utils')


class MyFlock:
    def __init__(self):
        self._file_name = '/var/lock/sqlite_write.lock'

    def __enter__(self):
        self._fd = open(self._file_name, 'w')
        flock(self._fd, LOCK_EX)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        flock(self._fd, LOCK_UN)
        self._fd.close()
