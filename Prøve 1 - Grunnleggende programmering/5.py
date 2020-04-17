from pylab import *

# Bæreevnen, antall startbakterier og reproduksjonsraten
B = 2E9
N = 10000
k = 0.30

# Maks tid i minutter
maksTid = 60

# Tid i en liste
#x = [x for x in range(0, maksTid + 1)]

# Antall individer ved tid
#def individ(tid):
#    return N * (1 + k) ** tid
def individ(Nt):
    return Nt + k * Nt * (1 - Nt/B)

# Plotter utviklingen ut fra bæreevnen
#y = [individ(x) * k * individ(x) * (1 - individ(x) / B) for x in x]
x = [0]
y = [N]
for i in range(1, maksTid):
    x.append(i)
    y.append(individ(y[-1]))
    

# Konfigurerer grafen
grid()
title("Populasjonsvekst av e.coli")
xlabel("tid")
ylabel("populasjon")
axhline(y=0, color="black")
axvline(x=0, color="black")
plot(x,y)
show()

# Printer ut antall bakterier etter en time
print(f"\nEtter 1 time har vi {y[-1]} bakterier")

