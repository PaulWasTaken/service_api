from config import PROJECT_ROOT
from logging import DEBUG

LOGS_PATH = PROJECT_ROOT.join('global_logs.log').ensure().strpath
LOG_LEVEL = DEBUG
