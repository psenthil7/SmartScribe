import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = None):
    """Logger with file and console output"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(acstime)s - %(name)s - %(levelname)s - %(message)s'
    )

  