import time
import multiprocessing
import math
from multiprocessing import Pool, cpu_count
from pierwszePlus import licz

L_RANGE = 1000000
R_RANGE = 5000000
PROCESY = 8

def czy_pierwsza_podstawowa(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def generuj_male_pierwsze(limit):
    return [i for i in range(2, limit + 1) if czy_pierwsza_podstawowa(i)]

def czy_germain(n,male_pierwsze):
    limit_n = math.sqrt(n)
    for p in male_pierwsze:
        if p > limit_n: break
        if n%p == 0: return False
    m = 2*n + 1
    limit_m = math.sqrt(m)
    for p in male_pierwsze:
        if p > limit_m: break
        if m%p == 0: return False
    return True


def worker(args):
    start, end, male_pierwsze = args
    wynik = []
    for i in range(start, end):
        if (czy_germain(i,male_pierwsze)):
            wynik.append(i)
    return wynik

def oblicz_sekwencyjnie(l,r,male_pierwsze):
    print("Start sekwencyjny")
    t_start = time.time()
    wynik = []
    for i in range(l,r+1):
        if czy_germain(i, male_pierwsze):
            wynik.append(i)
    czas = time.time() - t_start
    print(f"Koniec sekwencyjny. Czas: {czas:.4f}s. Znaleziono: {len(wynik)}")

def oblicz_rownolegle(l,r,male_pierwsze):
    print(f"Start równoległy ({PROCESY} procesy)...")
    t_start = time.time()
    zakres = r - l + 1
    krok = zakres // PROCESY
    zadania = []
    
    for i in range(PROCESY):
        poczatek = l + i * krok
        koniec = l + (i + 1) * krok if i != PROCESY - 1 else r + 1
        zadania.append((poczatek, koniec, male_pierwsze))

    with Pool(processes=PROCESY) as p:
        wyniki_czesciowe = p.map(worker, zadania)

    wynik_koncowy = [liczba for lista in wyniki_czesciowe for liczba in lista]
    
    czas = time.time() - t_start
    print(f"Koniec równoległy.  Czas: {czas:.4f}s. Znaleziono: {len(wynik_koncowy)}")


if __name__ == '__main__':
    # 1. Przygotowanie danych (sito)
    # Potrzebujemy dzielników do sqrt(2*R + 1) żeby sprawdzić liczbę Germain
    limit_sita = int(math.sqrt(2 * R_RANGE + 1)) + 1
    male_pierwsze = generuj_male_pierwsze(limit_sita)
    print(f"Wygenerowano {len(male_pierwsze)} dzielników pomocniczych.")
    print("-" * 30)

    # 2. Uruchomienie porównania
    oblicz_sekwencyjnie(L_RANGE, R_RANGE, male_pierwsze)
    print("-" * 30)
    oblicz_rownolegle(L_RANGE, R_RANGE, male_pierwsze)