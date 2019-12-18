from pylab import plot


def a():
    """Øker populasjonen med 62% 15 ganger, én gang etter hver time."""

    print(f"{round(1000 * 1.62 ** 15)} CFU")

    # Her ganger jeg startkolonien på 1000 med (1 + 62%) per time i 15 timer.
    # Dette avrunder jeg med round() for å få et heltall.
    # Når dette utprintes, fås 1 389 073 og ikke  2 250 299 som i fasiten.
    # Det er kun etter 16 timer man vil få 2 250 299, ikke 15 som i oppgaven:

    """
    For å illustrere det bedre, kan vi printe ut verdien etter hver time slik:
    
    [print(f"Etter {x} timer: {round(1000 * 1.62 ** x)}") for x in range(17)]
    
    Og få følgende resultater:
    
    Etter 0 timer: 1000
    Etter 1 timer: 1620
    Etter 2 timer: 2624
    Etter 3 timer: 4252
    Etter 4 timer: 6887
    Etter 5 timer: 11158
    Etter 6 timer: 18075
    Etter 7 timer: 29282
    Etter 8 timer: 47437
    Etter 9 timer: 76848
    Etter 10 timer: 124494
    Etter 11 timer: 201681
    Etter 12 timer: 326723
    Etter 13 timer: 529292
    Etter 14 timer: 857453
    Etter 15 timer: 1389073
    Etter 16 timer: 2250299
    """


def b():
    """Lagrer tid og antall i hver sin liste."""

    t = [x for x in range(16)]
    # Liste med alle tall fra og med 0 til og med 15.

    B = [round(1000 * 1.62 ** x) for x in t]
    # Liste med antall CFU-enheter fra etter 0 timer til og med etter 15 timer.
    # Jeg ganger 1000 med 1.62 etter hver time for å lage listen.
    # Dette runder jeg av for å få renere tall.
    # Istedenfor å skrive range(16) to ganger, går jeg igjennom t-listen.

    """
    Jeg må her gange 1000 med 1.62 105 ekstra ganger enn hvis jeg hadde lagt
    hvert tall til i listen etter hver gang jeg ganget. Siden jeg ikke har
    fokus på ytelse, tenker jeg heller på hvordan gjøre det enklest mulig. Hvis
    ikke, kunne jeg gjort det slik:
        
    B = [1000]
    
    # Her starter jeg listen med verdien etter 0 timer.
    
    [B.append(round(B[x - 1] * 1.62)) for x in range(1, 16)]
    
    # Jeg ganger den tidligere verdien med 1.62, nedrunder og legger den til.
    
    Problemet da er at nedrundingen blir større og større og kan gi unnøyaktige
    resultater.
    """


def c():
    """Plotter antall bakterier som funksjon av tid ved bruk av pylab."""

    # Importerer pylab øverst i programmet

    t = [x for x in range(16)]
    B = [round(1000 * 1.62 ** x) for x in t]
    # Tar listene laget i forrigje oppgave.

    plot(t, B)
    # Bruker plot()-funksjonen til å plotte t og B som i oppgavebeskrivelsen.
    # Her er t x-aksen og B y-aksen.


def d():
    """Beregner populasjonsvekst med begrensning på (1500 * 500) CFU."""

    t = [x for x in range(16)]
    # Tar liste t fra oppgave b.

    B = [round(1000 * 1.62 ** x) if 1000 * 1.62 ** x < 1500 * 500
         else 1500 * 500 for x in t]
    # Tar liste B fra oppgave b, og gir maks populasjon om grensen overstiges.

    plot(t, B)
    # Bruker plot()-funksjonen til å plotte funksjonen.

    """
    Istedenfor å "stoppe" veksten kun etter den har overstiget grensen som skjer
    i testresultatet, har jeg valgt å sette populasjonen til bæreevnen når
    grensen er nådd, som er 750 000.
    
    Dette vil ikke gi en riktig logistisk vekstkurve som vil
    være naturlig ettersom bakteriekulturen må konkurrere om mat og sakne
    vekstraten, men her vil bæreevnen i det minste ikke overstiges som i
    testresultatet gitt i oppgavebeskrivelsen.
    
    Jeg mener dermed at jeg har bedre svart på oppgaven om å lage "et program 
    som på nytt beregner antall bakterier og plotter utviklingen over 15 timer.
    " enn det som står i testresultatet.
    """


if __name__ == "__main__":
    # Kjører en av funksjonene når filen kjøres (ukommenter).

    a()
    # b()
    # c()
    # d()
