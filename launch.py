from api import app
from threading import Timer

from db.models import set_up_db
from db.queries import flush_hold


class RepeatableTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function()


RepeatableTimer(2.0, flush_hold).start()


set_up_db()
app.run(debug=True)
