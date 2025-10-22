import minimalmodbus
import math
import time


class RelayControl:
    def __init__(self, relay_instrument):
        self.relay = relay_instrument


    def uniform_distribute(self,m,n):
        if n==0:
            return []
        if n==1:
            return [(m+1)//2]

        if n>=m:
            return list(range(1,m+1))

        real = [(1+i*(m-1)/(n-1)) for i in range (0,n)]
        pos = [int(round(x)) for x in real]
        return pos


    def close_all_relay(self):
        address = 0x00FF
        self.relay.write_bit(registeraddress=address, value=0x0000, functioncode=5)


    def open_certain_relay(self, m, n):
        pos = self.uniform_distribute(m,n)
        for ch in pos:
            address = 0x0100 + (ch - 1)
            self.relay.write_bit(registeraddress=address, value=1, functioncode=5)
            time.sleep(0.2)



if __name__ == "__main__":
    m = int(input("Number of total LED:"))
    n = int(input("Number of turned-on LED:"))
    test = uniform_distribute(m,n)
    print(test)
