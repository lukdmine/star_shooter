import game as g
import pygame as pg


def main():
    pg.init()
    print('Game started')
    game = g.Game()
    game.run()


if __name__ == '__main__':
    main()
