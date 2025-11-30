import sysv_ipc
import os, sys, time
from keys import *

NULL_CHAR='\0'

def pisz(mem,s):
    s+=NULL_CHAR
    s=s.encode()
    mem.write(s)

def czytaj(mem):
    try:
        s = mem.read()
        s = s.decode().strip(NULL_CHAR)
        if NULL_CHAR in s:
            s = s[:s.find(NULL_CHAR)]
        return s
    except:
        return ''
    
def pobierz_wybor(nr_gracza):
    while True:
        x  = input(f"gracz:{nr_gracza}\nPodaj wybór:")
        if x in ['1','2','3']:
            return x
        print('niepoprawna wartość')


try:
    pw1 = sysv_ipc.SharedMemory(PW1)
    pw2 = sysv_ipc.SharedMemory(PW2)
    sem1 = sysv_ipc.Semaphore(SETUP)
    sem2 = sysv_ipc.Semaphore(ROUND1)
    sem3 = sysv_ipc.Semaphore(ROUND2)
    sem4 = sysv_ipc.Semaphore(ROUND3)
    print("połączono z serwerem")
except sysv_ipc.ExistentialError:
    print("Nie znaleziono zasobów")
    sys.exit(1)
moj_nr = 0

try:
    sem1.acquire(0)
    
    moj_nr = 1
    print("Udało się zająć semafor SETUP. Jestem GRACZEM 1")

except sysv_ipc.BusyError:
    moj_nr = 2
    print("Semafor SETUP zajęty. Jestem GRACZEM 2")


LICZBA_TUR = 3
wynik_ja = 0
wynik_przeciwnik=0

print(f"Rozpoczynam grę jako klient numer {moj_nr}")

for tura in range(1, LICZBA_TUR + 1):
    print(f"\n--- TURA {tura} ---")
    
    moj_wybor = ""
    wybor_rywala = ""

    if moj_nr == 1:
        print("Oczekiwanie na dostęp do zapisu...")
        if tura > 1:
            sem1.acquire()
        
    
        moj_wybor = pobierz_wybor(1)
        pisz(pw1, moj_wybor)
        
        sem2.release()
        
        print("Czekam na ruch Gracza 2...")
        
        sem3.acquire()
        wybor_rywala = czytaj(pw2)
        print(f"Gracz 2 wybrał: {wybor_rywala}")
        
        sem4.release()

    else:
        # GRACZ 2
        print("Czekam na ruch Gracza 1...")
        
        # 1. Czekaj aż Gracz 1 zapisze
        sem2.acquire()
        
        # 2. Wybierz i zapisz 
        moj_wybor = pobierz_wybor(2)
        pisz(pw2, moj_wybor)
        
        # 3. Pozwól Graczowi 1 odczytać twój wynik
        sem3.release()
        
        sem4.acquire()
        wybor_rywala = czytaj(pw1)
        print(f"Gracz 1 wybrał: {wybor_rywala}")
        
        sem1.release()

    # --- WYLICZANIE WYNIKU ---
    val_p1 = moj_wybor if moj_nr == 1 else wybor_rywala
    val_p2 = wybor_rywala if moj_nr == 1 else moj_wybor
    
    if val_p1 == val_p2:
        wygrywa = "Gracz 2"
        if moj_nr == 2: wynik_ja += 1
        else: wynik_przeciwnik += 1
    else:
        wygrywa = "Gracz 1"
        if moj_nr == 1: wynik_ja += 1
        else: wynik_przeciwnik += 1
    
    print(f"W tej turze wygrywa: {wygrywa}")
    print(f"Stan meczu: Ty {wynik_ja} - {wynik_przeciwnik} Rywal")

print("\n--- KONIEC GRY ---")
if wynik_ja > wynik_przeciwnik: print("WYGRAŁEŚ!")
elif wynik_ja < wynik_przeciwnik: print("PRZEGRAŁEŚ!")
else: print("REMIS!")