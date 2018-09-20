# Fibonacci numbers module
"""Two Fibonacci routines: fib prints a series, fib2 returns a series"""

__version__ = "$Id: fibo.py,v 1.2 2012/12/21 17:44:32 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/math/fibo.py,v $


def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while b < n:
        print(b, end=" ")
        a, b = b, a+b


def fib2(n): # return Fibonacci series up to n
    """Return a Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result


if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
