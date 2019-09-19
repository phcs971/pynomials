
def poliAdd(poli1, poli2):
    if poli1.var == poli2.var:
        result = poli(poli1.var, poli1.name + ' + ' + poli2.name)
        exponents1 = poli1.getExponents()
        for exp in exponents1:
            result.add((poli1.poli[exp], exp))
        exponents2 = poli2.getExponents()
        for exp in exponents2:
            result.add((poli2.poli[exp], exp))
        return result
    else:
        print("Can't sum different variabel polynomials")
        
def poliSub(poli1, poli2):
    if poli1.var == poli2.var:
        result = poli(poli1.var, poli1.name + ' - ' + poli2.name)
        exponents1 = poli1.getExponents()
        for exp in exponents1:
            result.add((poli1.poli[exp], exp))
        exponents2 = poli2.getExponents()
        for exp in exponents2:
            result.add((-poli2.poli[exp], exp))
        return result
    else:
        print("Can't subtract different variabel polynomials")

def poliMult(poli1, poli2):
    if poli1.var == poli2.var:
        result = poli(poli1.var, poli1.name + ' * ' + poli2.name)
        exponents1 = poli1.getExponents()
        exponents2 = poli2.getExponents()
        for exp1 in exponents1:
            for exp2 in exponents2: 
                result.add((poli1.poli[exp1]*poli2.poli[exp2], exp1+exp2))
        return result
    else:
        print("Can't multiply different variabel polynomials")

def poliDiv(poli1, poli2):
    if poli1.var == poli2.var:
        result = poli(poli1.var, poli1.name + ' / ' + poli2.name)
        exponents1 = poli1.getExponents()
        exponents2 = poli2.getExponents()
        maxExp1 = max(exponents1)
        maxExp2 = max(exponents2)
        p1 = poli1
        p2 = poli2
        while maxExp1 >= maxExp2:
            coef = p1.poli[maxExp1]/p2.poli[maxExp2]
            exp = maxExp1-maxExp2
            p0 = poli(poli1.var, 'p0')
            p0.add((coef, exp))
            result.add((coef, exp))
            p0 = poliMult(p2, p0)
            p1 = poliSub(p1, p0)
            exponents1 = p1.getExponents()
            maxExp1 = max(exponents1)
        remainder = p1
        remainder.name = 'Remainder(' + poli1.name + ' / ' + poli2.name + ')'
        remainder.clean()
        return result, remainder
    else:
        print("Can't divide different variabel polynomials")

def BRDiv(Poli, a):
    exponents = Poli.getExponents()
    coefs = []
    result = poli(Poli.var, Poli.name + '/({}-('.format(Poli.var) + str(a) + '))')
    for exp in exponents:
        coefs.append(Poli.poli[exp])
    remainder = 0
    maxExp = max(exponents) - 1
    for i in coefs:
        remainder = remainder*a + i
        result.add((remainder, maxExp))
        maxExp -= 1
    return result, remainder

def intDivisors(x):
    divs = []
    maxdiv = int(x**0.5 + 1)
    for i in range(1, maxdiv):
        if x % i == 0:
            if i != x/i:
                divs.append(i)
                divs.append(x/i)
            else: 
                divs.append(x)
    return sorted(divs)

class poli:
    def __init__(self, var = 'x', name = 'y'):
        self.poli = {}
        self.var = var
        if self.var == 'c':
            self.c = 'const'
        else:
            self.c = 'c'
        self.name = name
        self.integreted = False

    def clean(self):
        exponents = sorted(self.poli.keys(), reverse=True)
        for exp in exponents:
            if self.poli[exp] == 0:
                del self.poli[exp]
        try:
            if self.poli[self.c] == self.c:
                del self.poli[self.c]
        except:
            pass
        if self.poli == {}:
            self.poli = {0: 0}
    
    def getExponents(self, reverse=True):
        try:
            if self.poli[self.c] == self.c:
                exponents = list(self.poli.keys())
                exponents.remove(self.c)
                exponents = sorted(exponents, reverse=reverse)
        except:
            exponents = sorted(self.poli.keys(), reverse=reverse)
        return exponents

    def add(self, *args):
        for i in args:
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
            if exponent in self.poli.keys():
                self.poli[exponent] += float(coeficient)
            else:
                self.poli[exponent] = float(coeficient)
        self.clean()

    def of(self, x):
        self.clean()
        result = 0
        exponents = self.getExponents()
        for exp in exponents:
            val = self.poli[exp]*x**exp
            result += val
        return result

    def intRoots(self):
        try:
            possibleDivs = intDivisors(self.poli[0])
        except:
            possibleDivs = [0]
        roots = []
        poli = self
        while True:
            exponents = poli.getExponents()
            if len(exponents) == 0:
                break
            oldpoli = poli
            for i in possibleDivs:
                newpoli, rpos = BRDiv(poli, i)
                if rpos == 0:
                    roots.append(i)
                    poli = newpoli
                    continue
                newpoli, rneg = BRDiv(poli, -i)
                if rneg == 0:
                    roots.append(-i)
                    poli = newpoli
                    continue
            poli.show()
            if poli == oldpoli :
                break
        return roots

    def derive(self, name=''):
        if name == '':
            name = 'd'+self.name
        self.dpoli = poli(self.var, name)
        exponents = self.getExponents()
        for exp in exponents:
            try:
                self.dpoli.add((self.poli[exp]*exp, exp-1))
            except:
                pass
        self.dpoli.clean()
        return self.dpoli
    
    def integrate(self, name=''):
        if name == '':
            name = 's'+self.name
        self.spoli = poli(self.var, name)
        exponents = self.getExponents()
        for exp in exponents:
            self.spoli.add((self.poli[exp]/(exp+1), exp+1))
        self.spoli.clean()
        self.spoli.poli[self.c] = self.c
        return self.spoli

    def defIntegrate(self, start, end):
        integral = self.integrate()
        return integral.of(end) - integral.of(start)

    def show(self):
        writtenPoli = ''
        exponents = self.getExponents()
        for exp in exponents:
            try:
                coef = self.poli[exp]
                
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
                writtenPoli += writtenTerm
                if self.poli == {0: 0}:
                    writtenPoli = ' 0'
            except:
                pass
        try:
            if self.poli[self.c] == self.c:
                writtenPoli += ' + c'
        except:
            pass
        print(self.name + ' =' + writtenPoli)
