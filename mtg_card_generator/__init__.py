import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

REPOSITORY_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
