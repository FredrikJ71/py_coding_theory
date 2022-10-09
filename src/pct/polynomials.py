"""Some python function for working with polynomials with coefficients in F_p.
In the function it is assumed that the polynomials is represented as a list
with d+1 elements, were d is the degree. Example: poly = [1, 2, 3] is the
polynomial p(x) = 1 + 2x + 3x^2."""


def next_poly(poly, p):
    """return the next polynomial in lexicographic order."""
    # take care of the case for length 0
    if len(poly) == 0:
        return []

    # add 1 to degree with least degree
    new_poly = poly.copy()
    new_poly[0] += 1

    # if coefficient reached p, update next coefficient
    if new_poly[0] == p:
        new_poly = [0] + next_poly(new_poly[1:], p)
    return new_poly


def cyclic_shift(poly):
    """Return the shift of the polynomial poly cyclicaly one step.
    poly = c0 + c1x + c2x^2 + ... + cnx^n will be shifted into
    poly = cn + c0x + c1x^2 + ...+ c(n-1)x^n
    Mathematically this is equivalent to multiplication of x mod (x^n - 1)."""

    return (poly[-1:]+poly[0:-1]).copy()


def consta_cyclic_shift(poly, a, p):
    """Return the shift of the polynomial poly consta cyclicaly one step.
    poly = c0 + c1x + c2x^2 + ... + cnx^n will be shifted into
    poly = a*cn + c0x + c1x^2 + ...+ c(n-1)x^n, the multiplication
    a*cn is done modulus p
    Mathematically this is equivalent to multiplication of x mod (x^n - a)."""

    p2 = (poly[-1:]+poly[0:-1]).copy()
    p2[0] = (a*p2[0]) % p
    return p2


def degree(poly):
    """calculate the degree of the polynomial poly,
    return -1 if all coefficients zero"""
    for i, coeff in enumerate(reversed(poly)):
        # print(i, coeff)
        # if coeff is not zero we have found the degree
        if coeff != 0:
            return len(poly)-1-i
    return -1


def evaluate(poly, x):
    """calculate the value of poly(x)"""
    x_pow = 1
    val = 0
    for coeff in poly:
        val += coeff*x_pow
        x_pow *= x
    return val


if __name__ == '__main__':
    # test next_poly
    # start with 1 + 2x over F_3
    pol = [1, 2]
    print(pol)
    for int in range(10):
        pol = next_poly(pol, 3)
        print(pol)

    # test cyclic shift
    pol = [1, 2, 3, 4]
    print(pol)
    for i in range(10):
        pol = cyclic_shift(pol)
        print(pol)
    # test consta cyclic shift
    # testing consta cyclic shift
    print("consta_cyclic")
    pol = [1, 2, 3, 4]
    print(pol)
    for i in range(10):
        pol = consta_cyclic_shift(pol, 3, 5)
        print(pol)
    # test degree
    # 1 + 2x + x^2 degree = 2
    pol = [1, 2, 1, 0, 0]
    deg = degree(pol)
    print(deg)
    pol = [0, 0, 0]
    print(degree(pol))
    pol = [1, 0]
    print(degree(pol))
    print(evaluate(pol, 3))
    pol = [0, 0, 0]
    print(evaluate(pol, 3))
    pol = [1, 2, 1, 0, 0]
    print(evaluate(pol, 3))
