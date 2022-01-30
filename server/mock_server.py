## @file Server.py
#
# @brief File for the server class
# @author Alexander Krause
import logging
import sys
from opcua import ua, uamethod, Server

## Server endpoint definition
#
# Defines how the server can be reached and stores the path for the custom Namespace xml file
namespace = "server/Namespace/myNS.xml"
uri = "http://tu-dresden.de/iat-opc/"
name = "IAT OPC Server"
endpoint = "opc.tcp://localhost:4840/freeopcua/server/"

## Interactive Python import
try:
    from IPython import embed
except ImportError:
    import code

    ## Interactive python function
    # This way one can run python commands on the console when the server is set up and running
    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

sys.path.insert(0, "../..")


## Server class
# This is the server class containing the OPC-UA Server.
class MyServer():
    ## Server Initializer
    # Sets up the server with address, namspace, uri and creates the OPC Server object.
    def __init__(self):
        ## optional: setup logging.
        logging.basicConfig(level=logging.WARN)

        ## Creates the actual OPC server object from FreeOPCUA
        self.server = Server()
        # server.disable_clock()
        ## Address of the server
        self.server.set_endpoint(endpoint)
        ## Name of the server
        self.server.set_server_name(name)
        ## set all possible endpoint policies for clients to connect through
        self.server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])

        ## Our namespace uri
        self.idx = self.server.register_namespace(uri)

        ## get Objects node
        self.objects = self.server.get_objects_node()

        ## import the actual nodes from our namespace
        self.server.import_xml(namespace)

    ## Starts the server
    def start(self):
        ## After that the server is online and running
        self.server.start()
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        try:
            # do stuff here

            print("before embed()")
            ## Embed the command line into interactive python, so that the server does not shut down
            embed()
        finally:
            ## Stops and shuts down the server
            self.stop()

    ## Stops the server
    def stop(self):
        print("Stopping Server ...")
        self.server.stop()


## Main function that creates our server.
#
# This function is called when you run the file.
if __name__ == "__main__":
    server = MyServer()
    server.start()
