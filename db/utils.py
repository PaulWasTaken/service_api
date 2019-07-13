import logging

from fcntl import flock, LOCK_EX, LOCK_UN

logger = logging.getLogger(__name__)


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
        if exc_type:
            logger.error("Error occurred while holding lock.", exc_info=True)
            logger.error("Info from __exit__: %s %s", exc_type, exc_val)
        return True
