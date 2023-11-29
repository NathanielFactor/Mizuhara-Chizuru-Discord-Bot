import discord
from app.openai import ai_response

# settings.py for env token
import os
from dotenv import load_dotenv, find_dotenv


def run_discord_bot():
    load_dotenv(find_dotenv())
    TOKEN = str(os.environ.get("token"))
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
                
    @client.event
    async def on_message(message):
        
        if message.author == client.user:
            return
        
        username = str(message.author)
        channel = str(message.channel)
        command = None
        user_message = None
        
        for text in ['/ai','/bot','/chizuru','mizuhara','/shutdown','/dm']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                user_message = message.content.replace(text, ' ')
        
        print(f"{username} said:  '{command}' '{user_message}' ({channel})")
        
        if username == '_c0bra' and command == '/shutdown':
            exit()
        
        if command in ['/ai', '/bot', '/chizuru', 'mizuhara']:
            bot_response = ai_response(user_message)
            await message.channel.send(f"{bot_response}")
                
#        if command == '/dm':
 #           user_message = user_message[1:]
  #          await message.channel.send(message,user_message,is_private=True)
   #     else:
    #        await message.channel.send(message,user_message,is_private=False)
    
    client.run(TOKEN)