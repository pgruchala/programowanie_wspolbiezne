import os
import signal
import struct
import time
import sys
import errno

SERVER_FIFO = "/tmp/server_fifo_db"

BAZA_DANYCH = {
    1: "Kowalski",
    2: "Nowak",
    3: "Wiśniewski",
    4: "Zieliński"
}


running = True


def handle_sigusr1(signum, frame):
    global running
    print("\nSerwer: Otrzymano SIGUSR1. Kończenie pracy...")
    running = False

def setup_signals():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    
    signal.signal(signal.SIGUSR1, handle_sigusr1)
    print(f"Serwer: PID = {os.getpid()}. Obsługa sygnałów ustawiona.")

def create_fifo(path):
    try:
        os.mkfifo(path, 0o666)
        print(f"Serwer: Utworzono kolejkę FIFO: {path}")
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            print(f"Serwer: Błąd tworzenia FIFO: {oe}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Serwer: Kolejka FIFO {path} już istnieje.")

def run_server():
    global running
    
    setup_signals()
    create_fifo(SERVER_FIFO)
    
    fifo_in = None
    fifo_out_self = None
    
    try:
        print("Serwer: Otwieranie kolejki do odczytu...")
        fifo_in = os.open(SERVER_FIFO, os.O_RDONLY)
        
        fifo_out_self = os.open(SERVER_FIFO, os.O_WRONLY)
        print("Serwer: Gotowy na przyjmowanie zapytań.")
        
        while running:
            try:
                len_bytes = os.read(fifo_in, 4)
            except InterruptedError:
                continue
                
            if not len_bytes and running:
                print("Serwer: pusta kolejka, sprawdzam status...")
                time.sleep(0.1)
                continue
            
            if not len_bytes:
                break 

            if len(len_bytes) < 4:
                print(f"Serwer: Otrzymano niekompletny nagłówek ({len(len_bytes)} bajtów). Ignorowanie.")
                continue

            length_of_rest = struct.unpack('i', len_bytes)[0]
            
            rest_bytes = os.read(fifo_in, length_of_rest)
            if len(rest_bytes) != length_of_rest:
                print("Serwer: Błąd odczytu - niekompletne dane. Ignorowanie.", file=sys.stderr)
                continue

            try:
                client_id = struct.unpack('i', rest_bytes[:4])[0]
                client_fifo_path = rest_bytes[4:].decode('utf-8')
                print(f"Serwer: Otrzymano zapytanie o ID {client_id} od {client_fifo_path}")
            except Exception as e:
                print(f"Serwer: Błąd rozpakowywania danych: {e}", file=sys.stderr)
                continue

            print("Serwer: Przetwarzanie zapytania (5s)...")
            time.sleep(5)
            
            response_str = BAZA_DANYCH.get(client_id, "Nie ma")
            response_bytes = response_str.encode('utf-8')
            
            # [długość][odpowiedź]
            len_bytes_resp = struct.pack('i', len(response_bytes))
            message = len_bytes_resp + response_bytes
            
            try:
                fifo_out_client = os.open(client_fifo_path, os.O_WRONLY)
                os.write(fifo_out_client, message)
            except Exception as e:
                print(f"Serwer: Błąd wysyłania odpowiedzi do {client_fifo_path}: {e}", file=sys.stderr)
            finally:
                if 'fifo_out_client' in locals() and fifo_out_client:
                    os.close(fifo_out_client)
                    
            print(f"Serwer: Wysłano odpowiedź '{response_str}' do {client_fifo_path}")

    except Exception as e:
        if running:
            print(f"Serwer: Wystąpił nieoczekiwany błąd: {e}", file=sys.stderr)
            
    finally:
        print("\nSerwer: Rozpoczynanie sprzątania...")
        if fifo_in is not None:
            os.close(fifo_in)
        if fifo_out_self is not None:
            os.close(fifo_out_self)
            
        try:
            os.unlink(SERVER_FIFO)
            print(f"Serwer: Usunięto kolejkę {SERVER_FIFO}")
        except OSError as e:
            print(f"Serwer: Błąd usuwania kolejki {SERVER_FIFO}: {e}", file=sys.stderr)
            
        print("Serwer: Zakończono działanie.")

if __name__ == "__main__":
    run_server()