from json import load
from pylab import array, append
import pygame as pg

# Ikke konstante konstanter (den beste typen konstanter)
DEFAULT = (1280, 800)
WINDOW = pg.display.set_mode(DEFAULT, pg.RESIZABLE)
SIZE = DEFAULT
TITLE = None
TILE = [71, 71]


def main():
    """ Initialiserer pygame """
    global SIZE, TITLE
    pg.init()

    pg.display.set_caption("Organsjakk")

    menu()

    # Legger til musikk
    pg.mixer.music.load("./Media/Musikk.wav")
    pg.mixer.music.play(-1)

    # Lager en class
    board = Board()

    # Starter en while-løkke for å hente hendelser.
    running = True
    while running:
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Sjekker om startmenyen treffes og oppdaterer skjermen.
                if TITLE and hitbox(e.pos, [(275, 500), (1000, 675)]):
                    TITLE = False
                    blit("Bakgrunn.jpg")
                    board.update()
                # Sjekker om sjakkbretter treffes og oppdaterer skjermen.
                elif not TITLE and hitbox(e.pos, [(327, 83), (952, 712)]):
                    board.select(e.pos)
            elif e.type == pg.VIDEORESIZE:
                SIZE = tuple(e.dict['size'])

    # Slutter programmer ved pg.QUIT.
    pg.quit()
    quit()


def menu():
    """ Legger til bakgrunn. """
    global TITLE
    TITLE = True
    blit("Bakgrunn.jpg")
    blit("Startmeny.png")


def blit(path, dim=DEFAULT, pos=(0, 0)):
    """ Legger bilder til på skjermen. """

    WINDOW.blit(pg.transform.scale(pg.image.load(f"./Media/{path}"), dim), pos)


def hitbox(pos, coords):
    """ Finner ut om et museklikk er innenfor en hitboks, uavhengig av skjermoppløsning. """

    scaling = array([SIZE[0] / DEFAULT[0], SIZE[1] / DEFAULT[1]])
    coords = array(coords) * scaling
    return all(pos[i] > coords[0][i] and pos[i] < coords[1][i]
               for i in range(2))


