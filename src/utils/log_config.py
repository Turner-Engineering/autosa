import logging
from utils.settings import get_log_path

# create logger
autosa_logger = logging.getLogger("Autosa")

# set up log format
logging.basicConfig(
    level=logging.INFO,
    # handlers=[logging.FileHandler(get_log_path()), logging.StreamHandler()],
    handlers=[logging.FileHandler(get_log_path())],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S%z",
)
