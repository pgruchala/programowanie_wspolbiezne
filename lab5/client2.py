import sysv_ipc, time, os
from keys import IN_KEY, OUT_KEY



def runClient():
    pid = os.getpid()
    print(f"klient działa; PID: {pid}")
    try:
        mq_in= sysv_ipc.MessageQueue(IN_KEY)
        mq_out = sysv_ipc.MessageQueue(OUT_KEY)
        print("utworzono pliki fifo")
    except sysv_ipc.ExistentialError:
        print("Wystąpił problem otwieraniem kolejek IPC")
        return
    
    countries = ["Belgia", 'Polska', 'Czechy', "Estonia"]
    for country in countries:
        msg = country.encode()
        mq_in.send(msg, type=pid)
        print(f"Wysłano zapytanie o: {country}")
        time.sleep(1)

    print("czekam na odpowiedź")

    for _ in countries:
        message,_ = mq_out.receive(type=pid)
        response = message.decode()
        print(f"Odebrano odpowiedź {response}")
    print("klient kończy działanie")


runClient()