import pickle, time
from client import Client
from dbclient import DBClient
from constRPC import *

def main():
    c1   = Client(PORTC1)
    dbC1 = DBClient(HOSTS, PORTS)
    dbC1.create()
    dbC1.appendData('Client 1')
    time.sleep(1)
    c1.sendTo(HOSTC2, PORTC2, pickle.dumps(dbC1))
    print(f"[Client1] sent stub to client2 at {HOSTC2}:{PORTC2}")

if __name__ == "__main__":
    main()
