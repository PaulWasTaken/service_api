from threading import Timer

from api import app
from core.log import get_logger
from db.models import set_up_db
from db.queries import flush_hold


class RepeatableTimer(Timer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = get_logger('repeatable_timer')

    def run(self):
        while not self.finished.wait(self.interval):
            self.function()
            self._logger.debug('Hold was flushed.')


if __name__ == '__main__':
    RepeatableTimer(600, flush_hold).start()

    set_up_db()
    app.run(host='0.0.0.0', port=80)
