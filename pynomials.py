from numpy import arange
from tqdm import tqdm
import inspect, types

def polyAdd(poly1, poly2):
    if poly1.var == poly2.var:
        result = poly(poly1.var, '[' + poly1.name + ' + ' + poly2.name + ']')
        exponents1 = poly1.getExponents()
        for exp in exponents1:
            result.add((poly1.poly[exp], exp))
        exponents2 = poly2.getExponents()
        for exp in exponents2:
            result.add((poly2.poly[exp], exp))
        return result
    else:
        print("Can't sum different variabel polynomials")
        
def polySub(poly1, poly2):
    if poly1.var == poly2.var:
        result = poly(poly1.var, '[' + poly1.name + ' - ' + poly2.name + ']')
        exponents1 = poly1.getExponents()
        for exp in exponents1:
            result.add((poly1.poly[exp], exp))
        exponents2 = poly2.getExponents()
        for exp in exponents2:
            result.add((-poly2.poly[exp], exp))
        return result
    else:
        print("Can't subtract different variabel polynomials")

def polyMult(poly1, poly2):
    if poly1.var == poly2.var:
        result = poly(poly1.var, '[' + poly1.name + ' * ' + poly2.name + ']')
        exponents1 = poly1.getExponents()
        exponents2 = poly2.getExponents()
        for exp1 in exponents1:
            for exp2 in exponents2: 
                result.add((poly1.poly[exp1]*poly2.poly[exp2], exp1+exp2))
        return result
    else:
        print("Can't multiply different variabel polynomials")

def polyDiv(poly1, poly2):
    if poly1.var == poly2.var:
        result = poly(poly1.var, '[' + poly1.name + ' / ' + poly2.name + ']')
        maxExp1 = poly1.degree()
        maxExp2 = poly2.degree()
        p1 = poly1
        p2 = poly2
        while maxExp1 >= maxExp2:
            coef = p1.poly[maxExp1]/p2.poly[maxExp2]
            exp = maxExp1-maxExp2
            p0 = poly(poly1.var, 'p0')
            p0.add((coef, exp))
            result.add((coef, exp))
            p0 = polyMult(p2, p0)
            p1 = polySub(p1, p0)
            maxExp1 = p1.degree()
        remainder = p1
        remainder.name = '[Remainder(' + poly1.name + ' / ' + poly2.name + ')]'
        remainder.clean()
        return result, remainder
    else:
        print("Can't divide different variabel polynomials")

def BRDiv(Poly, a):
    exponents = Poly.getExponents()
    coefs = []
    result = poly(Poly.var, Poly.name + '/({}-('.format(Poly.var) + str(a) + '))')
    for exp in exponents:
        coefs.append(Poly.poly[exp])
    remainder = 0
    maxExp = Poly.degree() - 1
    for i in coefs:
        remainder = remainder*a + i
        result.add((remainder, maxExp))
        maxExp -= 1
    return result, remainder

def intDivisors(x):
    divs = []
    maxdiv = int(abs(x)**0.5 + 1)
    for i in range(1, maxdiv):
        if x % i == 0:
            if i != x/i:
                divs.append(i)
                divs.append(x/i)
            else: 
                divs.append(x)
    return sorted(divs)

