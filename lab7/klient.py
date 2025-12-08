import socket 
import struct
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5001
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
BUF_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_score = 0
opp_score = 0

print("Dostępne ruchy: p (papier), k (kamień), n (nożyce)")
print("Wyjście z gry: wpisz 'koniec'")
print("-" * 40)


def check_round_result(my_move, opp_move):
    if my_move == opp_move:
        return 0 
    if (my_move == 'p' and opp_move == 'k') or \
       (my_move == 'k' and opp_move == 'n') or \
       (my_move == 'n' and opp_move == 'p'):
        return 1
    return -1 
while True:
    try:
        wybor = input("Twój wybór (p/k/n/koniec): ").strip().lower()

        if wybor not in ['p', 'k', 'n', 'koniec']:
            print("Niepoprawny wybór! Użyj: p, k, n lub koniec.")
            continue

        client_socket.sendto(wybor.encode('utf-8'), SERVER_ADDR)

        if wybor == "koniec":
            print("Wysłano sygnał końca. Zamykanie klienta...")
            break
        
        print("Czekam na ruch przeciwnika...")

        resp_bytes, _ = client_socket.recvfrom(BUF_SIZE)
        resp = resp_bytes.decode('utf-8')

        if resp == "===KONIEC===":
            print("\n--- Drugi gracz zakończył grę. KONIEC ROZGRYWKI ---")
            break
        
        opp_move = resp
        wynik = check_round_result(wybor, opp_move)

        if wynik == 1:
            my_score += 1
            status = "WYGRANA"
        elif wynik == -1:
            opp_score += 1
            status = "PRZEGRANA"
        else:
            status = "REMIS"

        print(f"\nTy: {wybor.upper()} | Przeciwnik: {opp_move.upper()} -> {status}")
        print(f"Stan punktów -> Ty: {my_score} | Przeciwnik: {opp_score}")
        print("-" * 40)

    except KeyboardInterrupt:
        client_socket.sendto("koniec".encode('utf-8'), SERVER_ADDR)
        print("\nPrzerwano.")
        break
    except Exception as e:
        print(f"Błąd: {e}")
        break

client_socket.close()