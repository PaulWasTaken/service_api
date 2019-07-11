from api import app
from db.models import set_up_db

set_up_db()
app.run(debug=True)
