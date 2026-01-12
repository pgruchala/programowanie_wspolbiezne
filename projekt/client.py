import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 5000

class ReversiClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversi Client")
        self.sock = None
        self.my_id = 0 
        self.buttons = []
        self.running = True
        
        self.setup_gui()
        self.connect()

    def setup_gui(self):
        self.info_label = tk.Label(self.root, text="Łączenie...", font=("Arial", 12))
        self.info_label.pack(pady=5)
        
        frame = tk.Frame(self.root, bg="black")
        frame.pack(padx=10, pady=10)

        for y in range(8):
            row = []
            for x in range(8):
                btn = tk.Button(frame, width=4, height=2, bg="green",
                                font=("Arial", 10, "bold"),
                                command=lambda r=x, c=y: self.send_move(r, c))
                btn.grid(row=y, column=x, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można połączyć z serwerem: {e}")

    def send_move(self, x, y):
        if self.sock:
            try:
                self.sock.sendall(f"MOVE {x} {y}\n".encode())
            except:
                pass

    def update_board(self, board_str):
        for i, char in enumerate(board_str):
            y, x = divmod(i, 8)
            color = "green"
            text = ""
            fg = "black"
            
            if char == '1': # Czarny
                text = "●"
                fg = "black"
            elif char == '2': # Biały
                text = "●"
                fg = "white"
            
            self.buttons[y][x].config(text=text, fg=fg, bg=color)

    def receive_loop(self):
        buf = ""
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data: break
                buf += data
                
                while "\n" in buf:
                    msg, buf = buf.split("\n", 1)
                    self.process_msg(msg)
            except:
                break

    def process_msg(self, msg):
        parts = msg.split()
        cmd = parts[0]

        if cmd == "WELCOME":
            self.my_id = int(parts[1])
            color = "CZARNY (Zaczynasz)" if self.my_id == 1 else "BIAŁY (Drugi)"
            self.root.title(f"Reversi - Jesteś: {color}")

        elif cmd == "BOARD":
            self.update_board(parts[1])
            turn = int(parts[2])
            
            status = f"Ty: {'Czarny' if self.my_id==1 else 'Biały'} | "
            if turn == self.my_id:
                status += "TWOJA TURA"
                self.info_label.config(text=status, fg="red")
            else:
                status += "Ruch przeciwnika"
                self.info_label.config(text=status, fg="black")

        elif cmd == "MSG":
            print(f"Serwer info: {' '.join(parts[1:])}")

        elif cmd == "GAMEOVER":
            b, w = parts[1], parts[2]
            res = " ".join(parts[3:])
            txt = f"Koniec gry!\nCzarni: {b}\nBiali: {w}\nWynik: {res}"
            messagebox.showinfo("Koniec", txt)
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ReversiClient(root)
    root.mainloop()