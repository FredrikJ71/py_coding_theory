"""Some python function for working with polynomials with coefficients in F_p.
In the function it is assumed that the polynomials is represented as a list with d+1 
elements, were d is the degree. Example: poly = [1, 2, 3] is the polynomial
p(x) = 1 + 2x + 3x^2."""


def next_poly(poly, p):
    """return the next polynomial in lexicographic order."""
    # take care of the case for length 0
    if len(poly) == 0:
        return []
    
    # add 1 to degree with least degree
    new_poly = poly.copy()
    new_poly[0] += 1

    #if coefficient reached p, update next coefficient
    if new_poly[0] == p:
        new_poly = [0] + next_poly(new_poly[1:], p)
    return new_poly

