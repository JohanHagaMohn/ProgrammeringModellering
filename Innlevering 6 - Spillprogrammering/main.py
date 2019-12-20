from json import load
from pylab import array, append
import pygame as pg

# Ikke konstante konstanter
DEFAULT = (1280, 800)
WINDOW = pg.display.set_mode(DEFAULT, pg.RESIZABLE)
SIZE = DEFAULT
TITLE = True
TILE = [71, 71]


def main():
    """ Initialiserer pygame """
    global SIZE, TITLE
    pg.init()

    pg.display.set_caption("Organsjakk")

    # Legger til bakgrunn
    blit("Bakgrunn.jpg")
    blit("Startmeny.png")

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


class Board():
    """ Sjakkbrettklasse """
    def __init__(self):
        """ Lager en tom 8x8 liste og kjører create_pieces som initialiserer brettet. """

        self.board = [[None for i in range(8)] for i in range(8)]
        self.checked = False
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
        if not self.checked:
            if not piece["checked"]:
                for i in range(len(piece["movement"][0])):
                    for j in range(len(piece["movement"])):
                        movement = array(piece["movement"][j][i])
                        if piece["player"]:
                            movement *= -1
                        movement[0], movement[1] = movement[1], movement[0]
                        coord = (array(pos) + movement).tolist()
                        if coord[0] < 0 or coord[0] > 7 or coord[
                                1] < 0 or coord[1] > 7:
                            break
                        piece["checked"].append(coord)
                        if self.board[coord[0]][coord[1]]:
                            break
                if piece["checked"]:
                    self.checked = pos
                    self.update()
        else:
            self.board[self.checked[0]][self.checked[1]]["checked"] = []
            self.move(self.checked, pos)
            self.checked = False

        # if player's move: (if not piece or piece["player"])

        # player's move is false
        

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


def blit(path, dim=DEFAULT, pos=(0, 0)):
    """ Legger bilder til på skjermen. """

    WINDOW.blit(pg.transform.scale(pg.image.load(f"./Media/{path}"), dim), pos)


def hitbox(pos, coords):
    """ Finner ut om et museklikk er innenfor en hitboks, uavhendig av skjermoppløsning. """

    scaling = array([SIZE[0] / DEFAULT[0], SIZE[1] / DEFAULT[1]])
    coords = array(coords) * scaling
    return all(pos[i] > coords[0][i] and pos[i] < coords[1][i]
               for i in range(2))


if __name__ == "__main__":
    main()
""" global TURN, CHECKED
        if piece and not CHECKED:
            for i in range(len(piece["movement"])):
                for j in range(len(piece["movement"][i])):
                    movement = array(piece["movement"][i][j])
                    if piece["player"]:
                        movement *= -1
                    movement[0], movement[1] = movement[1], movement[0]
                    coord = (array(pos) + movement).tolist()
                    print(piece, coord, movement, pos)
                    if coord[0] < 0 or coord[0] > 7 or coord[1] < 0 or coord[
                            1] > 7:
                        print("heyyy")
                        break
                    elif self.board[coord[0]][coord[1]] and self.board[pos[0]][
                            pos[1]]["name"] != "Bukspyttkjertel":
                        if self.board[coord[0]][coord[1]]["player"] == TURN:
                            print("hey")
                            continue
                        else:
                            self.board[coord[0]][coord[1]]["checked"] = pos
                            print("hi")
                            break
                    else:
                        self.board[coord[0]][coord[1]] = {
                            "image": "Tile.png",
                            "checked": pos
                        }
            self.update()
        elif CHECKED and self.board[pos[0]][pos[1]]:
            if self.board[pos[0]][pos[1]]["checked"]:
                self.move(self.board[pos[0]][pos[1]]["checked"], pos)
        CHECKED = not CHECKED """

""" global CHECKED
        if CHECKED and self.board[pos[0]][pos[1]]:
            if self.board[pos[0]][pos[1]]["checked"]:
                self.move(self.board[pos[0]][pos[1]]["checked"], pos)
            CHECKED = False
        elif piece:
            for i in range(len(piece["movement"])):
                for j in range(len(piece["movement"][i])):
                    movement = array(piece["movement"][i][j])
                    if piece["player"]:
                        movement *= -1
                    movement[0], movement[1] = movement[1], movement[0]
                    coord = (array(pos) + movement).tolist()
                    if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[
                            0] < 0:
                        if len(piece["movement"]) == 1:
                            continue
                        else:
                            break
                    elif self.board[coord[0]][coord[1]]:
                        if self.board[coord[0]][coord[1]]["player"] == TURN:
                            break
                        else:
                            self.board[coord[0]][coord[1]]["checked"] = pos
                            break
                    else:
                        self.board[coord[0]][coord[1]] = {
                            "image": "Tile.png",
                            "checked": pos
                        }
            CHECKED = True
            self.update() """
