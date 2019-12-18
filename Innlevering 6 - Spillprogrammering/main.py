import pygame as pg
from simplejson import load
from pylab import array

def main():
    pg.init()
    
    window = pg.display.set_mode((1280, 800))
    pg.display.set_caption("Organsjakk")
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.USEREVENT])
    
    
    bg = pg.transform.scale(pg.image.load("./Grafikk/Bakgrunn.jpg"), (1280, 800))
    fg = pg.transform.scale(pg.image.load("./Grafikk/Startmeny.png"), (1280, 800))
    
    window.blit(bg, (0, 0))
    window.blit(fg, (0, 0))
    
    Board()
    
    running = True
    
    while running:
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.pos[0] > 275 and e.pos[0] < 1000 and e.pos[1] > 500 and e.pos[1] < 675:
                    window.blit(pg.transform.scale(pg.image.load("./Grafikk/Bakgrunn.jpg"), (1280, 800)), (0, 0))
                    window.blit(pg.transform.scale(pg.image.load("./Grafikk/Sjakkbrett.png"), (1280, 800)), (0, 0))

    pg.quit()
    quit()


class Board():
    def __init__(self):
        self.board = [[None for i in range(8)] for i in range(8)]
        
        with open('./pieces.json', "r") as file:
            for piece in load(file):
                for i in range(len(piece["position"])):

                    movement = sum(array(piece["movement"]) * i \
                                   for i in range(1, piece["scalar"] + 1))
                    
                    Piece(piece.key(), piece["position"][i], False, movement, \
                          piece["image"])
    
    
    def move(self, previous, current, name):
        self.board[previous[0]][previous[1]] = None
        self.board[current[0]][current[1]] = name
    
    
    def update(self):
        pass


class Piece():
    def __init__(self, name, position, player, movement, image):
        self.previous = (0, 1)
        self.current = position
        self.name = name.capitalize()
        self.player = player
        self.move = movement
        self.image = image

    def show(self):
        pass

    def die(self):
        self.dead = True
    
    def select(self):
        pass
    
    def move(self):
        pass
    
if __name__ == "__main__":
    main()
