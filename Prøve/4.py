from pylab import *

def NH3(T):
    return 0.00868 * T ** 2 - 1.66 * T + 87.4

def NaCl(T):
    return 0.000295 * T ** 2 + 0.00554 * T + 35.7
    
def likevekt(T):
    return NH3(T) - NaCl(T)

def halver(f,a=10, b=90, tol=1E-8):
    m = (a + b) / 2
    while abs(f(m)) > tol:
        if f(a) * f(m) < 0:
            b = m
        elif f(b) * f(m) < 0:
            a = m
        m = (a + b) / 2
    return m

print(f'Løsningene er like ved {halver(likevekt)} grader C')

x = linspace(0, 90, 1000)
y1 = NH3(x)
y2 = NaCl(x)
y = likevekt(x)
grid()
xlabel("Temperatur (C)")
ylabel("Konsentrasjon (mg/L)")
plot(x, y1, x, y2, x, y)
legend(["NH3", "NaCl", "Forskjell"])
show()
