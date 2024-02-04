import world as w
import pygame as pg


def main():
    pg.init()
    print('Game started')
    game_world = w.World()
    while True:
        game_world.tick()


if __name__ == '__main__':
    main()
