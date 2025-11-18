import sysv_ipc, os
from keys import IN_KEY

def stop():
    print("Wysyłanie sygnału zatrzymania")
    try:
        mq_in = sysv_ipc.MessageQueue(IN_KEY)
        mq_in.send("stop".encode(),type=os.getpid())
        print("wysłano")
    except sysv_ipc.ExistentialError:
        print("Wystąpił problem z kolejką")

stop()