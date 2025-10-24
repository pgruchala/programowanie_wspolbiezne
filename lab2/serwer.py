import os, time

BUFFER_FILE="buffer.txt"
LOCK_FILE="lockfile.lock"
END_MARKER=":EOF:"

def cleanup():
    if os.path.exists(BUFFER_FILE):
        os.remove(BUFFER_FILE)
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def process_client_request():
    print("odebrano zapytanie od klienta")
    try:
        with open(BUFFER_FILE,'r') as f:
            lines = f.readlines()
        client_reply = lines[0].strip()

        message_lines = []
        for line in lines[1:]:
            if line.strip() == END_MARKER:
                break
            message_lines.append(line.strip())
        message = "\n".join(message_lines)
        print(f"otrzymano od klienta: {client_reply}")
        print(f"wiadomość od klienta:\n{message}")

        server_response = input("podaj odpowiedź serwera: ")
        with open(BUFFER_FILE,'w') as f:
            f.write(server_response + "\n")
            f.write(END_MARKER + "\n")
        print("wysłano odpowiedź do klienta")
    except FileNotFoundError:
        print("Plik bufora nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania zapytania: {e}")
    finally:
        cleanup()

    
def main():
    cleanup()
    print("Serwer uruchomiony. Oczekiwanie na zapytania klientów...")
    while True:
        if os.path.exists(LOCK_FILE):
            process_client_request()
        time.sleep(1)

if __name__ == "__main__":
    main()