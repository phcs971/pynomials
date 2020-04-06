import math

e = math.e
pi = math.pi


class Expression:
    def __init__(self, l, r, parent=0, layer=0):
        # l = Const(l) if isinstance(l, (int, float)) else l
        # r = Const(r) if isinstance(r, (int, float)) else r
        self.l = l
        self.r = r
        self.layer = layer
        self.parent = parent

    def __str__(self):
        return ''

    def __add__(self, b):
        self.parent = Add.priority
        if not (isinstance(b, (int, float))):
            b.parent = Add.priority
        return Add(self, b, layer=self.layer + 1)

    def __sub__(self, b):
        self.parent = Sub.priority
        if not (isinstance(b, (int, float))):
            b.parent = Sub.priority
        return Sub(self, b, layer=self.layer + 1)

    def __mul__(self, b):
        self.parent = Mult.priority
        if not (isinstance(b, (int, float))):
            b.parent = Mult.priority
        else:
            return Mult(b, self, layer=self.layer + 1)
        return Mult(self, b, layer=self.layer + 1)

    def __truediv__(self, b):
        self.parent = Div.priority
        if not (isinstance(b, (int, float))):
            b.parent = Div.priority
        elif (b == 0):
            raise ZeroDivisionError
        return Div(self, b, layer=self.layer + 1)

    def __pow__(self, b):
        self.parent = Pow.priority
        if not (isinstance(b, (int, float))):
            b.parent = Pow.priority
        return Pow(self, b, layer=self.layer + 1)

    def __radd__(self, b):
        self.parent = Add.priority
        return Add(self, b, layer=self.layer + 1)

    def __rsub__(self, b):
        self.parent = Sub.priority
        return Sub(b, self, layer=self.layer + 1)

    def __rmul__(self, b):
        self.parent = Mult.priority
        return Mult(b, self, layer=self.layer + 1)

    def __rtruediv__(self, b):
        self.parent = Div.priority
        return Div(b, self, layer=self.layer + 1)

    def __rpow__(self, b):
        self.parent = Pow.priority
        return Pow(b, self, layer=self.layer + 1)

    def __contains__(self, var):
        return self.dependsOn(var)

    def value(self, **env):
        pass

    def differenciate(self, variable, n=1):
        result = self
        for _ in range(n):
            result = 0 if isinstance(result, (int, float)
                                     ) else result.differenciate(variable, 1)
        return result

    def dependsOn(self, variable):
        lDepend = not isinstance(
            self.l, (int, float)) and self.l.dependsOn(variable)
        rDepend = not isinstance(
            self.r, (int, float)) and self.r.dependsOn(variable)
        return lDepend or rDepend

    priority = 0


class Const (Expression):
    def __init__(self, c, layer=0):
        self.c = c
        self.layer = layer

    def __str__(self):
        return str(self.c)

    def value(self, **env):
        return self.c

    def differenciate(self, variable, n=1):
        return 0

    def dependsOn(self, variable):
        return False


