import os
HOSTS  = os.getenv("SERVER_HOST",  "localhost")
HOSTC1 = os.getenv("CLIENT1_HOST", "localhost")
HOSTC2 = os.getenv("CLIENT2_HOST", "localhost")
PORTS   = 50004
PORTC1  = 50053
PORTC2  = 50054
OK       = '1'
ADD      = '2'
APPEND   = '3'
GETVALUE = '4'
CREATE   = '5'
STOP     = '6'
