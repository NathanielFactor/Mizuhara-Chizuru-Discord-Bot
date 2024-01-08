import discord
import sqlite3
from app.openai import ai_response

# settings.py for env token
import os
from dotenv import load_dotenv, find_dotenv


def get_db_connection():
    conn = sqlite3.connect('db/Conversations.db')
    conn.row_factory = sqlite3.Row
    return conn
    

def addMessages(discordUser, message):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch UserNames, Userid, and Messages
    cur.execute("SELECT UserName, Userid, Messages FROM CONVERSATIONS")
    rows = cur.fetchall()

    if rows is not None:
        for row in rows:
            UserNames_list = row["UserName"]
            Userid = row["Userid"]
            Messages_list = row["Messages"]

            # Making sure Message history is no more than 3, updating database if so
            if Messages_list is not None and len("".join(Messages_list)) == 3:
                
                # Update the existing Messages rather than deleting all
                new_messages = Messages_list[1:] + [message]
                cur.execute("UPDATE Conversations SET Messages = ? WHERE Userid = ?", (new_messages, Userid))


            for i in range(len(UserNames_list)):
                userName = UserNames_list[i]

                if discordUser == userName:
                    # Insert new message for the specific user
                    cur.execute("UPDATE Conversations SET Messages = ? WHERE Userid = ?", (message, Userid))

    conn.commit()
    conn.close()


def retreieveMessages():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch Messages
    cur.execute("SELECT Messages FROM CONVERSATIONS")
    rows = cur.fetchall()

    Messages_list = [row["Messages"] for row in rows] if rows is not None else []

    conn.commit()
    conn.close()
    print(Messages_list)
    return Messages_list


def retreieveUserNames():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch UserNames
    cur.execute("SELECT UserName FROM CONVERSATIONS")
    rows = cur.fetchall()

    UserName_list = [row["UserName"] for row in rows] if rows is not None else []

    conn.commit()
    conn.close()
    return UserName_list

      
    
def run_discord_bot():
    
    load_dotenv(find_dotenv())
    TOKEN = str(os.environ.get("token"))
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    #Confirmation of bot functionality
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    #Message Event Function        
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
        #If I wish to shutdown the bot within discord
        if username == '_c0bra' and command == '/shutdown':
            exit()
        
        #Adding user_message to database       
        #addMessages(username,user_message)
        print(f"{username} said:  '{command}' '{user_message}' ({channel})")
        
        
        if command in ['/ai', '/bot', '/chizuru', 'mizuhara']:
            #messageHistory = retreieveMessages()
            bot_response = ai_response(user_message)
            await message.channel.send(f"{bot_response}")
    
    client.run(TOKEN)