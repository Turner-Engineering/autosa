import logging
from utils.settings import get_log_path

# create logger
formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

debug_handler = logging.FileHandler(get_log_path("debug"))
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

info_handler = logging.FileHandler(get_log_path("info"))
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

autosa_logger = logging.getLogger("Autosa")
autosa_logger.addHandler(debug_handler)
autosa_logger.addHandler(info_handler)
autosa_logger.setLevel(logging.DEBUG)
