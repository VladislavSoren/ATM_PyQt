from dataclasses import dataclass
from enum import Enum
from random import choice, randint

from config import BANKNOTE_TYPES, MAX_QUANTITY


@dataclass
class Cartridge:
    number: int
    banknote_type: int
    banknote_type_index: int
    quantity: int
    quantity_temp: int
    broken: bool


class CartridgeInfoGen:
    @staticmethod
    def gen_banknote_type_index():
        return randint(0, len(BANKNOTE_TYPES) - 1)

    @staticmethod
    def gen_quantity():
        return randint(0, MAX_QUANTITY)

    @staticmethod
    def gen_broken():
        return choice([True, False])


class Status(Enum):
    SUCCESS = 'SUCCESS'
    FAULT = 'FAULT'
