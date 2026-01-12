import socket, threading, sys

HOST = '0.0.0.0'
PORT = 5000
SIZE = 8


class ReversiServer:
    def __init__(self):
        self.board = [[0]*SIZE for _ in range(SIZE)]
        self.clients=[]
        self.turn = 1
        self.game_over = False
        self.lock = threading.Lock()
        self.init_board()

    def init_board(self):
        c = SIZE//2
        self.board[c-1][c-1] = 2
        self.board[c][c] = 2
        self.board[c-1][c] = 1
        self.board[c][c-1] = 1

    def board_to_string(self):
        return "".join("".join(map(str,row)) for row in self.board)
    
    def is_on_board(self, x, y):
        return 0 <= x < SIZE and 0 <= y < SIZE
    
    def get_valid_moves(self, player):
        moves = []
        for y in range(SIZE):
            for x in range(SIZE):
                if self.check_move(player, x, y, execute=False):
                    moves.append((x, y))
        return moves

    def check_move(self, player, x, y, execute=False):
        if self.board[y][x] != 0:
            return False
        
        opponent = 2 if player == 1 else 1
        to_flip = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            temp_flip = []
            while self.is_on_board(nx, ny) and self.board[ny][nx] == opponent:
                temp_flip.append((nx, ny))
                nx += dx
                ny += dy
            if self.is_on_board(nx, ny) and self.board[ny][nx] == player:
                to_flip.extend(temp_flip)
        
        if not to_flip:
            return False
        
        if execute:
            self.board[y][x] = player
            for fx, fy in to_flip:
                self.board[fy][fx] = player
        return True

    def count_score(self):
        b = sum(row.count(1) for row in self.board)
        w = sum(row.count(2) for row in self.board)
        return b, w

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall((message + "\n").encode())
            except:
                pass

    def handle_turn_cycle(self):
        p1_moves = self.get_valid_moves(1)
        p2_moves = self.get_valid_moves(2)

        if not p1_moves and not p2_moves:
            self.end_game()
            return

        current_moves = p1_moves if self.turn == 1 else p2_moves
        if not current_moves:
            print(f"Gracz {self.turn} nie ma ruchu. PASS.")
            self.turn = 2 if self.turn == 1 else 1
            self.broadcast(f"MSG Brak ruchu! Tura przechodzi dalej.")
            self.handle_turn_cycle()
            return

        state = self.board_to_string()
        self.broadcast(f"BOARD {state} {self.turn}")

    def end_game(self):
        self.game_over = True
        b, w = self.count_score()
        if b > w: res = "WYGRAL CZARNY"
        elif w > b: res = "WYGRAL BIALY"
        else: res = "REMIS"
        self.broadcast(f"GAMEOVER {b} {w} {res}")

    def client_thread(self, conn, player_id):
        my_color = player_id 
        while not self.game_over:
            try:
                data = conn.recv(1024).decode().strip()
                if not data: break
                
                if data.startswith("MOVE"):
                    with self.lock:
                        if self.turn != my_color:
                            conn.sendall("MSG To nie twoja tura!\n".encode())
                            continue
                        
                        _, x, y = data.split()
                        x, y = int(x), int(y)
                        
                        if self.check_move(my_color, x, y, execute=True):
                            self.turn = 2 if self.turn == 1 else 1
                            self.handle_turn_cycle()
                        else:
                            conn.sendall("MSG Ruch niedozwolony!\n".encode())
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Błąd gracza {player_id}: {e}")
                break
        print(f"Gracz {player_id} rozłączony.")

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(2)
        print(f"Serwer Reversi działa na porcie {PORT}. Czekam na graczy...")

        try:
            while len(self.clients) < 2:
                conn, addr = s.accept()
                self.clients.append(conn)
                pid = len(self.clients)
                print(f"Połączono gracza {pid}: {addr}")
                conn.sendall(f"WELCOME {pid}\n".encode())

            print("Start gry!")
            self.handle_turn_cycle()

            t1 = threading.Thread(target=self.client_thread, args=(self.clients[0], 1))
            t2 = threading.Thread(target=self.client_thread, args=(self.clients[1], 2))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except KeyboardInterrupt:
            print("\nZamykanie serwera.")
        finally:
            s.close()

if __name__ == "__main__":
    ReversiServer().start()