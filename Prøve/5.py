from pylab import *

k = 0.1
N = 100000
tidslengde = 60
dt = 60 / (N - 1)
sluttemperatur = 21

y0 = 75

t = zeros(N)
tder = zeros(N - 1)
tid = zeros(N)

t[0] = y0

for i in range(N - 1):
    tder[i] = -k * (t[i] - sluttemperatur)
    t[i + 1] = t[i] + tder[i] * dt
    tid[i + 1] = tid[i] + dt
grid()
xlabel("Tid (min)")
ylabel("Temperatur (C)")
plot(tid, t, "g", tid[:-1], tder, "r")
legend(["Temperatur", "Temperaturendring"])
show()