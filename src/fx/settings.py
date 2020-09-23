import logging
import os

LOGGER = logging.getLogger('ForexTradingBot')
ROOT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}"

# Formatting
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S.%f'
