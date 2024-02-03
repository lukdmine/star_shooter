import pygame as pg
import settings as s
import entity as e
import player as p
import network as n
import utils as u


# a class which stores the game world
class World:
    def __init__(self, window: pg.Surface, network: 'n.Network'):
        self.player = p.Player()
        self.projectiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.window = window
        self.clock = pg.time.Clock()
        self.mouse_pos = (0, 0)
        self.size = (s.W_WIDTH, s.W_HEIGHT)
        self.network = network
        self.enemy_position = 0, 0

    def tick(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.event_handler()
        self.clock.tick(s.FPS)
        self.update()
        self.draw()
        self.send_player_data()


    def update(self):
        self.player.update(self.mouse_pos)
        for projectile in self.projectiles:
            projectile.update(self.player)
        for enemy in self.enemies:
            enemy.update(self.player)

    def draw(self):
        # REMOVE AFTER TESTING
        self.create_enemy()

        self.window.fill(s.BLACK)
        self.player.update(self.mouse_pos)
        self.player.draw(self.window)
        self.projectiles.draw(self.window)
        self.enemies.draw(self.window)
        pg.display.update()

    def send_player_data(self):
        print(self.player.actual_pos)
        prep_pos = u.pack_player_data(self.player.actual_pos)
        # sending the player position and receiving the enemy position
        self.enemy_position = u.unpack_player_data(self.network.send(prep_pos))

    def create_enemy(self):
        enemy = e.Enemy(self.enemy_position, (0, 0))
        # REMOVE AFTER TESTING
        self.enemies.empty()

        self.enemies.add(enemy)

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
                    # propel the player spaceship
                    self.player.spaceship.propel()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # shoot a projectile
                    pass
