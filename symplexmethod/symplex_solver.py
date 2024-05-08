from dataclasses import dataclass
from fractions import Fraction
from typing import List

from prettytable import PrettyTable


def mul_vectors(a: list, b: list):
    return [a[i] * b[i] for i in range(len(a))]


@dataclass
class SymplexTable:
    bs: list[int]
    c: list[Fraction]
    p0: list[Fraction]
    p: list[list[Fraction]]

    def solve(self) -> list[Fraction]:
        out: list[Fraction] = [sum(mul_vectors(self.p0, self.__get_basis()))]
        for i in range(len(self.p[0])):
            out.append(
                sum(mul_vectors(self.__get_p(i), self.__get_basis())) - self.c[i]
            )
        return out

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = ["i", "BS", "C"] + [
            f"P{i}" for i in range(len(self.p[0]) + 1)
        ]
        for i, _ in enumerate(self.p0):
            table.add_row(
                [i, f"P{self.bs[i]}", self.c[self.bs[i]], self.p0[i]] + self.p[i]
            )
        table.add_row(["", "", ""] + self.solve())
        return str(table)

    def __get_p(self, i: int) -> List[Fraction]:
        return [arr[i] for arr in self.p]

    def __get_basis(self) -> list[Fraction]:
        return [self.c[b] for b in self.bs]


class SymplexSolver:
    def __init__(self, a: List[List[Fraction]], b: List[Fraction], c: List[Fraction]):
        self.a = a
        self.b = b
        self.c = c
        self.n = len(a[0])
        self.bs: list[int] = []

    def solve(self) -> None:
        self.print_p()
        table = self.__create_start_symplex_table()
        print(table)

    def print_p(self):
        print(f"P{0} = ({', '.join(map(str, self.b))})")
        for i in range(self.n):
            print(f"P{i + 1} = ({', '.join(map(str, self.__get_p(i)))})")

    def __get_p(self, i: int) -> List[Fraction]:
        return [arr[i] for arr in self.a]

    def __create_start_symplex_table(self) -> SymplexTable:
        start_basis = self.__find_start_basis()
        table = SymplexTable(bs=start_basis, c=self.c, p0=self.b, p=self.a)
        return table

    def __find_start_basis(self) -> list[int]:
        out: list[int] = []
        for i in range(len(self.a)):
            basis = [Fraction(1) if i == j else Fraction(0) for j in range(len(self.a))]
            for j in range(self.n):
                if self.__get_p(j) == basis:
                    out.append(j)
                    break
            if len(out) != i + 1:
                return []
        return out
