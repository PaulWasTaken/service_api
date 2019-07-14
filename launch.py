from api import app
from threading import Timer

from db.models import set_up_db
from db.queries import flush_hold


class RepeatableTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function()


if __name__ == '__main__':
    RepeatableTimer(600, flush_hold).start()

    set_up_db()
    app.run(host='0.0.0.0', port=80, debug=True)
