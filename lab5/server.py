import os, sys, errno, sysv_ipc, time
from keys import IN_KEY, OUT_KEY

DATABASE = {
    "Belgia":"Luksemburg",
    "Polska":"Warszawa",
    "Czechy":"Praga",
    "Estonia":"Talin",
    "Norwegia":"Oslo",
    "Szkocja":"Edynburg",
    "Niemcy":"Berlin",
}
def runServer():
    try:
        mq_in= sysv_ipc.MessageQueue(IN_KEY, sysv_ipc.IPC_CREAT)
        mq_out = sysv_ipc.MessageQueue(OUT_KEY, sysv_ipc.IPC_CREAT)
        print("utworzono pliki fifo")
    except sysv_ipc.ExistentialError:
        print("Wystąpił problem z tworzeniem kolejek IPC")
        return
    
    try:
        print("Czekam na zapytania")
        while True:
            message, m_type = mq_in.receive()
            decoded = message.decode()

            print(f"Otrzymano {decoded} od procesu: {m_type}")

            if decoded == "stop":
                print("kończę")
                break

            time.sleep(2)
            response = DATABASE.get(decoded, "Nie wiem")
            mq_out.send(response.encode(),type=m_type)
            print(f"Wysłano : {response} do {m_type}")
    except KeyboardInterrupt:
        print("Przerwano przez CTRL+C")
    finally:
        print("Usuwanie kolejek IPC")
        try:
            mq_in.remove()
            mq_out.remove()
            print("Kolejki usunięte poprawnie")
        except sysv_ipc.ExistentialError:
            print("kolejki już nie istnieją")

runServer()