import pickle
from client import Client
from constRPC import *

def main():
    c2   = Client(PORTC2)
    print(f"[Client2] waiting for stub on port {PORTC2}...")
    data = c2.recvAny()
    dbC2 = pickle.loads(data)
    dbC2.appendData('Client 2')
    result = dbC2.getValue()
    print(f"[Client2] final list: {result}")
    c2.sendTo(HOSTS, PORTS, [STOP])

if __name__ == "__main__":
    main()
