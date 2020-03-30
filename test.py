import pynomials as pn

x = pn.Var('x')
y = pn.Var('y')

f = x*y**3 + 3*x**2*y + pn.const_e**(x*y)

print(f)
print(f.value(x=1, y=1))

fx = f.differenciate('x')
print(fx)
print(fx.value(x=1, y=1))
