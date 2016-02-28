import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	       	'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload)
        if payload['response'] in self.possible_responses:
           return payload['timestamp'] + ': ' + self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        return 'Error: ' + payload['content']
    
    def parse_info(self, payload):
        return 'Server: ' + payload['content']

    def parse_message(self, payload):
        return payload['sender'] + ': ' + payload['content']

    def parse_history(self, payload):
        listOfMessages = 'A list of previous messages: '
        for message in payload['content']: # Iterating over the list in 'content'. This is a list of json objects
            listOfMessages = listOfMessages + '\n' + self.parse(message)
        return listOfMessages
