import os, time

INSTRUCTION="\\input{"

count = 0

def reading(p,s):
    count = 0
    childs=[]
    try:
        with open(p, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                time.sleep(0.5)

                if line.startswith(INSTRUCTION):
                    newFile = line[len(INSTRUCTION):].rstrip('}').strip()
                    try:
                        pid = os.fork()
                        if pid == 0: 
                            result = reading(newFile, s)
                            os._exit(result) 
                        else:
                            childs.append(pid)
                    except OSError as e:
                        print(f"Fork failed: {e}")
                else:
                    print(line)
                    count += sum(1 for word in line.split() if word == s)

                    
        for pid in childs:
            _, status = os.waitpid(pid, 0)
            if os.WIFEXITED(status):
                count += os.WEXITSTATUS(status)
                
        return count
    except FileNotFoundError:
        print(f"Plik nie istnieje: {p}")



total = reading('plikA.txt','czterdzieści')

print(f"Liczba wystąpień słowa: {total}")