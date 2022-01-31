import logging
import sys
from opcua import ua, uamethod, Server

"""
Server endpoint definition
Defines how the server can be reached and stores the path for the custom Namespace xml file
"""
namespace = "Namespace/my_namespace.xml"
uri = "http://tu-dresden.de/iat-opc/"
name = "IAT OPC Server"
endpoint = "opc.tcp://localhost:4840/freeopcua/server/"

# Interactive Python import
try:
    from IPython import embed
except ImportError:
    import code
    """
    Interactive python function
    This way one can run python commands on the console when the server is set up and running
    """
    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

sys.path.insert(0, "")


class MyServer:
    """
    Server Initializer
    Sets up the server with address, namspace, uri and creates the OPC Server object.
    """
    def __init__(self):
        # optional: setup logging.
        logging.basicConfig(level=logging.WARN)

        # Creates the actual OPC server object from FreeOPCUA
        self.server = Server()
        # Address of the server
        self.server.set_endpoint(endpoint)
        # Name of the server
        self.server.set_server_name(name)
        # set all possible endpoint policies for clients to connect through
        self.server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])

        # Our namespace uri
        self.idx = self.server.register_namespace(uri)

        # get Objects node
        self.objects = self.server.get_objects_node()

        # import the actual nodes from our namespace
        self.server.import_xml(namespace)

        self.root = self.server.get_root_node()
        self.node_dict = dict()

    # Starts the server
    def start(self):
        # After that the server is online and running
        self.server.start()
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        try:
            self.objects.add_object(self.idx, "XML DA Server - eats11", ua.NodeId.from_string('ns=%d;i=1001' % self.idx))

            self.init_node_dict()

            self.node_dict['Schneider/Fuellstand1_Ist'].set_attribute(ua.AttributeIds.Value, ua.DataValue(120.0))
            self.node_dict['Schneider/Fuellstand2_Ist'].set_attribute(ua.AttributeIds.Value, ua.DataValue(130.0))
            self.node_dict['Schneider/Fuellstand3_Ist'].set_attribute(ua.AttributeIds.Value, ua.DataValue(125.0))

            self.node_dict['Schneider/Behaelter_A_FL'].set_attribute(ua.AttributeIds.Value, ua.DataValue(2))
            self.node_dict['Schneider/Behaelter_B_FL'].set_attribute(ua.AttributeIds.Value, ua.DataValue(3))

            self.node_dict['Schneider/Start_Umpumpen_FL'].set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

            # Embed the command line into interactive python, so that the server does not shut down
            embed()
        finally:
            # Stops and shuts down the server
            self.stop()

    # Stops the server
    def stop(self):
        print("Stopping Server ...")
        self.server.stop()

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


if __name__ == "__main__":
    server = MyServer()
    server.start()
