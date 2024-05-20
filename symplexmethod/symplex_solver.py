from fractions import Fraction
from typing import List, Tuple

from symplexmethod.models.symplex_table import SymplexTable
from symplexmethod.vector_utilities import sum_vectors, mul_vector


class SymplexSolver:
    def __init__(self, a: List[List[Fraction]], b: List[Fraction], c: List[Fraction]):
        self.a = a
        self.b = b
        self.c = c
        self.n = len(a[0])
        self.bs: list[int] = []
        self.table = self.__create_start_symplex_table()

    def solve(self) -> None:
        self.print_p()
        self.bs = self.__find_start_basis()
        if len(self.bs) == 0:
            print("Базис не вырожден")
            self.table = self.solve_non_singular()
            self.bs = self.table.bs
            print("Новая таблица:")
        while True:
            print(self.table)
            i, new_bs = self.__get_to_remove_p()
            if i == -1:
                print("Задача решена")
                self.__print_answer()
                break
            print(f"Вектор P{i + 1} встает на место вектора P{self.bs[new_bs] + 1} в базисе")
            self.table = self.__create_new_table(i, new_bs)

    def solve_non_singular(self) -> SymplexTable:
        """Решение симплекс таблицы с не вырожденным базисом"""
        print("Будем искать минимум новой целевой функции w=" + "+".join(f"y{i}" for i in range(1, len(self.b) + 1)))
        bs = list(range(self.n, self.n + len(self.b)))
        w = [Fraction(0) for _ in range(self.n)] + [Fraction(1) for _ in range(len(self.b))]
        p = [
            line + [Fraction(1) if i == j else Fraction(0) for j in range(len(bs))]
            for i, line in enumerate(self.a)
        ]
        solver = SymplexSolver(
            a=p,
            b=self.b,
            c=w
        )
        solver.solve()
        new_p = [
            line[:self.n]
            for line in solver.table.p
        ]
        return SymplexTable(
            bs=solver.table.bs,
            c=self.c,
            p0=solver.table.p0,
            p=new_p
        )

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

    def __get_to_remove_p(self) -> Tuple[int, int]:
        p = -1
        for i, el in enumerate(self.table.solve()[1:]):
            if el > 0:
                p = i
        if p == -1:
            return -1, -1
        p_data = self.table.get_p(p)
        theta_min = Fraction(10000)
        theta_i = -1
        for i, el in enumerate(p_data):
            if el <= 0:
                continue
            new_theta = self.table.p0[i] / el
            if new_theta < theta_min:
                theta_min = new_theta
                theta_i = i
        assert theta_i != -1
        return p, theta_i

    def __create_new_table(self, p_i: int, bs_i: int) -> SymplexTable:
        new_bs = [el if i != bs_i else p_i for i, el in enumerate(self.table.bs)]
        div_value = self.table.p[bs_i][p_i]
        # -1 + 4 * x = 0
        # x = -el / div_value
        coefficients = [
            -el / div_value if i != bs_i else (1 - div_value) / div_value
            for i, el in enumerate(self.table.get_p(p_i))
        ]
        new_p = [
            sum_vectors(line, mul_vector(self.table.p[bs_i], coefficients[i]))
            for i, line in enumerate(self.table.p)
        ]
        new_p0 = [
            el + self.table.p0[bs_i] * coefficients[i]
            for i, el in enumerate(self.table.p0)
        ]
        return SymplexTable(bs=new_bs, c=self.c, p0=new_p0, p=new_p)

    def __print_answer(self) -> None:
        p0, *_ = self.table.solve()
        print(f"Z_min = {p0}")
        for i, bs in enumerate(self.table.bs):
            print(f"X{bs + 1} = {self.table.p0[i]}")
