import random


def handle_response(message) -> str:
    p_message = message.lower()
    
    if p_message == 'hello':
        return 'hi!'
    
    if p_message == '!roll':
        return str(random.randint(1,99))
    
    if p_message == '!chat':
        return 'I am still working on this :3'
    
    if p_message == '!play':
        return 'I am still working on this :3'

    if p_message == '!help':
        return str('Ehhhhhh ... you need help? Let me know if this is good then!\n------------------------------------------------------------\n!help - I give you a list of helpful commands:)\n!chat - We get to chat freely but at a cost of 24000 yen per hour :3\n!roll - I roll a random number for some reason ?\n!play (link) - I join the voice channel and play your link :3')
    
    return "I don't know what you said\nplease repeat or use !help for a list of commands"