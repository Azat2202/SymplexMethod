from fractions import Fraction
from typing import List

from prettytable import PrettyTable


# def __repr__(self):
class SymplexSolver:
    def __init__(self, a: List[List[Fraction]], b: List[Fraction], c: List[Fraction]):
        self.a = a
        self.b = b
        self.c = c
        self.n = len(a[0])
        self.bs: list[int] = list()

    def solve(self) -> None:
        self.print_p()

    def print_p(self):
        for i in range(self.n):
            print(f"P{i} = ({', '.join(map(str, self.__get_p(i)))})")

    def __get_p(self, i: int) -> List[Fraction]:
        return [arr[i] for arr in self.a]

# @staticmethod
# def print_symplex_table(bs: list[int], c: list[int], a: list[list[int]], result: list[int]) -> str:
#     table = PrettyTable()
#     table.title = ["BS", "C"] + [f"P{i}" for i in range(len(a))]
#     return table.__repr__()
