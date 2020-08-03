import logging.config

from .parser.parser import Parser
from .translator import Translator
from .refiner import refine

logging.config.fileConfig("logging.conf")
