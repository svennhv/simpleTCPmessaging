# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clientDictionay = {}
chatHistory = []

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
        self.username = None

        self.response = {
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            'sender': 'Server',
            'response': 'info',
            'content': 'Client connected to server. IP: ' + str(self.ip) + " Port: " + str(self.port)
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
                self.response['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                possible_requests[payload['request']](payload)
            else:
                self.response['sender'] = 'Server'
                self.response['response'] = 'error'
                self.response['content'] = 'Server could not understand request'
                self.connection.send(json.dumps(self.response))

    def handle_login(self,payload):
        self.response['sender'] = 'Server'
        requestedUsername = payload['content']
        if self.username != None:
            self.response['response'] = 'error'
            self.response['content'] = 'You are already logged in as' + self.username
        elif requestedUsername == None:
            self.response['response'] = 'error'
            self.response['content'] = 'No username specified'
        elif requestedUsername.isalnum() == False:
            self.response['response'] = 'error'
            self.response['content'] = 'Username contains illegal charachters. Only alphanumeric charachters are allowed.'
        elif clientDictionay.has_key(requestedUsername):
            self.response['response'] = 'error'
            self.response['content'] = 'Username ' + requestedUsername + ' is already taken!'
        else:
            clientDictionay[requestedUsername] = self.connection
            self.username = requestedUsername
            self.response['response'] = 'info'
            self.response['content'] = 'Login succesful'
            self.connection.send(json.dumps(self.response))
            self.response['response'] = 'history'
            self.response['content'] = chatHistory
        self.connection.send(json.dumps(self.response))

    def handle_logout(self,payload):
        self.response['sender'] = 'Server'
        if self.username == None:
            self.response['response'] = 'error'
            self.response['content'] = 'You are not logged in'
        else:
            del clientDictionay[self.username]
            self.username = None
            self.response['response'] = 'info'
            self.response['content'] = 'Logout succesful'
        self.connection.send(json.dumps(self.response))

    def handle_msg(self,payload):
        if self.username == None:
            self.response['sender'] = 'Server'
            self.response['response'] = 'error'
            self.response['content'] = 'You are not logged in'
            self.connection.send(json.dumps(self.response))
        else:
            self.response['sender'] = self.username
            self.response['response'] = 'message'
            self.response['content'] = payload['content']
            responseAsJSON = json.dumps(self.response)
            for clientSocket in clientDictionay.values():
                clientSocket.send(responseAsJSON)
            chatHistory.append(responseAsJSON)

    def handle_names(self,payload):
        self.response['sender'] = 'Server'
        if self.username == None:
            self.response['response'] = 'error'
            self.response['content'] = 'You are not logged in'
        elif len(clientDictionay) == 0:
            self.response['response'] = 'info'
            self.response['content'] = 'User list empty'
        else:
            self.response['response'] = 'info'
            self.response['content'] = 'List of users logged in:\n' + '\n'.join(clientDictionay) #Converting keys to string
        self.connection.send(json.dumps(self.response))

    def handle_help(self,payload):
        self.response['sender'] = 'Server'
        self.response['response'] = 'info'
        self.response['content'] = 'Legal requests:\nlogin <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text '
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
