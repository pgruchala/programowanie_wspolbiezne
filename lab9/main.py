import threading
import math
from pierwsze import gen_pierwsza

l = 2
r = 500

TH_NUM = 4
res = []
list_lock = threading.Lock()

def search(start,end,barrier,th_name):
    print(f"{th_name} start pracy dla zakresu {start} - {end}")
    local_primes= gen_pierwsza(start,end)

    with list_lock:
        res.extend(local_primes)

    print(f"{th_name} zakończył działanie")

    barrier.wait()

len_range = r-l+1
chunk_size = math.ceil(len_range/TH_NUM)

barrier = threading.Barrier(TH_NUM+1)

threads = []

for i in range(TH_NUM):
    start = l+i*chunk_size
    end = start+chunk_size-1

    if end > r:
        end = r
    
    t = threading.Thread(target=search, args=(start,end,barrier, f"Wątek:{i+1}"))
    threads.append(t)
    t.start()


barrier.wait()

res.sort()
print(f"znalezione liczby pierwsze: \n{res}")