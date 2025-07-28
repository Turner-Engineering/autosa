import logging
from logging.handlers import RotatingFileHandler

from utils.settings import get_log_path

SIZE = 1024 * 1024 * 2  # 2 Megabytes


# create logger
formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


debug_handler = RotatingFileHandler(get_log_path("debug"), maxBytes=SIZE, backupCount=5)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

info_handler = RotatingFileHandler(get_log_path("info"), maxBytes=SIZE, backupCount=5)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.INFO)

autosa_logger = logging.getLogger("Autosa")
autosa_logger.addHandler(debug_handler)
autosa_logger.addHandler(info_handler)
autosa_logger.addHandler(terminal_handler)
autosa_logger.setLevel(logging.DEBUG)
