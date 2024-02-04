import pygame as pg
import constants as s
import network as n
import client_entity as p
from time import perf_counter
import utils as u


# a class which stores the game world
class World:
    def __init__(self):
        # size not needed - the world is infinite
        self.network = n.Network()
        # TODO: get the initial player position from the server
        self.client_entity = p.PlayerSpaceShip()
        self.projectiles = pg.sprite.Group()
        self.enemy_entities = pg.sprite.Group()
        self.window = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        self.clock = pg.time.Clock()
        self.mouse_pos = 0, 0
        self.last_time = perf_counter()

    def tick(self):
        dt = self.get_delta_time()
        # LOCAL CLIENT GAME LOOP
        self.event_handler()
        self.clock.tick(s.FPS)
        self.update(dt)
        self.draw()
        self.send_player_data()

    def update(self, delta_time):
        self.mouse_pos = pg.mouse.get_pos()
        # TODO: update the projectiles, enemies and player
        # TODO: if the enemy or projectile is too far, remove it from the storage
        pass

    def draw(self):
        # TODO: draw the player, enemies and projectiles
        pg.display.update()  # function to update the screen

    def send_player_data(self):
        # TODO: send the player data to the server AND receive the data from the server
        pass

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                if event.key == pg.K_SPACE:
                    # TODO: propel the player
                    pass
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # TODO shoot a projectile
                    pass

    def get_delta_time(self):
        dt = perf_counter() - self.last_time
        dt *= s.FPS
        self.last_time = perf_counter()
        return dt
