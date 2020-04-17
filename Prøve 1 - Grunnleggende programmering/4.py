# Plancks konstant, Bohrs konstant og lysets hastighet
h = 6.63E-34
B = 2.18E-18
c = 3.0E8


def bølgeLengde(n, m):
    """Returnerer bølgelengde i nm gitt deeksitasjon fra to skall (int)"""
    
    return round((c / ((B /  h) * ((1 / m ** 2) * (1 / n ** 2))))/1.0E-9, 2)

# Tar skall fra og til som input, konverterer de til int, og funksjonen med de.
print(f"Bølgelengde: {bølgeLengde(int(input('Fra: ')), int(input('Til: ')))}nm")

# Eksempel
# print(f"{bølgeLengde(5, 2)}nm")