""" global TURN, CHECKED
        if piece and not CHECKED:
            for i in range(len(piece["movement"])):
                for j in range(len(piece["movement"][i])):
                    movement = array(piece["movement"][i][j])
                    if piece["player"]:
                        movement *= -1
                    movement[0], movement[1] = movement[1], movement[0]
                    coord = (array(pos) + movement).tolist()
                    if coord[0] < 0 or coord[0] > 7 or coord[1] < 0 or coord[
                            1] > 7:
                        break
                    elif self.board[coord[0]][coord[1]]:
                        if self.board[coord[0]][coord[1]]["player"] == TURN:
                            break
                        else:
                            self.board[coord[0]][coord[1]]["checked"] = pos
                            break
                    else:
                        self.board[coord[0]][coord[1]] = {
                            "image": "Tile.png",
                            "checked": pos
                        }
            CHECKED = True
        elif CHECKED and self.board[pos[0]][pos[1]]:
            if self.board[pos[0]][pos[1]]["checked"]:
                self.move(self.board[pos[0]][pos[1]]["checked"], pos)
                CHECKED = False """
"""global CHECKED
    if CHECKED:
        if self.board[pos[0]][pos[1]]:
            self.move(self.board[pos[0]][pos[1]]["checked"], pos)
        CHECKED = False
    elif piece:
        for i in range(len(piece["movement"])):
            for j in range(len(piece["movement"][i])):
                movement = array(piece["movement"][i][j])
                if piece["player"]:
                    movement *= -1
                movement[0], movement[1] = movement[1], movement[0]
                coord = (array(pos) + movement).tolist()
                if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[
                        0] < 0:
                    if len(piece["movement"]) == 1:
                        continue
                    else:
                        break
                if self.board[coord[0]][coord[1]]:
                    self.board[coord[0]][coord[1]]["checked"] = pos
                    break
                else:
                    self.board[coord[0]][coord[1]] = {
                        "image": "Tile.png",
                        "checked": pos
                    }
        CHECKED = True
        self.update()"""
""" def recur(i, j, tiling, hit=False):
            if hit or j == len(piece["movement"][i]):
                return i, j, tiling, True
            xy = piece["movement"][i][j]
            if self.board[xy[0]][xy[1]]:
                self.board[xy[0]][
                    xy[1]]["tile"] = "Tile.png" if tiling else False
                self.board[xy[0]][xy[1]]["path"] = pos if tiling else False
                return i, j, tiling, True
            else:
                self.board[xy[0]][xy[1]] = {
                    "tile": "Tile.png",
                    "path": pos
                } if tiling else False
            return recur(i, j + 1, tiling)

        if CHECKED:
            self.move(self.board[pos[0]][pos[1]]["path"], pos)

        for i in range(len(piece["movement"])):
            recur(i, 0, not CHECKED)

        if not CHECKED:
            self.update()

        print(self.board) """
""" if CHECKED:
            coord = self.board[pos[0]][pos[1]]
            if coord:
                if coord["image"] == "Tile.png":
                    self.move(coord["name"], pos)
                    coord = None
                elif coord["checked"]:
                    self.move(coord["checked"], pos)
                    coord["checked"] = False
            CHECKED = False
        elif piece:
            for i in range(len(piece["movement"])):
                for j in range(len(piece["movement"][i])):
                    movement = array(piece["movement"][i][j])
                    if piece["player"]:
                        movement *= -1
                    movement[0], movement[1] = movement[1], movement[0]
                    coord = (array(pos) + movement).tolist()
                    if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[
                            0] < 0:
                        if len(piece["movement"]) == 1:
                            continue
                        else:
                            break
                    if self.board[coord[0]][coord[1]]:
                        self.board[coord[0]][coord[1]]["checked"] = pos
                        break
                    else:
                        self.board[coord[0]][coord[1]] = {
                            "image": "Tile.png",
                            "name": pos
                        }
            CHECKED = True
            self.update() """
""" print(piece, pos)
        global CHECKED
        while CHECKED:
            if self.board[pos[0]][pos[1]]:
                if self.board[pos[0]][pos[1]]["checked"]:
                    previous = self.board[pos[0]][pos[1]]["checked"]
                    self.move(previous, pos)
                    try:
                        if self.board[previous[0]][previous[1]]["name"]:
                            self.board[previous[0]][
                                previous[1]]["checked"] = False
                    except (KeyError, TypeError):
                        self.board[previous[0]][previous[1]] = None
                    CHECKED = False
                    return 0
            if piece:
                self.update()
            CHECKED = False

        for i in range(len(piece["movement"])):
            for j in range(len(piece["movement"][i])):
                movement = array(piece["movement"][i][j])
                if piece["player"]:
                    movement *= -1
                movement[0], movement[1] = movement[1], movement[0]
                coord = (array(pos) + movement).tolist()

                if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[0] < 0:
                    break
                blit("Tile.png", TILE, self.coordinates(coord[0], coord[1]))
                checking = True
                try:
                    self.board[coord[0]][coord[1]]["checked"] = pos
                except:
                    self.board[coord[0]][coord[1]] = {"checked": pos}

                if self.board[coord[0]][coord[1]]:
                    break
        CHECKED = True """