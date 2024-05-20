import json
from json import JSONDecodeError
from typing import Tuple

from symplexmethod.input.abstract_input import AbstractInput


class JSONInput(AbstractInput):

    def __init__(self):
        super().__init__()
        while True:
            try:
                file_name = input("Введите название файла ")
                with open(file_name, "r", encoding="UTF-8") as inp_file:
                    self.data = json.load(inp_file)
                    break
            except FileNotFoundError:
                print("Файл с таким именем не найден!")
            except JSONDecodeError:
                self.data = {}
                return

    def read(self) -> Tuple[list[int], list[list[int]], list[int]]:
        return self.data["c"], self.data["a"], self.data["b"]

    def validate(self):
        if not [el in self.data.keys() for el in "abc"]:
            return False
        c, a, b = self.read()
        if len(set(map(len, a))) != 1 or len(c) != len(a[0]):
            return False
        if len(b) != len(a):
            return False
        return True