class Var (Expression):
    def __init__(self, name, layer=0):
        self.name = name
        self.layer = layer

    def __str__(self):
        return self.name

    def value(self, **env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            if isinstance(variable, str) and variable == self.name:
                return 1
            elif isinstance(variable, Var) and variable.name == self.name:
                return 1
            return 0
        else:
            return 0

    def dependsOn(self, variable):
        if isinstance(variable, str):
            return variable == self.name
        elif isinstance(variable, Var):
            return variable.name == self.name

class Add (Expression):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' and r == '0':
            return '0'
        elif l == '0':
            return r
        elif r == '0':
            return l

        if (self.priority < self.parent):
            return f'({l} + {r})'
        else:
            return f'{l} + {r}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l + r

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            l = 0 if isinstance(self.l, (int, float)
                                ) else self.l.differenciate(variable)
            r = 0 if isinstance(self.r, (int, float)
                                ) else self.r.differenciate(variable)
            return l + r
        else:
            return super().differenciate(variable, n=n)

    priority=1


class Sub (Expression):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' and r == '0':
            return '0'
        elif l == '0':
            return '-' + r
        elif r == '0':
            return l

        if(self.priority < self.parent):
            return f'({l} - {r})'
        else:
            return f'{l} - {r}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l - r

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            l = 0 if isinstance(self.l, (int, float)
                                ) else self.l.differenciate(variable)
            r = 0 if isinstance(self.r, (int, float)
                                ) else self.r.differenciate(variable)
            return l - r
        else:
            return super().differenciate(variable, n=n)

    priority=1


class Mult (Expression):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if l == '0' or r == '0':
            return '0'
        elif l == '1':
            return r
        elif r == '1':
            return l
        elif l == '-1':
            return f'-{r}'
        elif r == '-1':
            return f'-{l}'

        if (self.priority < self.parent):
            return f'({l} * {r})'
        else:
            return f'{l} * {r}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l * r

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.l
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            v = self.r
            dv = 0 if isinstance(v, (int, float)
                                 ) else v.differenciate(variable)
            return du*v + u*dv
        else:
            return super().differenciate(variable, n=n)

    priority=2


class Div (Expression):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            raise ZeroDivisionError
        elif l == '0':
            return '0'
        elif r == '1':
            return l

        if (self.priority < self.parent):
            return f'({l} / {r})'
        else:
            return f'{l} / {r}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l / r

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.l
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            v = self.r
            dv = 0 if isinstance(v, (int, float)
                                 ) else v.differenciate(variable)
            return (du*v - dv*u) / v**2
        else:
            return super().differenciate(variable, n=n)

    priority=2


class Pow (Expression):
    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            return '1'
        elif l == '0':
            return '0'
        elif r == '1':
            return l

        if (self.priority < self.parent):
            return f'({l} ** {r})'
        else:
            return f'{l} ** {r}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return l ** r

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.l
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            v = self.r
            dv = 0 if isinstance(v, (int, float)
                                 ) else v.differenciate(variable)
            return (v)*du*u**(v-1) + dv*Ln(u)*u**v
        else:
            return super().differenciate(variable, n=n)

    priority=3


class Root (Pow):
    def __init__(self, base, x, layer=0):
        super().__init__(x, 1/base, layer=layer)


class SquareRoot(Root):
    def __init__(self, x, layer=0):
        super().__init__(2, x, layer=layer)


class CubicRoot(Root):
    def __init__(self, x, layer=0):
        super().__init__(3, x, layer=layer)


class Log (Expression):
    def __init__(self, base, x, layer=0):
        super().__init__(x, base, layer=layer)

    def __str__(self):
        l = str(self.l)
        r = str(self.r)
        if r == '0':
            raise ValueError('math domain error')
        elif l == '1':
            return '0'
        elif r == l:
            return '1'

        if (self.priority < self.parent):
            return f'(log{str(self.r)} {str(self.l)})'
        else:
            return f'log{str(self.r)} {str(self.l)}'

    def value(self, **env):
        l = self.l if isinstance(self.l, (int, float)) else self.l.value(**env)
        r = self.r if isinstance(self.r, (int, float)) else self.r.value(**env)
        return math.log(l, r)

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.l
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            return (du/u) * Log(self.r, math.e)
        else:
            return super().differenciate(variable, n=n)

    priority=3


class Ln(Log):
    def __init__(self, x, layer=0):
        super().__init__(math.e, x, layer=layer)

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

    def differenciate(self, variable, n=1):
        u = self.l
        du = 0 if isinstance(u, (int, float)
                             ) else u.differenciate(variable)
        return (du/u)


class Trignometric(Expression):
    def __init__(self, x, parent=0, layer=0):
        super().__init__(x, 1, parent=parent, layer=layer)
        self.x = x
        self.parent = parent
        self.layer = layer


class Sin(Trignometric):
    def __str__(self):
        if isinstance(self.x, (int, float, Const)):
            val = self.value()
            return str(val)
        return f'sin({self.x})'

    def value(self, **env):
        x = self.x if isinstance(self.x, (int, float)) else self.x.value(**env)
        return math.sin(x)

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.x
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            return Cos(u, parent=self.parent, layer=self.layer)*du
        else:
            return super().differenciate(variable, n=n)

    def dependsOn(self, variable):
        return not isinstance(
            self.x, (int, float)) and self.x.dependsOn(variable)


class Cos(Trignometric):
    def __str__(self):
        if isinstance(self.x, (int, float, Const)):
            val = self.value()
            return str(val)
        return f'cos({self.x})'

    def value(self, **env):
        x = self.x if isinstance(self.x, (int, float)) else self.x.value(**env)
        return math.cos(x)

    def differenciate(self, variable, n=1):
        if not isinstance(n, int) and n < 0:
            raise ValueError('n must be a positive integer')
        if n == 0:
            return self
        elif n == 1:
            u = self.x
            du = 0 if isinstance(u, (int, float)
                                 ) else u.differenciate(variable)
            return (-1)*Sin(u, parent=self.parent, layer=self.layer)*du
        else:
            return super().differenciate(variable, n=n)

    def dependsOn(self, variable):
        return not isinstance(
            self.x, (int, float)) and self.x.dependsOn(variable)


class Tan(Trignometric):
    pass


class Sec(Trignometric):
    pass


class Cossec(Trignometric):
    pass


class Cotan(Trignometric):
    pass


