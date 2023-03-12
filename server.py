import socket
from _thread import *
import pickle
from game import Game
from settings import *

server = SERVER_IP
port = SERVER_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
id_count = 0


def threaded_client(conn, p, gameId):
    global id_count
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data == "continue":
                        game.continues[p] = True
                    elif data == "resetContinue":
                        game.reset_continue()
                    elif data == "tie":
                        game.ties += 1
                    elif data == "win":
                        game.wins[p] += 1
                    elif data == "choosed":
                        game.choose[p] = True
                    elif data == "notchoosed":
                        game.choose[p] = False
                    elif data != "get":
                        if data[0] == 'C':
                            game.set_color(p, data[1:])
                        elif data[0] == 'M':
                            game.marks[p] = data[1]
                        else:
                            game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    id_count -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1)//2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, game_id))
