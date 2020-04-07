from expression import Var, SquareRoot, Ln, pi

k = 8.99e9
e = 1.6e-19
E = 8.85e-12

q = Var('q')

z = Var('z')
R = Var('R')

d = Var('d')
L = Var('L')

sigma = Var('sigma')
lmbd = Var('lambda')


Vbarra = k*lmbd*Ln((L + SquareRoot(L**2 + d**2))/d)
Vbarra2 = k*q/L*Ln((L + SquareRoot(L**2 + d**2))/d)

Vanel = k*q/(SquareRoot(z**2+R**2))

Vdisco = sigma * (SquareRoot(z**2+R**2)-z) / (2*E)
Vdisco2 = q / (pi*R**2) * (SquareRoot(z**2+R**2)-z) / (2*E)


print(Vdisco2.value(
    q=5e-9,
    z=0.01,
    R=17.5e-3/2
)*(-e))