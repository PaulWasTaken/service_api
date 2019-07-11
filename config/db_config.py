from config import PROJECT_ROOT


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT.join('sqlite.db').ensure().strpath
