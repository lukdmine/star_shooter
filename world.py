import pygame as pg
import pygame.sprite
from random import randint
import _thread
import pickle
from time import perf_counter

import box as b
import constants as s
import network as n
import client_entity as p
import utils as u
import projectile as pr
import enemy_entity as e

# a class which stores the game world
class World:
    def __init__(self):
        # size not needed - the world is infinite
        # network
        self.network = n.Network()

        # init player position
        player_pos = pg.Vector2(self.network.get_init_client_pos())

        # sprite groups
        self.client_entity = p.PlayerSpaceShip(init_pos=player_pos)
        self.projectiles = pg.sprite.Group()
        self.enemy_entities = pg.sprite.Group()
        self.stars = pg.sprite.Group()

        # list of projectiles that were shot by the player
        self.shot_projectiles = []

        # pygame objects
        self.window = pg.display.set_mode((s.WIN_WIDTH, s.WIN_HEIGHT))
        self.clock = pg.time.Clock()
        self.mouse_pos = 0, 0
        self.last_time = perf_counter()
        self.star_clusters: list[StarCluster] = []
        self.current_cluster: StarCluster | None = None

        # thread for sending and receiving data from the server
        _thread.start_new_thread(self.send_player_data, ())
        self.new_data_loaded = False  # flag for new data to send to the server

    def tick(self):
        dt = self.get_delta_time()
        # LOCAL CLIENT GAME LOOP
        self.event_handler()
        self.clock.tick(s.FPS)
        self.update(dt)
        self.draw()
        self.new_data_loaded = True

    def update(self, delta_time):
        self.mouse_pos = pg.mouse.get_pos()
        # TODO: update the projectiles, enemies and player
        # TODO: if the enemy or projectile is too far, remove it from the storage
        self.projectiles.update(delta_time, self.client_entity.position)
        self.client_entity.update(delta_time, self.mouse_pos)
        self.update_star_cluster()
        self.update_enemy_entities()


    def draw(self):
        self.window.fill(s.BLACK)

        self.client_entity.draw(self.window)
        self.enemy_entities.draw(self.window)
        self.projectiles.draw(self.window)
        self.draw_stars()

        pg.display.update()  # function to update the screen

    def send_player_data(self):
        # TODO: send the player data to the server AND receive the data from the server
        while True:
            if self.new_data_loaded:
                self.new_data_loaded = False  # reset the flag

                box = self.box_current_state()
                received_box_bytes = self.network.send(pickle.dumps(box))
                received_box = pickle.loads(received_box_bytes)

                self.load_received_data(received_box)

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
                    self.client_entity.propel()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_projectile = self.client_entity.shoot()
                    # TODO: send the projectile data to the server
                    self.projectiles.add(new_projectile)
                    self.shot_projectiles.append(new_projectile)

    def get_delta_time(self):
        dt = perf_counter() - self.last_time
        dt *= s.DELTA_FPS  # wanted fps
        self.last_time = perf_counter()
        return dt

    def update_star_cluster(self):
        for cluster in self.star_clusters:
            cluster.stars.update(self.client_entity.position)
        current_cluster_position = self.get_current_cluster_position()
        # cluster not changed
        if self.current_cluster is not None and self.current_cluster.position == current_cluster_position:
            return

        print('cluster changed')
        # cluster changed -> generating new stars and deleting too far ones
        self.set_current_cluster(current_cluster_position)
        assert self.current_cluster is not None

        new_live_clusters_coords = self.current_cluster.get_adjacent_cluster_coords()
        for index, cluster in enumerate(self.star_clusters):
            # deleting not adjacent clusters
            if cluster.position not in new_live_clusters_coords:
                self.star_clusters.pop(index)
                continue
            new_live_clusters_coords.remove(cluster.position)

        # generating new clusters
        _thread.start_new_thread(self.generate_new_clusters, (new_live_clusters_coords,))

    def generate_new_clusters(self, new_live_clusters_coords):
        for new_cluster_coords in new_live_clusters_coords:
            new_cluster = StarCluster(new_cluster_coords)
            self.star_clusters.append(new_cluster)

    def get_current_cluster_position(self):
        cluster_position = pygame.Vector2(self.client_entity.position.x // s.CLUSTER_SIDE_SIZE, self.client_entity.position.y // s.CLUSTER_SIDE_SIZE)
        return cluster_position

    def set_current_cluster(self, current_cluster_position):
        for cluster in self.star_clusters:
            if cluster.position == current_cluster_position:
                self.current_cluster = cluster
                return
        # init of first cluster
        self.current_cluster = StarCluster(current_cluster_position)

    def draw_stars(self):
        for cluster in self.star_clusters:
            cluster.stars.draw(self.window)

    def box_current_state(self):
        new_box = b.Box()
        new_box.client_entity = self.client_entity.transform_to_server_player()
        for projectile in self.shot_projectiles:
            new_box.add_entity(projectile.transform_to_server_projectile())
        self.shot_projectiles.clear()
        return new_box

    def load_received_data(self, received_box: b.Box):
        for entity in received_box.entities:
            if isinstance(entity, pr.ServerProjectile):
                self.projectiles.add(pr.Projectile(entity.position, entity.speed, 'enemy', entity.damage))
            if isinstance(entity, e.ServerSpaceShip):
                # if the enemy is too far don't save it
                if entity.position.distance_to(self.client_entity.position) > s.ENEMY_RENDER_DISTANCE:
                    continue
                updated = False
                for enemy in self.enemy_entities:
                    if enemy.id == entity.id:
                        print(entity.heading)
                        enemy.update(entity.position, entity.hp, entity.heading, self.client_entity.position)
                        updated = True

                # if the enemy is already loaded don't generate it
                if updated:
                    return
                self.enemy_entities.add(e.EnemySpaceShip(entity.id, entity.position, entity.hp, entity.heading))

    def update_enemy_entities(self):
        for entity in self.enemy_entities:
            assert isinstance(entity, e.EnemySpaceShip)
            if entity.position.distance_to(self.client_entity.position) < 1500:
                continue
            entity.kill()


class Star(pg.sprite.Sprite):
    def __init__(self, init_pos):
        pg.sprite.Sprite.__init__(self)
        self.position = init_pos
        self.image = u.load_image('star.png', s. STAR_SIZE)
        self.rect = self.image.get_rect()
        # window pos updated in update function
        self.rect.center = init_pos

    def update(self, player_pos):
        self.rect.center = self.position - player_pos + pg.Vector2(s.WIN_WIDTH // 2, s.WIN_HEIGHT // 2)


class StarCluster:
    def __init__(self, position: pygame.Vector2):
        self.stars = pygame.sprite.Group()
        self.position = position
        self.generate_stars()

    def get_adjacent_cluster_coords(self):
        adjacent_coords = []
        for x in range(int(self.position.x) - 1, int(self.position.x) + 2):
            for y in range(int(self.position.y) - 1, int(self.position.y) + 2):
                adjacent_coords.append(pygame.Vector2(x, y))
        return adjacent_coords

    def generate_stars(self):
        for _ in range(s.STAR_COUNT):
            star = Star(pygame.Vector2(randint(self.position.x * s.CLUSTER_SIDE_SIZE, (self.position.x + 1) * s.CLUSTER_SIDE_SIZE),
                                       randint(self.position.y * s.CLUSTER_SIDE_SIZE, (self.position.y + 1) * s.CLUSTER_SIDE_SIZE)))
            self.stars.add(star)
