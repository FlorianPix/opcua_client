import time

from myclient import MyClient


def main():
    client = MyClient()
    try:
        if client.connected:
            for i in range(0, 10):
                if client.sub_fuell1_ist.hasChanged() or client.sub_fuell2_ist.hasChanged() or client.sub_fuell3_ist.hasChanged():
                    print(client.sub_fuell1_ist.getVar(), client.sub_fuell2_ist.getVar(), client.sub_fuell3_ist.getVar())
                time.sleep(1)
    except BaseException as err:
        print(err)
    finally:
        client.client.disconnect()


if __name__ == "__main__":
    main()

