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
        self.client = client
        self.connection = connection
        self = Thread(target = self.run) # Initializing the object as a thread object

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection

        # Must somehow initiaze thread(). This is my try
        self.start()
        #recieverThread.join() #Not sure if needed?

    def run(self):
        while(True):
            recievedMessage = self.connection.recv(1024) #Not sure if correct, but this is how the book recieves messages from the server
            self.client.recieve_message(recievedMessage) 
            # Maybe add a wait statement?
