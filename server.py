import socket
import _thread
import sys
import utils as u

server = '127.0.0.1'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# linking the server to the port
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)  # number of possible connections

print('waiting for connection')

# TODO: store the data of players, projectiles and enemies
# DATA STRUCTURES HERE


# server loop
def server_loop():
    while True:
        print('server loop running')
        # TODO: update the game world
        # TODO: the time between the updates should be constant and equal to the client's FPS
        # TODO: update projectile positions and check for collisions
        pass


# player connection function
def threaded_client(conn, player_id: int) -> None:
    # TODO: initialize the player in storage
    # sending the initial player position to the client
    # conn.send(str.encode(u.pack_player_data(# TODO: player position from storage)))
    reply = ''
    while True:
        # receiving the player position from the client
        try:
            data = conn.recv(2048).decode('utf-8')
            decoded_data = u.unpack_player_data(data)

            if not data:
                print('disconnected')
                break
            else:
                # TODO: store the player position
                # TODO: prepare the data to send to the client
                # print the received data and the data to send
                print('-------------------')
                print('player_id:', player_id)
                print('received:', decoded_data)
                print('sending:', reply)

            # sending the enemy and projectile data to the client
            # conn.sendall(str.encode(u.pack_player_data(# TODO: enemy and projectile positions from storage)))
        except:
            break
    print('lost connection')
    conn.close()


current_player_id = 0
server_loop_running = False
while True:
    conn, addr = s.accept()
    print('connected to:', addr)

    if not server_loop_running:
        _thread.start_new_thread(server_loop, ())
        server_loop_running = True

    # adding the player position to stored positions
    _thread.start_new_thread(threaded_client, (conn, current_player_id))
    # changing the player id
    current_player_id += 1
