import os

TESTING = True
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'this is debug'

if 'SNITCH_DB_URI' not in os.environ:
    from snitch.config.postgres_config import config as postgres
    os.environ['SNITCH_DB_URI'] = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(**postgres)

SQLALCHEMY_DATABASE_URI = os.environ['SNITCH_DB_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False


ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TREE = os.path.join(ROOT_PATH, "snark", "tree.bin")
TREE_INDEX = os.path.join(ROOT_PATH, "snark", "tree_index.bin")
VERIFICATION_KEY = os.path.join(ROOT_PATH, "snark", "vk.key")
PROVING_KEY = os.path.join(ROOT_PATH, "snark", "pk.key")

UPLOAD_FOLDER = os.path.join(ROOT_PATH, "uploads")
DEFAULT_IMAGE_NAME = "default.png"
DEFAULT_IMAGE = os.path.join(UPLOAD_FOLDER, DEFAULT_IMAGE_NAME)
