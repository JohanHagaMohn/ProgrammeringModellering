# Importerer pylab
from pylab import *

# Konstanter
k = 0.1
N = 100000
tidslengde = 60
dt = 60 / (N - 1)
sluttemperatur = 21

# Startverdi(er)
y0 = 75

# Definerer arrayer
t = zeros(N)
tder = zeros(N - 1)
tid = zeros(N)

# Setter startverdi(er)
t[0] = y0

# Går igjennom løkka N antall ganger og legger in verdier ut ifra endringer
for i in range(N - 1):
    tder[i] = -k * (t[i] - sluttemperatur)
    t[i + 1] = t[i] + tder[i] * dt
    tid[i + 1] = tid[i] + dt

# Plotter (enda mer snacks)
grid()
xlabel("Tid (min)")
ylabel("Temperatur (C)")
# Bemerk at den deriverte er én mindre fordi den trenger to punkter for å finne endring. Derfor ekskluderer jeg siste tidsverdi
plot(tid, t, "g", tid[:-1], tder, "r")
legend(["Temperatur", "Temperaturendring"])
axhline(y=sluttemperatur, color="blue")
axhline(y=0, color="black")
axvline(x=0, color="black")
show()