class poly:
    def __init__(self, var = 'x', name = 'y', *terms):
        '''
        var: poly variable
        name: poly name
        terms: either a function or a series of poly Terms (coeficient, exponent) (examples):
            def f(x):
                y = x**2 + 2*x + 1
                return y
            or
            def f(x):
                return x**2 + 2*x + 1

            or

            (1,2), (2,1), (1)
        
        '''
        self.poly = {}
        self.var = var
        if self.var == 'c':
            self.c = 'const'
        else:
            self.c = 'c'
        self.name = name
        
        for i in terms:
            if isinstance(i, tuple, list, int, float):
                self.add(i)
            #elif isinstance(i, types.FunctionType):
            #    self.addFuntion(i)

    def clean(self):
        exponents = sorted(self.poly.keys(), reverse=True)
        for exp in exponents:
            if self.poly[exp] == 0:
                del self.poly[exp]
        try:
            if self.poly[self.c] == self.c:
                del self.poly[self.c]
        except:
            pass
        if self.poly == {}:
            self.poly = {0: 0}
    
    def getExponents(self, reverse=True):
        try:
            if self.poly[self.c] == self.c:
                exponents = list(self.poly.keys())
                exponents.remove(self.c)
                exponents = sorted(exponents, reverse=reverse)
        except:
            exponents = sorted(self.poly.keys(), reverse=reverse)
        return exponents

    def degree(self):
        return max(self.getExponents())

    def add(self, *terms):
        for i in terms:
            try:
                i = float(i)
                coeficient = i
                exponent = 0
            except:
                if len(i) == 1:
                    coeficient = i[0]
                    exponent = 0
                elif len(i) == 2:
                    coeficient = i[0]
                    exponent = i[1]
            if exponent in self.poly.keys():
                self.poly[exponent] += float(coeficient)
            else:
                self.poly[exponent] = float(coeficient)
        self.clean()
        
    def of(self, x):
        self.clean()
        result = 0
        exponents = self.getExponents()
        for exp in exponents:
            val = self.poly[exp]*x**exp
            result += val
        return result

    def roots(self, tryInt=True):
        deg = self.degree()
        roots = []
        if deg == 1:
            a = self.poly[1]
            b = self.poly[0]
            roots.append(-b/a)

        elif deg == 2:
            a = self.poly[2]
            b = self.poly[1]
            c = self.poly[0]
            delta = b**2 -4*a*c
            if delta == 0:
                roots.append(-b/(2*a))
            else:
                roots.append((-b+delta**0.5)/(2*a))
                roots.append((-b-(delta**0.5))/(2*a))
        else:
            if tryInt == True:
                try:
                    intRoots, remainder = self.intRoots()
                    for i in intRoots:
                        roots.append(i)
                    newRoots = remainder.roots(tryInt=False)
                    for i in newRoots:
                        roots.append(i)
                except:
                    pass
            else:
                if len(roots) == 0:
                    return ["Couldn't find the roots of the poly"]
                else:
                    return ["Could only find these roots: ", roots]    
        return roots

    def intRoots(self):
        try:
            possibleDivs = intDivisors(self.poly[0])
        except:
            possibleDivs = [0]
        roots = []
        poly = self
        while True:
            exponents = poly.getExponents()
            if len(exponents) == 0:
                break
            oldpoly = poly
            for i in possibleDivs:
                newpoly, rpos = BRDiv(poly, i)
                if rpos == 0:
                    roots.append(i)
                    poly = newpoly
                    continue
                newpoly, rneg = BRDiv(poly, -i)
                if rneg == 0:
                    roots.append(-i)
                    poly = newpoly
                    continue
            if poly == oldpoly :
                break
        return roots, poly

    def extensiveRootSearch(self, start, end, increment=0.01):
        roots = []
        for i in tqdm(arange(start, end, increment)):
            if self.of(i) == 0:
                roots.append(i)
        return roots

    def derive(self, name=''):
        if name == '':
            name = 'd'+self.name
        self.dpoly = poly(self.var, name)
        exponents = self.getExponents()
        for exp in exponents:
            try:
                self.dpoly.add((self.poly[exp]*exp, exp-1))
            except:
                pass
        self.dpoly.clean()
        return self.dpoly
    
    def integrate(self, name=''):
        if name == '':
            name = 's'+self.name
        self.spoly = poly(self.var, name)
        exponents = self.getExponents()
        for exp in exponents:
            self.spoly.add((self.poly[exp]/(exp+1), exp+1))
        self.spoly.clean()
        self.spoly.poly[self.c] = self.c
        return self.spoly

    def defIntegrate(self, start, end):
        integral = self.integrate()
        return integral.of(end) - integral.of(start)

    def show(self):
        writtenPoly = ''
        exponents = self.getExponents()
        for exp in exponents:
            try:
                coef = self.poly[exp]
                
                if coef > 0:
                    signal = '+'
                elif coef < 0:
                    signal = '-'
                else:
                    signal = ''

                if abs(coef) == 1 and exp != 0:
                    writtenCoef = ''
                elif exp == 0:
                    writtenCoef = str(abs(coef))
                else:
                    writtenCoef = str(abs(coef)) + '*'

                if exp == 0:
                    writtenExp = ''
                elif exp == 1:
                    writtenExp = '{}'.format(self.var)
                else:
                    writtenExp = '{}^'.format(self.var) + str(exp)
                
                writtenTerm = ' ' + signal + ' ' + writtenCoef + writtenExp

                if coef == 0:
                    writtenTerm = ''
                writtenPoly += writtenTerm
                if self.poly == {0: 0}:
                    writtenPoly = ' 0'
            except:
                pass
        try:
            if self.poly[self.c] == self.c:
                writtenPoly += ' + c'
        except:
            pass
        print(self.name + ' =' + writtenPoly)
