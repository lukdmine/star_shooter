import socket
import _thread
import sys
import utils as u
import uuid
import random
import pickle
from time import perf_counter

import constants as s
import enemy_entity as e
import projectile as p
import client_entity as c
import box as b
import pygame as pg

server = '127.0.0.1'
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# linking the server to the port
try:
    server_socket.bind((server, port))
except socket.error as e:
    print(str(e))

server_socket.listen(2)  # number of possible connections

print('waiting for connection')

# TODO: store the data of players, projectiles and enemies
# DATA STRUCTURES HERE


class ServerWorld:
    def __init__(self):
        self.players: dict[uuid.UUID, e.ServerSpaceShip | None] = {}
        self.projectiles = []
        self.to_send_projectiles: dict[uuid.UUID, list[p.Projectile]] = {}

        # time between updates
        self.last_time = perf_counter()

        self.clock = pg.time.Clock()

    def add_player(self, player_id: uuid.UUID):
        # initialize the player in storage
        self.players[player_id] = None
        self.to_send_projectiles[player_id] = []

    def update_player(self, client_entity: c.ServerPlayer, player_id: uuid.UUID):
        # convert the player to enemy entity and add it to the players list
        self.players[player_id] = e.ServerSpaceShip(player_id, client_entity.position, client_entity.hp, client_entity.heading)

    def remove_player(self, player_id: uuid.UUID):
        self.players.pop(player_id)
        self.to_send_projectiles.pop(player_id)

    def update_by_client(self, box: b.Box, player_id: uuid.UUID):
        self.update_player(box.client_entity, player_id)
        for projectile in box.entities:
            self.projectiles.append(projectile)
            for player in self.players:
                if player != player_id:
                    self.to_send_projectiles[player].append(projectile)

    def update(self, dt):
        for projectile in self.projectiles:
            projectile.update(dt)  # player position doesn't matter here

        # check for collisions
        for player in self.players.values():
            if not player:
                continue
            self.solve_collisions(player)

    def tick(self):
        dt = self.get_delta_time()
        self.clock.tick(s.FPS)
        self.update(dt)

    def get_delta_time(self):
        dt = perf_counter() - self.last_time
        dt *= s.DELTA_FPS  # wanted fps
        self.last_time = perf_counter()
        return dt

    def solve_collisions(self, player):
        # collisions based on circle hitboxes
        for projectile in self.projectiles:
            assert isinstance(player.position, pg.Vector2)
            if player.position.distance_to(projectile.position) < s.PLAYER_SIZE[0] / 2 + s.PROJECTILE_SIZE[0] / 2:
                player.hp -= projectile.damage
                self.projectiles.remove(projectile)
                # :TODO send the player the information about the hit to delete the projectile
                if player.hp <= 0:
                    self.player_death(player)

    def player_death(self, player):
        pass

    def box_current_state(self, player_id: uuid.UUID):
        new_box = b.Box()
        new_box.client_entity = None

        for projectile in self.to_send_projectiles[player_id]:
            new_box.add_entity(projectile)
        self.to_send_projectiles[player_id] = []

        for player in self.players.values():
            if player and player.id != player_id:
                new_box.add_entity(player)
        return new_box


# server loop
def server_loop(s_world: ServerWorld):
    pg.init()
    while True:
        print(world.players)
        s_world.tick()


# player connection function
def threaded_client(conn, player_id: uuid.UUID, local_world: ServerWorld) -> None:
    local_world.add_player(player_id)  # initialize the player in storage

    # generating the initial position of the player
    new_position = [random.randint(0, 400), random.randint(0, 400)]

    # sending the initial player position to the client
    conn.send(str.encode(','.join(map(str, new_position))))

    while True:
        try:
            data = conn.recv(4096)
            print('loading data')

            if not data:
                print('disconnected')
                break
            else:
                box: b.Box = pickle.loads(data)
                world.update_by_client(box, player_id)
                # TODO: store the player position
                # TODO: prepare the data to send to the client

                new_box = local_world.box_current_state(player_id)  # box for client

            # sending the box to the client
            conn.sendall(pickle.dumps(new_box))
        except:
            break
    print('lost connection')
    conn.close()

world = ServerWorld()
server_loop_running = False
while True:
    conn, addr = server_socket.accept()
    print('connected to:', addr)

    if not server_loop_running:
        _thread.start_new_thread(server_loop, (world,))
        server_loop_running = True

    new_player_id = uuid.uuid4()
    print('player_id:', new_player_id)

    # adding the player position to stored positions
    _thread.start_new_thread(threaded_client, (conn, new_player_id, world))