class Board():
    """ Sjakkbrettklasse """
    def __init__(self):
        """ Lager en tom 8x8 liste og kjører create_pieces som initialiserer brettet. """

        self.board = [[None for i in range(8)] for i in range(8)]
        self.checked = False
        self.player = True
        self.create_pieces()

    def create_pieces(self):
        """ Henter data fra pieces.json og utfyller brettet."""

        with open('./pieces.json', "r") as file:
            for key, value in load(file).items():
                # Legger sammen skalerte vektorer
                movement = [(array(value["movement"]) * i).tolist()
                            for i in range(1, value["scalar"] + 1)]
                # Går igjennom alle brikker to ganger
                for i in range(len(value["position"])):
                    for j in range(2):
                        # En må være spiller
                        player = False if j == 0 else True
                        # Inverterer koordinatene for spilleren
                        position = value["position"][i] if j == 0 else [
                            7 - value["position"][i][0], 7 -
                            value["position"][i][1]
                        ]
                        # Lager en dict med info om brikkene
                        self.board[position[1]][position[0]] = {
                            "name": key.capitalize(),
                            "player": player,
                            "movement": movement,
                            "image": value["image"],
                            "checked": []
                        }

    def move(self, old, new):
        """ Flytter en brikke og oppdaterer skjermen """

        # Sjekker om kongen drepes.
        if self.board[new[0]][new[1]]:
            try:
                if self.board[new[0]][new[1]]["name"] == "Lever":
                    # Starter så på nytt
                    self.__init__()
                    menu()
                    return 0
            except KeyError:
                pass

        # Erstatter gamle koordinater med nye og erstatter eventuelle brikker.
        self.board[new[0]][new[1]] = self.board[old[0]][old[1]]
        self.board[old[0]][old[1]] = None

        # Oppdaterer og tar bort eventuelle markeringer
        self.update()

    def coordinates(self, i, j):
        """ Returnerer approx. pixel-verdier til hver av rutene basert på indexen. """

        return [328 + 79 * j, 88 + 79 * i]

    def update(self):
        """ Oppdaterer skjermen. """

        blit("Sjakkbrett.png")
        # Legger kun til sjakkbrettet for tillagt effekt.

        # Looper igjennom alle rutene
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    # Legger til bilde og eventuelle markøringer
                    blit(self.board[i][j]["image"], TILE,
                         self.coordinates(i, j))
                    if self.board[i][j]["checked"]:
                        for x, y in self.board[i][j]["checked"]:
                            blit("Tile.png", TILE, self.coordinates(x, y))

    def check(self, piece, pos):
        """ Sjekker om brikken skal flyttes eller om lovlige trekk skal vises. """
        
        # Er ingenting selektert?
        if not self.checked:
            # Sjekker om brikken som markeres er riktig.
            if piece:
                if piece["player"] != self.player:
                    return 0
            # Går igjennom trekkene i skalerende rekkefølge
            for i in range(len(piece["movement"][0])):
                for j in range(len(piece["movement"])):
                    # Gjør om til array
                    movement = array(piece["movement"][j][i])
                    # Inverterer arrayen ved spillerbrikke
                    if piece["player"]:
                        movement *= -1
                    # Reverserer arrayen fordi det er stress å endre alle i json filen
                    movement[0], movement[1] = movement[1], movement[0]
                    # Legger sammen arrayen med brikkens posisjon
                    coord = (array(pos) + movement).tolist()
                    # Hvis trekket er utenfor brettet, gå til neste retning
                    if coord[0] < 0 or coord[0] > 7 or coord[1] < 0 or coord[
                            1] > 7:
                        break
                    # Hvis det er en tarm, blir livet igjen litt styr
                    elif piece["name"] == "Tarm":
                        attacks = [(array(coord) + array([0, 1])).tolist(),
                                   (array(coord) + array([0, -1])).tolist()]
                        for attack in attacks:
                            if not (attack[0] < 0 or attack[0] > 7
                                    or attack[1] < 0 or attack[1] > 7):
                                if self.board[attack[0]][attack[1]]:
                                    if piece["player"] != self.board[
                                            attack[0]][attack[1]]["player"]:
                                        piece["checked"].append(attack)
                        if self.board[coord[0]][coord[1]]:
                            break
                        else:
                            # Dobbelt steg ved første tarmtrekk
                            double = (array(pos) + movement * 2).tolist()
                            start = 6 if piece["player"] else 1
                            if not self.board[double[0]][double[1]] and pos[0] == start:
                                piece["checked"].append(double)
                    # Hvis trekket møter en egen brikke, gå til neste retning
                    elif self.board[coord[0]][coord[1]]:
                        if self.board[coord[0]][coord[1]]["player"] == piece["player"]:
                            break
                    # Legger til trekket
                    piece["checked"].append(coord)
                    # Hvis trekket møter en motstanderbrikke, gå til neste retning
                    if self.board[coord[0]][coord[1]]:
                        break
            # Oppdaterer posisjonen med markører hvis det var noen gyldige trekk
            if piece["checked"]:
                # Lagrer brikkens posisjon som vi kan bruke senere
                self.checked = pos
                self.update()
        else:
            # Sjekker om brikken som flyttes er riktig.
            if self.board[self.checked[0]][
                self.checked[1]]["player"] != self.player:
                return 0
            # Finner ut om trekket sammenfaller med et gyldig trekk
            valid = pos in self.board[self.checked[0]][
                self.checked[1]]["checked"]
            # Tarmen forfremmes hvis trekket er mulig
            if valid and self.board[self.checked[0]][
                    self.checked[1]]["name"] == "Tarm":
                # Sjekker om tarmen når andre side
                other_side = 0 if self.board[self.checked[0]][
                    self.checked[1]]["player"] else 7
                if pos[0] == other_side:
                    # Henter hjertedata
                    with open('./pieces.json', "r") as file:
                        for key, value in load(file).items():
                            if key.capitalize() == "Hjerte":
                                # Oppdaterer tarmens data
                                movement = [
                                    (array(value["movement"]) * i).tolist()
                                    for i in range(1, value["scalar"] + 1)
                                ]
                                self.board[self.checked[0]][
                                    self.checked[1]] = {
                                        "name":
                                        key.capitalize(),
                                        "player":
                                        self.board[self.checked[0]][
                                            self.checked[1]]["player"],
                                        "movement":
                                        movement,
                                        "image":
                                        value["image"],
                                        "checked": []
                                    }
            # Resetter listen
            self.board[self.checked[0]][self.checked[1]]["checked"] = []
            # Flytter brikken om trekket er gyldig, ellers tas bort markørene
            if valid:
                # Bytter tur
                self.player = not self.player
                self.move(self.checked, pos)
            else:
                self.update()
            # Resetter checked
            self.checked = False

    def select(self, pos):
        """ Går igjennom hitboksen og finner indexen. """
        for i in range(8):
            for j in range(8):
                if self.board[i][j] or self.checked:
                    coords = self.coordinates(i, j)
                    if hitbox(
                            pos,
                        [(coords[0], coords[1] - 6 - round(4.5 * i)),
                         (70 + coords[0], 61 + coords[1] - round(4.5 * i))]):
                        self.check(self.board[i][j], [i, j])


if __name__ == "__main__":
    main()
