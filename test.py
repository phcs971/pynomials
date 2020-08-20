from expression import Var

x = Var('x')
y = Var('y')

f = x**2 + x*y + y**2 + 3*x - 3*y + 4

fx = f.diff(x)
fxx = f.diff(x,2)
fy = f.diff(y)
fyy = f.diff(y, 2)
fxy = fx.diff(y)
fyx = fy.diff(x)

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