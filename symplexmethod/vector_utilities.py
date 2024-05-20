from fractions import Fraction
from typing import Union


def sum_vectors(a: list, b: list) -> list:
    return [a[i] + b[i] for i in range(len(a))]


def mul_vectors(a: list, b: list) -> list:
    return [a[i] * b[i] for i in range(len(a))]


def mul_vector(a: list, b: Union[int, Fraction]):
    return [el * b for el in a]
