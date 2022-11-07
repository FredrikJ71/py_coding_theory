"""A script that generates all generating polynomials for
m x m circulant matrices. The generation is over the field F_q"""
import math
import pct.polynomials as poly


def euler_phi(d):
    """Calculates Eulers phi (totient) function of d.
    The number of positive integers k smaller than d such 
    that gcd(k,d)==1. Note! This is a naive implementation based 
    on exhaustive search."""

    # return 0 if d <= 0
    if d <= 0:
        return 0        
    phi = 1
    for k in range(2,d):
        # check if gcd(k,d) == 1, then increase phi
        if math.gcd(k,d) == 1:
            phi += 1 
    return phi


def number_defining_pol(m,q):
    """Calculates the number of defining polynomials for mxm
    circulant matrices. The function is based on the formula in
    Quasi-cyclic codes over F_13 and enumeration of defining polynomials."""
    sum = 0
    # sum over all divisors of m
    for d in range(1,m+1):
        # if d not divisor test next d
        if m % d != 0:
            continue
        # calculate number of defining polynomials for d
        sum+= euler_phi(d) * (pow(q,m/d)-1) * math.gcd(d, q-1)
    return int(sum/((q-1)*m))


def mult_inverse(q):
    """generate a list of all multiplicative inverses a*a^-1 mod q""" 
    inverses = [-1, 1] # a = 0 no multiplicative inverse, a = 1 its own inverse
    for a in range(2,q):
        a_inv = 1
        while (a * a_inv) % q != 1:
            a_inv += 1
        inverses.append(a_inv)
    return inverses


def equivalent_monic(pol, q, inv_q):
    """Generate an equivalent monic polynomial to pol.
    assume pol is a_0 + a_1 x + a_2 x^2 + ... + a_dx^d.
    The equivalent polynomial is then 
    (a_0 * inv_ad) + (a_1 * inv_ad) x + (a_2 * inv_ad) x^2 + .. + x^d,
    where inv_ad is the multiplicative inverse of a_d mod q."""
    deg = poly.degree(pol)
    ad = pol[deg] # find the value of a_d
    inv_ad = inv_q[ad] # find the inverse using the inv_q
    temp = pol.copy()
    for pos in range(len(pol)):
        temp[pos] = (pol[pos] * inv_ad) % q
    return temp


def generate_polynomials(m,q):
    """generate all non-equivalent generating polynomials for 
    m x m circulant matrices over F_q"""
    nbr_polynomials = number_defining_pol(m,q) # number of polynomials to look for
    # create first polynomial p(x) = 1 + 0x + ... + 0x^(m-1)
    pol = [1]
    while len(pol) != m:
        pol.append(0)
    print(pol)
    polynomials = [pol] # the list of found polynomials
    print(polynomials)
    # need multiplicative inverses when determine equivalent polynomials
    inverses = mult_inverse(q)
    # iterate until we have found nbr_polynomials
    while len(polynomials) != nbr_polynomials:
        # generate next monic polynomial
        pol = poly.next_monic_poly(pol, q)
        print(pol)
        temp = pol.copy() # temp should later be shifted and we do not want to shift pol
        new_pol = True # keep track if pol is in list
        for i in range(m-1):
            # shift polynomial
            temp = poly.cyclic_shift(temp)
            print(temp)
            # check if monic equivalent polynomial is already in polynomials
            if equivalent_monic(temp, q, inverses) in polynomials:
                new_pol = False
        # if new polynomial add pol in list
        if new_pol:
            polynomials.append(pol.copy())
        print(polynomials)
    return polynomials    


if __name__ == '__main__':
    m = int(input("Size of the matrix (m): "))
    q = int(input("Prime field (q): "))
    print("Number of polynomials:", number_defining_pol(m,q))
    pols = generate_polynomials(m,q)
    print(pols)
    print(len(pols))
