from opcua import Client
from opcua import ua


def main():
    with Client("opc.tcp://141.30.154.211:4850") as client:
        client.connect()
        client.load_type_definitions()
        root = client.get_root_node()
        objects = client.get_objects_node()
        idx = client.get_namespace_index("http://141.30.154.212:8087/OPC/DA")
        for child in root.get_children():
            if child.nodeid.Identifier == 85:
                for chil in child.get_children():
                    if chil.nodeid.Identifier == 'XML DA Server - eats11Root':
                        for chi in chil.get_children():
                            if chi.nodeid.Identifier == 'F:Schneider':
                                for ch in chi.get_children():
                                    try:
                                        print(ch.nodeid.Identifier, ch.get_value())
                                    except:
                                        pass


if __name__ == "__main__":
    main()
