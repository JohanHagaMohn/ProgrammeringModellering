from math import log10


def ph(konsentrasjon):
    """
    Returnerer pH gitt en konsentrasjon av oksoniumioner.

    Parameter:
    arg1 (float): Konsentrasjon av oksoniumioner i mol/L.

    Returverdi:
    string: pH-verdi med 2 gjeldende siffer.
    """

    return '{:#.2}'.format(-log10(konsentrasjon))

    # Importerer log10 fra math-biblioteket.
    # Finner pH-verdien med definitionen gitt i oppgavebeskrivelsen.
    # Bruker format()-funksjonen til å avrunde verdien til 2 gjeldende siffer.
    # Returnerer stringen.


def main():
    """Henter oksoniumionkonsentrasjon og printer samsvarende pH-verdi."""

    print(f"pH: {ph(eval(input('Oksoniumionkonsentrasjon: ').replace('^', '**')))}")

    # Bruker input()-funksjonen til å få oksoniumionkonsentrasjonen fra brukeren.
    # Replace()-funksjonen utbytter "^" med "**" hvis vitenskapelig notasjon er brukt.
    # Bruker eval()-funksjonen til gjøre string-uttrykket til én float.
    # Anvender ph-funksjonen og får samsvarende pH-verdi som string.
    # Printer verdien ut i en formattert string.


if __name__ == "__main__":
    # Kjører main()-funksjonen hvis filen er kjørt.
    main()
