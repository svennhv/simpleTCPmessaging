# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.run()
        self.messageReciever = MessageReceiver(self,self.connection)
        self.messageParser = MessageParser()



    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        
    def disconnect(self):
        self.connection.close()

    def recieve_message(self, message):
        messageAsString = self.messageParser.parse(message)
        print(messageAsString)

    def send_payload(self, data):
        self.messageReciever.connection.send(data) #This assumes that "data" already is in JSON format

    def messageToPayload(self, message):
        # Converting user input to JSON format. Done in many steps to make the logic transparent
        splitMessage = message.split(None, 1) #Separating request and content
        request = splitMessage[0] if len(splitMessage) > 0 else None
        content = splitMessage[1] if len(splitMessage) > 1 else None
        payloadAsDictionary = {'request' : request,'content' : content}
        payload = json.dumps(payloadAsDictionary)
        return payload

    def chatClient(self):
        while True:
            userInput = raw_input()
            payload = self.messageToPayload(userInput)
            self.send_payload(payload)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
    client.chatClient()
