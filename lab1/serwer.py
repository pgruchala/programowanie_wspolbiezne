import os
import time

f = lambda x : (x+x)*x


while True:
    with open('dane.txt', 'r') as f_dane:
        dane = f_dane.read().strip()
    if dane == '':
        time.sleep(0.1)
        continue
    try:
        wynik = str(f(int(dane)))
    except Exception as e:
        wynik = f"Błąd: {e}"
    with open('wyniki.txt', 'w') as res_f:
        res_f.write(wynik)
    with open('dane.txt', 'w') as f_dane:
        f_dane.write('') 
    time.sleep(0.1)