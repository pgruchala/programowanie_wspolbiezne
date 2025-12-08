import socket 

IP = "127.0.0.1"
PORT = 5001
BUF_SIZE=1024

server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind((IP,PORT))

print(f"serwer działa: {IP}:{PORT}")


ruchy ={}
wyniki={}

def reset_game():
    global ruchy ,wyniki
    wyniki={}
    ruchy={}

def sprawdz_wygrana(ruch1,ruch2):
    if ruch1==ruch2:
        return 0
    if (ruch1=='p' and ruch2=='k') or (ruch1=='k' and ruch2=='n') or (ruch1 == 'n' and ruch2 == 'p'):
        return 1
    return 2


while True:
    try:
        message_bytes,address = server_socket.recvfrom(BUF_SIZE)
        message = message_bytes.decode('utf-8').strip().lower()

        if address not in ruchy:
            if len(ruchy)<2:
                ruchy[address]=None
                wyniki[address]=0
                print(f"Dołączył nowy gracz {address}")
            else:
                continue
        print(f"Otrzymano ruch: \n{message} od {address}")
        ruchy[address] = message

        gracze = list(ruchy.keys())

        if len(gracze) == 2 and ruchy[gracze[0]] is not None and ruchy[gracze[1]] is not None:
            m1 = ruchy[gracze[0]]
            m2 = ruchy[gracze[1]]

            if m1 == 'koniec' or m2 =='koniec':
                print("otrzymano znak końca gry")
                msg_end = "===KONIEC===".encode('utf-8')
                server_socket.sendto(msg_end,gracze[0])
                server_socket.sendto(msg_end,gracze[1])
                reset_game()
                continue
            wynik = sprawdz_wygrana(m1,m2)

            if wynik == 1:
                wyniki[gracze[0]]+=1
            elif wynik ==2:
                wyniki[gracze[1]] +=1

            print(f"Wynik rundy: {m1} vs {m2} -> Wygrał gracz {wynik if wynik > 0 else 'Remis'}")
            print(f"Punkty serwera: {gracze[0]}: {wyniki[gracze[0]]} | {gracze[1]}: {wyniki[gracze[1]]}")

            server_socket.sendto(m2.encode('utf-8'), gracze[0])
            server_socket.sendto(m1.encode('utf-8'), gracze[1])

            ruchy[gracze[0]] = None
            ruchy[gracze[1]] = None

    except KeyboardInterrupt:
        print("\nWyłączanie serwera...")
        break
    except Exception as e:
        print(f"Błąd: {e}")

server_socket.close()