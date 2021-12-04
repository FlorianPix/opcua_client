import time

import opcua
from opcua import Client, ua
from opcua.ua.uaerrors import UaStatusCodeError

from myclient import MyClient


def main():
    client = MyClient()
    if client.ready:
        for i in range(0, 10):
            if client.sub_fuell1_ist.hasChanged() or client.sub_fuell2_ist.hasChanged() or client.sub_fuell3_ist.hasChanged():
                print(client.sub_fuell1_ist.getVar(), client.sub_fuell2_ist.getVar(), client.sub_fuell3_ist.getVar())
            time.sleep(1)
    client.client.disconnect()


if __name__ == "__main__":
    main()

