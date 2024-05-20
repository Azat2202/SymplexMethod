from dataclasses import dataclass
from fractions import Fraction
from typing import List

from prettytable import PrettyTable

from symplexmethod.vector_utilities import mul_vectors


@dataclass
class SymplexTable:
    bs: list[int]
    c: list[Fraction]
    p0: list[Fraction]
    p: list[list[Fraction]]

    def solve(self) -> list[Fraction]:
        out: list[Fraction] = [sum(mul_vectors(self.p0, self.__get_basis()))]
        for i in range(len(self.p[0])):
            out.append(sum(mul_vectors(self.get_p(i), self.__get_basis())) - self.c[i])
        return out

    def get_p(self, i: int) -> List[Fraction]:
        return [arr[i] for arr in self.p]

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = ["i", "BS", "C"] + [
            f"P{i}" for i in range(len(self.p[0]) + 1)
        ]
        table.padding_width = 2
        for i, _ in enumerate(self.p0):
            table.add_row(
                [i, f"P{self.bs[i] + 1}", self.c[self.bs[i]], self.p0[i]] + self.p[i]
            )
        table.add_row(["", "", ""] + self.solve())
        return str(table)

    def __get_basis(self) -> list[Fraction]:
        return [self.c[b] for b in self.bs]
