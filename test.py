from datetime import datetime

from opcua import Client
from opcua import ua
from opcua.ua import DataValue

from subhandler import SubHandler


def init_nodes(root, node_dict):
    for child0 in root.get_children():
        if child0.get_browse_name().Name == 'Objects':
            for child1 in child0.get_children():
                if child1.get_browse_name().Name == 'XML DA Server - eats11':
                    for child2 in child1.get_children():
                        if child2.get_browse_name().Name == 'Schneider':
                            for child3 in child2.get_children():
                                node_dict[child3.get_browse_name().Name] = child3
    return node_dict


def subscribe_to_node(client, variable, interval_in_ms):
    # subscribe to a variable node
    handler = SubHandler()
    sub = client.create_subscription(interval_in_ms, handler)
    sub.subscribe_data_change(variable)
    return handler


if __name__ == "__main__":
    node_dict = dict()
    client = Client("opc.tcp://141.30.154.211:4850")
    client.connect()
    client.load_type_definitions()
    root = client.get_root_node()

    """    
    node_dict = init_nodes(root, node_dict)
    print(node_dict['Schneider/Fuellstand1_Ist'].get_value())
    hand = subscribe_to_node(client, node_dict['Schneider/Fuellstand2_Ist'], 100)

    print(node_dict['Schneider/Start_Umpumpen_FL'].get_value())
    node_dict['Schneider/Start_Umpumpen_FL'].set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

    while True:
        if hand.hasChanged():
            print(hand.getVar())
    """




