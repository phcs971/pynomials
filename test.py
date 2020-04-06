from expression import Var

x = Var('x')
y = Var('y')

f = x**2 + x*y + y**2 + 3*x - 3*y + 4

fx = f.differenciate(x)
fxx = f.differenciate(x,2)
fy = f.differenciate(y)
fyy = f.differenciate(y, 2)
fxy = fx.differenciate(y)
fyx = fy.differenciate(x)

h = fxx*fyy - fxy*fyx

print('fx =', fx)
print('fy =', fy)
print()
print('fxx =', fxx)
print('fxy =', fxy)
print('fyy =', fyy)
print('fyx =', fyx)
print()
print('h =', h)