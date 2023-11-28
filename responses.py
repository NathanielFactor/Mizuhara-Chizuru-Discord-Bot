import random


def handle_response(message) -> str:
    p_message = message.lower()
    
    if p_message == 'hello':
        return 'hi!'
    
    if p_message == 'roll':
        return str(random.randint(1,99))
    
    if p_message == '!help':
        return str('modify this later')
    
    return "I don't know what you said, please repeat or use !help for a list of commands"