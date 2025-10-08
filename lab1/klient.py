import os
import time

def main():
    print("===klient===")
    x = input("Podaj liczbę: ")
    with open('wyniki.txt', 'w') as f:
        f.write('')
    with open('dane.txt', 'w') as f:
        f.write(x)
    while True:
        with open('wyniki.txt', 'r') as f:
            result = f.read().strip()
        if result == '':
            time.sleep(0.1)
            continue
        else:
            print('wynik:', result)
            break

if __name__ == "__main__":
    main()
