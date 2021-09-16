from num_theory import * 
import math
from sympy import pi, E, N

"""
this is a python file for unit testing of the python file 'num_theory.py'
"""

"""
Testing 'expand() function'
"""
def test_expand_1():
    assert expand(digits = 20, mathex = "pi", multiplier = 1) == "3.1415926535897932385"

def test_expand_2():
    assert expand(digits = 12, mathex = "pi", multiplier = 17) == "53.4070751110"
    
def test_expand_3():
    assert expand(digits = 25, mathex = "e", multiplier = 1) == "2.718281828459045235360287"

    
    
"""
Testing 'is_prime() function'
"""

def test_is_prime_1():
    assert is_prime(user_num = 1) == False
    
def test_is_prime_2():
    assert is_prime(user_num = -7) == False
    
def test_is_prime_3():
    assert is_prime(user_num = 2.4) == False

def test_is_prime_4():
    assert is_prime(user_num = 4) == False

def test_is_prime_5():
    assert is_prime(user_num = 97) == True

    
"""
Testing 'sliding() function'
"""

def test_sliding_1():
    assert sliding(my_string = '200.89420', window = 2) == [89, 94, 42, 20]
    
def test_sliding_2():
    assert sliding(my_string = '69.0131094', window = 3) == [131, 310, 109]

    
"""
Testing 'digit_prime() function'
"""
def test_digit_prime_1():
    assert digit_prime(pdigits = 120, pmathex = "e", pmultiplier = 1, pwindow=10) == 7427466391
    
