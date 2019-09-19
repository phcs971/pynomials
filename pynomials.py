#from matplotlib.pyplot import figure, plot, show
#from numpy import arange

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
    
    def getExponents(self):
        try:
            if self.poli[self.c] == self.c:
                exponents = list(self.poli.keys())
                exponents.remove(self.c)
                exponents = sorted(exponents, reverse=True)
        except:
            exponents = sorted(self.poli.keys(), reverse=True)
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
        result = 0
        exponents = self.getExponents()
        for exp in exponents:
            val = self.poli[exp]*x**exp
            result += val
        return result

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

    def area(self, start, end):
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
            except:
                pass
        try:
            if self.poli[self.c] == self.c:
                writtenPoli += ' + c'
        except:
            pass
        print(self.name + ' =' + writtenPoli)

'''
    def markerPlot(self, figSize, start, end, increment, color='black', marker='o'):
        fig = figure(figsize=figSize)
        for x in arange(start, end, increment):
            y = self.of(x)
            plot(x, y, color=color, marker=marker)
        show()
'''
