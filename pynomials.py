import math


class Pynomial:
    def __init__(self, l, r):
        # l = Const(l) if isinstance(l, (int, float)) else l
        # r = Const(r) if isinstance(r, (int, float)) else r
        self.l = l
        self.r = r

    def __str__(self):
        return ''

    def __add__(self, b):
        return Add(self, b)

    def __sub__(self, b):
        return Sub(self, b)

    def __mul__(self, b):
        return Mult(self, b)

    def __truediv__(self, b):
        return Div(self, b)

    def __pow__(self, b):
        return Pow(self, b)

    def __radd__(self, b):
        return Add(b, self)

    def __rsub__(self, b):
        return Sub(b, self)

    def __rmul__(self, b):
        return Mult(b, self)

    def __rtruediv__(self, b):
        return Div(b, self)

    def __rpow__(self, b):
        return Pow(b, self)

    def value(self, **env):
        pass

    def differenciate(self, variable):
        pass

    def __integrate(self, variable):
        pass


class Const (Pynomial):
    def __init__(self, c):
        self.c = c

    def __str__(self):
        return str(self.c)

    def value(self, **env):
        return self.c

    def differenciate(self, variable):
        return 0

    def __integrate(self, variable):
        return self*Var(variable)



class Var (Pynomial):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def value(self, **env):
        if self.name in env.keys():
            return env[self.name]
        else:
            return 0

    def differenciate(self, variable):
        if variable == self.name:
            return 1
        return 0

    def __integrate(self, variable):
        if variable == self.name:
            return self**2/2
        return self*Var(variable)

class Add (Pynomial):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' and r == '0':
            return '0'
        elif l == '0':
            return r
        elif r == '0':
            return l
        return f'({l} + {r})'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l + r

    def differenciate(self, variable):
        l = 0 if isinstance(self.l, (int, float)
                            ) else self.l.differenciate(variable)
        r = 0 if isinstance(self.r, (int, float)
                            ) else self.r.differenciate(variable)
        return l + r


class Sub (Pynomial):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' and r == '0':
            return '0'
        elif l == '0':
            return '-' + r
        elif r == '0':
            return l
        return f'({l} - {r})'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l - r

    def differenciate(self, variable):
        l = 0 if isinstance(self.l, (int, float)
                            ) else self.l.differenciate(variable)
        r = 0 if isinstance(self.r, (int, float)
                            ) else self.r.differenciate(variable)
        return l-r


class Mult (Pynomial):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' or r == '0':
            return '0'
        elif l == '1':
            return r
        elif r == '1':
            return l
        return f'({l} * {r})'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l * r

    def differenciate(self, variable):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        v = self.r
        dv = 0 if isinstance(v, (int, float)
                             ) else v.differenciate(variable)
        return du*v + u*dv


class Div (Pynomial):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            raise ZeroDivisionError
        elif l == '0':
            return '0'
        elif r == '1':
            return l
        return f'({l} / {r})'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l / r

    def differenciate(self, variable):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        v = self.r
        dv = 0 if isinstance(v, (int, float)
                             ) else v.differenciate(variable)
        return (du*v - dv*u) / v**2


class Pow (Pynomial):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            return '1'
        elif l == '0':
            return '0'
        elif r == '1':
            return l
        return f'({l} ** {r})'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l ** r

    def differenciate(self, variable):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        v = self.r
        dv = 0 if isinstance(v, (int, float)
                             ) else v.differenciate(variable)
        return (v)*du*u**(v-1) + dv*Ln(u)*u**v


class Root (Pow):
    def __init__(self, base, x):
        super().__init__(x, 1/base)


class SquareRoot(Root):
    def __init__(self, x):
        super().__init__(2, x)


class CubicRoot(Root):
    def __init__(self, x):
        super().__init__(3, x)


class Log (Pynomial):
    def __init__(self, base, x):
        super().__init__(x, base)

    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            raise ValueError('math domain error')
        elif l == '1':
            return '0'
        elif r == l:
            return '1'
        return f'log{str(self.r)} {str(self.l)}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return math.log(l, r)

    def differenciate(self, variable):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        return (du/u) * Log(self.r, math.e)


class Ln(Log):
    def __init__(self, x):
        super().__init__(math.e, x)

    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '1':
            return '0'
        elif r == l:
            return '1'
        return f'ln {str(self.l)}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        return math.log(l)

    def differenciate(self, variable):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        return (du/u)
