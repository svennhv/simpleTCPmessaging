# -*- coding: utf-8 -*-
import SocketServer
import json

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.response = {
            'timestamp': None,
            'sender': 'Server',
            'response': 'info',
            'content': 'Client connected to server. IP:' + str(self.ip) + " Port: " + str(self.port)
        } 

        self.connection.send(json.dumps(self.response))

        possible_requests = {
            'login': self.handle_login,
            'logout': self.handle_logout,
            'msg': self.handle_msg,
            'names': self.handle_names,
            'help': self.handle_help
        }

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            print received_string
            payload = json.loads(received_string)
            if payload['request'] in possible_requests:
                possible_requests[payload['request']](payload)
            else:
                pass

    def handle_login(self,payload):
        #self.response['timestamp'] = timestamp(timpestamp) #Find method for this
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'Login succesful'
        self.connection.send(json.dumps(self.response))
        # Of course, here we also need to implement the actual login logic

    def handle_logout(self,payload):
        #self.response['timestamp'] = timestamp(timpestamp) #Find method for this
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'Logout succesful'
        self.connection.send(json.dumps(self.response))
        # Of course, here we also need to implement the actual logout logic

    def handle_msg(self,payload):
        #self.response['timestamp'] = timestamp(timpestamp) #Find method for this
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'Message functionality not implemented yet'
        self.connection.send(json.dumps(self.response))
        # This needs to be handled differently. How to send message to all users?

    def handle_names(self,payload):
        #self.response['timestamp'] = timestamp(timpestamp) #Find method for this
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'User list empty'
        self.connection.send(json.dumps(self.response))

    def handle_help(self,payload):
        #self.response['timestamp'] = timestamp(timpestamp) #Find method for this
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'login <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text '
        self.connection.send(json.dumps(self.response))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
