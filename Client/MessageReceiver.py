# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection

    def run(self):
        recievedMessage = self.connection.recv(1024) #Added by Pål, not sure if correct, but this is how the book recieves messages from the server
        self.client.recieve_message(recievedMessage) #Added by Pål
        # TODO: Make MessageReceiver receive and handle payloads
