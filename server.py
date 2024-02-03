import socket
import _thread
import sys
import utils as u

server = '10.72.11.34'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print('waiting for connection')

player_positions = [(200, 200), (400, 400)]


def threaded_client(conn, player_id: int) -> None:
    conn.send(str.encode(u.pack_player_data(player_positions[player_id])))
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode('utf-8')
            decoded_data = u.unpack_player_data(data)

            if not data:
                print('disconnected')
                break
            else:
                if player_id == 1:
                    reply = player_positions[0]
                else:
                    reply = player_positions[1]

                print('player_id:', player_id)
                print('received:', decoded_data)
                print('sending:', reply)

            # sending the player position to the other player
            conn.sendall(str.encode(u.pack_player_data(reply)))
        except:
            break
    print('lost connection')
    conn.close()

current_player_id = 0
while True:
    conn, addr = s.accept()
    print('connected to:', addr)

    # adding the player position to stored positions
    _thread.start_new_thread(threaded_client, (conn, current_player_id))
    # changing the player id
    current_player_id += 1
