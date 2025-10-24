import os, sys, time, errno
from klient import cleanup

BUFFER_FILE="buffer.txt"
LOCK_FILE="lockfile.lock"
END_MARKER=":EOF:"

def acquire_lock():
    fd = None
    while True:
        try:
            fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            time.sleep(1)
    return fd

def getUserInput():
    print("Wpisz swoją wiadomość. Zakończ pustą linią (wciskając Enter).")
    message_lines = []
    while True:
        line = input()
        if not line:
            break
        message_lines.append(line)
    return message_lines


def main():
    pid = os.getpid()
    reply_file = f"odpowiedz_dla_{pid}.txt"

    message = getUserInput()

    lock_fd = acquire_lock()

    try:
        print("Wysyłanie wiadomości do serwera...")
        with open(BUFFER_FILE, 'w') as f:
            f.write(reply_file + '\n')
            f.write('\n'.join(message) + '\n')
            f.write(END_MARKER + '\n')
        
        os.close(lock_fd)
        
        print("Wiadomość wysłana. Oczekiwanie na odpowiedź serwera...")
    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania: {e}")
        os.close(lock_fd)
        os.unlink(LOCK_FILE)
        sys.exit(1)

    while not os.path.exists(reply_file):
        time.sleep(0.5)

    reply_content = ""
    
    while END_MARKER not in reply_content:
        time.sleep(0.5)
        with open(reply_file, 'r') as f:
            reply_content = f.read()

    print("\n" + "="*30)
    print("Otrzymano odpowiedź od serwera:")
    print(reply_content.replace(END_MARKER, "").strip())
    print("="*30)

    os.remove(reply_file)
    print("Zakończono komunikację.")