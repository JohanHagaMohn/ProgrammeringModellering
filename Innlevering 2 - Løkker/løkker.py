

def oppgave1():

    """Oppgave 4.7"""

    print(f"\n{sum(3 / 3 ** x for x in range(int(input('Iterasjoner: '))))}\n")

    # Her tar jeg antall iterasjoner, gjør det om til et heltall, og printer ut summen av 3 / 3 ** x så mange ganger.


def oppgave2():

    """Oppgave 4.9"""

    from math import log10

    print(f"\n{round(log10(float(input('Slutt: ')) / float(input('Start: '))) / log10(1 + float(input('Rente: '))), 2)}"
          f" år\n")

    # Her tar jeg først og importerer log10.
    # Så bruker tar jeg log10 av kvotienten av sluttinvesteringensfloaten og startinvesteringsfloaten.
    # Dette deler jeg på rentefloaten + 1, og avrunder kvotienten med 2 desimaler.
    # Dette printer jeg til slutt ut.


if __name__ == "__main__":
    oppgave1()
    oppgave2()
