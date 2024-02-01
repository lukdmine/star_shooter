import pygame as pg
import settings as s
import entity as e
import player as p
import utils as u


# a class which stores the game world
class World:
    def __init__(self, window: pg.Surface):
        self.player = p.Player()
        self.projectiles = []
        self.enemies = []
        self.window = window
        self.clock = pg.time.Clock()
        self.mouse_pos = (0, 0)

    def tick(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.event_handler()
        self.clock.tick(s.FPS)
        self.update()
        self.draw()

    def update(self):
        self.player.update(self.mouse_pos)
        for projectile in self.projectiles:
            projectile.update(self.player)
        for enemy in self.enemies:
            enemy.update(self.player)

    def draw(self):
        self.window.fill(s.BLACK)
        self.player.draw(self.window)
        for projectile in self.projectiles:
            projectile.draw(self.window)
        for enemy in self.enemies:
            enemy.draw(self.window)
        pg.display.update()

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
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.projectiles.append(e.PlayerProjectile(self.player.spaceship.position,
                                                               self.player.spaceship.projectile_damage,
                                                               self.player.spaceship.heading))
