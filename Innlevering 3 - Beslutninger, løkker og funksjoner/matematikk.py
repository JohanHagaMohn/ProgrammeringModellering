for n in range(11):
    # Lager en løkke som går igjennom tall 0 til og med 10.

    løsninger = 0
    # Løsninger vil telle anntall løsninger.

    uttrykk = []
    # Uttrykk vil samle sammen løsninger i en liste av tupler.

    for x in range(-100, 101):
        # Går gjennom tallene -100 t.o.m. 100.

        for y in range(-100, 101):
            # Går gjennom tallene -100 t.o.m. 100.

            for z in range(-100, 101):
                # Går gjennom tallene -100 t.o.m. 100.

                if x ** 3 + y ** 3 + z ** 3 == n:
                    # Sjekker om den diofantiske likningen stemmer.

                    løsninger += 1
                    # Gjør den det, øker vi anntall løsninger.

                    uttrykk.append((x, y, z))
                    # Deretter legger vi til x, y og z verdiene som en tupel i listen.

    print(f"For n = {n}, finnes {løsninger} løsning(er).\n{uttrykk}")
    # Etter hver n verdi printes ut anntall løsninger og deres uttrykk.
