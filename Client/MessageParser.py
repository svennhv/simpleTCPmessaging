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
           return self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        return 'Error recieved: ' + payload['content']
    
    def parse_info(self, payload):
        return 'Server responds: ' + payload['content']

    def parse_message(self, payload):
        return 'User ' + payload['sender'] + ' sent you a message: ' + payload['content']

    def parse_history(self, payload):
        listOfMessages = 'A list of previous message responses: '
        for message in payload['content']: # Iterating over the list in 'content'. This is a list of json formatted strings
            listOfMessages = listOfMessages + '\n' + self.parse(json.dumps(message)) # Not sure if this is correct
        return listOfMessages
