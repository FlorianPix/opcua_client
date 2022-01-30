from opcua import Client
from opcua import ua
from opcua.ua import DataValue

from subhandler import SubHandler


class MyClient:
    def __init__(self):
        self.server_address = "opc.tcp://localhost:4840/freeopcua/server/"
        self.uri = "http://tu-dresden.de/iat-opc/"
        # self.server_address = "opc.tcp://141.30.154.211:4850"
        # self.uri = "http://141.30.154.212:8087/OPC/DA"
        self.default_interval = 100
        self.connected = False

        try:
            self.client = Client(self.server_address)
            self.client.connect()
            self.client.load_type_definitions()
            self.root = self.client.get_root_node()
            self.objects = self.client.get_objects_node()
            self.idx = self.client.get_namespace_index(self.uri)

            self.node_dict = dict()
            self.init_node_dict()

            # füllstände
            self.sub_fuell1_ist = self.subscribe_to_node(self.node_dict['Schneider/Fuellstand1_Ist'], self.default_interval)
            self.sub_fuell2_ist = self.subscribe_to_node(self.node_dict['Schneider/Fuellstand2_Ist'], self.default_interval)
            self.sub_fuell3_ist = self.subscribe_to_node(self.node_dict['Schneider/Fuellstand3_Ist'], self.default_interval)
            self.sub_fuells = [self.sub_fuell1_ist, self.sub_fuell2_ist, self.sub_fuell3_ist]

            """
            # durchfluss
            self.sub_durchfluss1_ist = self.subscribe_to_node(self.node_dict['Schneider/Durchfluss1_Ist'], self.default_interval)
            self.sub_durchfluss2_ist = self.subscribe_to_node(self.node_dict['Schneider/Durchfluss2_Ist'], self.default_interval)

            # dosieren
            self.sub_volumen_1 = self.subscribe_to_node(self.node_dict['Schneider/Volumen1'], self.default_interval)
            self.sub_volumen_2 = self.subscribe_to_node(self.node_dict['Schneider/Volumen2'], self.default_interval)
            """

            print("connected with Server")
            self.connected = True

        except BaseException as err:
            print('Failed to connect to server!')
            raise Exception(err)

    def init_node_dict(self):
        # fill node dict with available nodes
        for child0 in self.root.get_children():
            if child0.get_browse_name().Name == 'Objects':
                for child1 in child0.get_children():
                    if child1.get_browse_name().Name == 'XML DA Server - eats11':
                        for child2 in child1.get_children():
                            if child2.get_browse_name().Name == 'Schneider':
                                for child3 in child2.get_children():
                                    self.node_dict[child3.get_browse_name().Name] = child3

    def subscribe_to_node(self, variable, interval_in_ms):
        # subscribe to a variable node
        handler = SubHandler()
        sub = self.client.create_subscription(interval_in_ms, handler)
        sub.subscribe_data_change(variable)
        return handler

    def set(self, node_name, value):
        self.node_dict[node_name].set_attribute(ua.AttributeIds.Value, ua.DataValue(value))
