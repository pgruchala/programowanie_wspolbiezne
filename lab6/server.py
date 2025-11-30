import sysv_ipc
import os, sys, time
from keys import *

print("===Serwer gry w trzy kości===")

try:
    pw1 = sysv_ipc.SharedMemory(PW1, sysv_ipc.IPC_CREX,0o700,size=128)
    pw2 = sysv_ipc.SharedMemory(PW2, sysv_ipc.IPC_CREX,0o700,size=128)

    sem0 = sysv_ipc.Semaphore(SETUP, sysv_ipc.IPC_CREX, 0o700,1) # zapis user1

    sem1 = sysv_ipc.Semaphore(ROUND1, sysv_ipc.IPC_CREX, 0o700,0) # zapis user2
    sem2 = sysv_ipc.Semaphore(ROUND2, sysv_ipc.IPC_CREX, 0o700,0) # odczyt user1
    sem3 = sysv_ipc.Semaphore(ROUND3, sysv_ipc.IPC_CREX, 0o700,0) # odczyft user2

    print("Zasoby utworzone")

    input("Wciśnij ENTER aby zakończyć grę")

    print("Usuwanie zasobów")
    pw1.remove()
    pw2.remove()
    sem0.remove()
    sem1.remove()
    sem3.remove()
    sem2.remove()

except sysv_ipc.ExistentialError:
    print("Błąd: zasoby już istnieją")
    sys.exit(1)
except Exception as e:
    print("Wystąpił błąd:"+e)
    sys.exit(1)