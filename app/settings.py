from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

SERVER_URL = config("DATA_CONNECTER_SERVER_URL", default="http://localhost:9022")
