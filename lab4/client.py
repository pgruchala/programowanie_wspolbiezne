import os, sys, time, struct, errno

SERVER_FIFO = '/tmp/server_fifo_db'
def main():
    if len(sys.argv) != 2:
        print(f"Użycie: {sys.argv[0]} <ID>", file=sys.stderr)
        sys.exit(1)

    try:
        client_id = int(sys.argv[1])
    except ValueError:
        print(f"Błąd: ID musi być liczbą całkowitą.", file=sys.stderr)
        sys.exit(1)

    CLIENT_FIFO = f'/tmp/client_fifo_{os.getpid()}'
    
    try:
        os.mkfifo(CLIENT_FIFO, 0o666)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            print(f"Klient: Błąd tworzenia kolejki {CLIENT_FIFO}: {oe}", file=sys.stderr)
            sys.exit(1)
        
    print(f"Klient: Utworzono kolejkę odpowiedzi: {CLIENT_FIFO}")

    try:
        #[długość_reszty][ID][ścieżka_klienta]
        path_bytes = CLIENT_FIFO.encode('utf-8')
        id_bytes = struct.pack('i', client_id)
        
        length_of_rest = len(id_bytes) + len(path_bytes)
        len_bytes = struct.pack('i', length_of_rest)
        
        message = len_bytes + id_bytes + path_bytes

        print(f"Klient: Wysyłanie zapytania o ID {client_id} do serwera...")
        try:
            fifo_out = os.open(SERVER_FIFO, os.O_WRONLY)
            os.write(fifo_out, message)
        except FileNotFoundError:
            print(f"Klient: Błąd - nie można znaleźć kolejki serwera {SERVER_FIFO}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Klient: Błąd zapisu do kolejki serwera: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if 'fifo_out' in locals():
                os.close(fifo_out)

        print("Klient: Oczekiwanie na odpowiedź serwera...")
        fifo_in = None
        try:
            fifo_in = os.open(CLIENT_FIFO, os.O_RDONLY)
            
            # [długość][dane]
            len_bytes_resp = os.read(fifo_in, 4)
            if not len_bytes_resp or len(len_bytes_resp) < 4:
                print("Klient: Otrzymano niekompletną odpowiedź z serwera.", file=sys.stderr)
                sys.exit(1)

            length_of_resp = struct.unpack('i', len_bytes_resp)[0]
            response_bytes = os.read(fifo_in, length_of_resp)
            
            response_str = response_bytes.decode('utf-8')
            
            print("\n------------------------------------")
            print(f"Klient: Otrzymano odpowiedź dla ID {client_id}: {response_str}")
            print("------------------------------------")

        except Exception as e:
            print(f"Klient: Błąd odczytu odpowiedzi: {e}", file=sys.stderr)
        finally:
            if fifo_in is not None:
                os.close(fifo_in)

    finally:
        try:
            os.unlink(CLIENT_FIFO)
            print(f"Klient: Usunięto kolejkę {CLIENT_FIFO}")
        except OSError as e:
            print(f"Klient: Błąd usuwania kolejki {CLIENT_FIFO}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()