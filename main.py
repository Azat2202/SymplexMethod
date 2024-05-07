from fractions import Fraction

from SymplexSolver import SymplexSolver


c = [0, 1, -3, 0, 2, 0]
a = [
    [1, 3, -1, 0, 2, 0],
    [0, -2, 4, 1, 0, 0],
    [0, -4, 3, 0, 8, 1]
]
b = [7, 12, 10]


def main():
    a_fr = [[Fraction(numerator=el) for el in arr] for arr in a]
    b_fr = [Fraction(numerator=el) for el in b]
    c_fr = [Fraction(numerator=el) for el in c]

    solver = SymplexSolver(a_fr, b_fr, c_fr)
    solver.solve()


if __name__ == '__main__':
    main()
