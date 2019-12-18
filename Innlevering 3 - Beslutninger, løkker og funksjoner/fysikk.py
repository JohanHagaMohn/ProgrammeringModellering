from numpy import sqrt, roots
# Importerer kvadratror og nullpunkter til definisjonene.
import sys
# Importerer sys for å kunne exite programmet


def fartsformel(args):
    """Returnerer liste med variabelindeks og verdi etter fartsformelen."""

    if args[4] == 0:
        return [0, args[1] - args[2] * args[3]]
    elif args[4] == 1:
        return [1, args[0] + args[2] * args[3]]
    elif args[4] == 2:
        return [2, (args[1] - args[0]) / args[3]]
    else:
        return [3, (args[1] - args[0]) / args[2]]

    # Sjekker fjerde parameter for å finne ut hvilken konstant som skal finnes.
    # Parametere 0-3 er konstanter etter deres indeks fra konstantlisten under.
    # 0 = Startfart, 1 = Sluttfart, 2 = Akselerasjon, 3 = Tid.
    # Returnerer en liste med konstantens ny indeks fra 0 - 4 og verdi.


def veiformel1(args):
    """Returnerer liste med variabelindeks og verdi etter veiformel 1."""

    if args[4] == 0:
        return [0, (2 * args[3]) / args[2] - args[1]]
    elif args[4] == 1:
        return [1, (2 * args[3]) / args[2] - args[0]]
    elif args[4] == 2:
        return [3, (2 * args[3]) / (args[0] + args[1])]
    else:
        return [4, 1 / 2 * (args[0] + args[1]) * args[2]]

    # Sjekker fjerde parameter for å finne ut hvilken konstant som skal finnes.
    # Parametere 0-3 er konstanter etter deres indeks fra konstantlisten under.
    # 0 = Startfart, 1 = Sluttfart, 2 = Tid, 3 = Strekning.
    # Returnerer en liste med konstantens ny indeks fra 0 - 4 og verdi.


def veiformel2(args):
    """Returnerer liste med variabelindeks og verdi etter veiformel 2."""

    if args[4] == 0:
        return [0, (args[3] - 1 / 2 * args[1] * args[2] ** 2) / args[2]]
    elif args[4] == 1:
        return [2, 2 * (args[3] - args[0] * args[2]) / args[2] ** 2]
    elif args[4] == 2:
        return [3, roots([args[1] / 2, args[0], -args[3]])[1]]
    else:
        return [4, args[0] * args[2] + 1 / 2 * args[1] * args[2] ** 2]

    # Sjekker fjerde parameter for å finne ut hvilken konstant som skal finnes.
    # Parametere 0-3 er konstanter etter deres indeks fra konstantlisten under.
    # 0 = Startfart, 1 = Akselerasjon, 2 = Tid, 3 = Strekning.
    # Returnerer en liste med konstantens ny indeks fra 0 - 4 og verdi.


def tidløs(args):
    """Returnerer liste med variabelindeks og verdi etter tidløs formel."""

    if args[4] == 0:
        return [0, sqrt(args[1] ** 2 - 2 * args[2] * args[3])]
    elif args[4] == 1:
        return [1, sqrt(args[0] ** 2 + 2 * args[2] * args[3])]
    elif args[4] == 2:
        return [2, (args[1] ** 2 - args[0] ** 2) / (2 * args[3])]
    else:
        return [4, (args[1] ** 2 - args[0] ** 2) / (2 * args[2])]

    # Sjekker fjerde parameter for å finne ut hvilken konstant som skal finnes.
    # Parametere 0-3 er konstanter etter deres indeks fra konstantlisten under.
    # 0 = Startfart, 1 = Sluttfart, 2 = Akselerasjon, 3 = Strekning.
    # Returnerer en liste med konstantens ny indeks fra 0 - 4 og verdi.


def main():

    konstanter = ["Startfart", "Sluttfart", "Akselerasjon", "Tid", "Strekning"]
    # Lager en liste med konstanter som er rekkefølgen programmet følger.

    print("\nTrykk enter på de du ikke har.\n")
    # Printer ut at enter signaliserer manglende input.

    løsning = [float(x) if x != '' else None for x in
               [input(f"{x}: ") for x in konstanter]]
    # Går igjennom hvert ord i konstanter-listen og spør brukeren om det.
    # Går så igjennom svarene og gjør tall om til float og "enter" til None.

    if sum([1 for x in løsning if x is None]) > 2:
        # Går igjennom besvarelsene og teller anntall manglende konstanter.

        print("Trenger minst tre verdier.")
        sys.exit(1)
        # Vi stopper det siden vi ikke kan løse formlene med < 2 variabler.

    elif løsning[3] is None:
        # Sjekker så om vi ikke har tiden - da kan vi få et umulig rotuttrykk.
        if (løsning[0] is None and løsning[1] ** 2 - 2 * løsning[2] *
            løsning[4] < 0) or (løsning[1] is None and løsning[0] ** 2 + 2 *
                                løsning[2] * løsning[4] < 0):
            # Sjekker begge mulighetene for negativt og uløselig rotuttrykk.

            print("Uttrykket har ingen løsninger.")
            sys.exit(1)
            # Stopper programmet.

    print("\n")
    # Nye linjer

    while True:
        # Starter en evig løkke for å finne alle konstantene.

        if all([x is not None for x in løsning]):
            # Går igjennom alle konstantene og sjekker om alle er løst.

            [print(f"{konstanter[x]}: {round(løsning[x], 3)}")
             for x in range(len(konstanter))]
            # Isåfall, går vi igjennom alle konstantene og utprinter verdiene.

            break
            # Går ut av løkken, vi er ferdige.

        for y in range(1, 5):
            # Går igjennom 4 verdier som hver av formlene ikke kan finne.

            if sum([1 for x in løsning if x is not None and x is not
                    løsning[y]]) == 3:
                # Nå som en er eliminert, sjekker vi om vi har 3 av de 4 andre.
                # Har vi det, kan uttrykket løses!

                variabler = tuple(løsning[x] for x in range(5) if x != y)
                # Genererer en tuple med de fire konstantene, der 3 er kjente.

                variabler += tuple(x for x in range(4) if variabler[x] is None)
                # Tillegger den ukjente indeksen så verdien så kan tillegges.

                if y == 4:
                    x = fartsformel(variabler)
                elif y == 2:
                    x = veiformel1(variabler)
                elif y == 1:
                    x = veiformel2(variabler)
                else:
                    x = tidløs(variabler)
                # Går igjennom hvilken ukjente verdi for å finne riktig formel.
                # Lagrer returlisten i variablen x.

                løsning[x[0]] = x[1]
                # Returlisten har både en indeks og verdi
                # Dermed, kan jeg enkelt legge den til i løsningslisten.


if __name__ == "__main__":
    # Kjører hovedprogrammet.
    main()
