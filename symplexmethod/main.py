import sys
from fractions import Fraction

from symplexmethod.input.json_input import JSONInput
from symplexmethod.symplex_solver import SymplexSolver


def main():
    input_ = JSONInput()
    if not input_.validate():
        print("Файл не валиден!")
        sys.exit(1)
    c, a, b = input_.read()
    a_fr = [[Fraction(numerator=el) for el in arr] for arr in a]
    b_fr = [Fraction(numerator=el) for el in b]
    c_fr = [Fraction(numerator=el) for el in c]

    solver = SymplexSolver(a_fr, b_fr, c_fr)
    solver.solve()


if __name__ == "__main__":
    main()
