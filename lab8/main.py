import threading, random, time

N = 20
SIZE = 1000000
NUM_THREADS=4096 # bazowo

L = [random.randint(0,N-1) for _ in range(SIZE)]

global_count = [0]*N
lock = threading.Lock()

def worker_count(start_index,end_index):
    local_count = [0]*N

    for i in range(start_index,end_index):
        val = L[i]
        local_count[val]+=1

    with lock:
        for i in range(N):
            global_count[i]+=local_count[i]

def multithread():
    global global_count
    global_count=[0]*N
    threads = []
    chunk_size = SIZE//NUM_THREADS
    print(f"uruchamianie {NUM_THREADS} wątków")
    start_time = time.time()

    for i in range(NUM_THREADS):
        start_idx= i*chunk_size
        end_idx = SIZE if i==NUM_THREADS-1 else (i+1)*chunk_size

        t = threading.Thread(target=worker_count,args=(start_idx,end_idx))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"zakończono liczenie. Czas: {end_time-start_time:.4f}s")
    return global_count


if __name__=="__main__":
    wynik = multithread()
    print("rezultat:\n")
    for i in range(N):
        print(f"Liczba {i}: {wynik[i]}")