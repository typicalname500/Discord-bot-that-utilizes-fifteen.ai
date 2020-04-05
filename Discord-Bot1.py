###################################################################################
#Using the brilliant API that I could only hope to call my own
#https://fifteen.ai/
###################################################################################

# bot.py
#importing modules
import os
import random
import requests
import discord

#Setting the fifteen.ai post request headers
headers = {
            'authority': 'api.fifteen.ai',
            'access-control-allow-origin': '*',
            'accept': 'application/json, text/plain, */*',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
            'dnt': '1',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://fifteen.ai',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://fifteen.ai/app',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

#
client = discord.Client()


#Announcing the bots entrance
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#Event declaration
@client.event
async def on_message(message):
    if message.author == client.user:
        return
####
#GlaDOS
####

    #Responding if the client says the phrases below 
    if message.content.startswith( 'hey glados, say' ) or message.content.startswith('hey GlaDOS, say') or message.content.startswith('hey Glados, say') or message.content.startswith('hey GlaDos, say'):
        ####
        #Change username - could also add 
        #await message.author.edit(nick="some new nick")
        ####

        #Stripping the start of the message to put the rest into the request "text" section
        Tobesaid = message.content[16:]
        print(Tobesaid)

        #Making the data section of the request
        data = '{"text":"%s","character":"GLaDOS"}' % (Tobesaid)

        #Debug print that shows the data section (makes sure the correct sting is passed)
        #print(data)

        #Constructing the request, passing in the headers and the data
        response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       

        #Checking if the api responds with a 500/ server error message
        if('server error' in response.text):
            print('error!')
            await message.channel.send('Something went wrong!')
        else:
            #Posting the response 
            with open('test1.wav', 'wb') as file:
                file.write(response.content)
            #Text to be entered with image \/  Image being specified \/
            await message.channel.send('Test',file=discord.File('test1.wav'))

            #Debug checking status code of response (403 may mean there will need to be a change to the request)
            #await message.channel.send(response.status_code)

            #Removing the file once it has been posted
            os.remove("test1.wav")
            #print("File Removed!")


####
#(MLP)Twilight sparkle 
####

            
    #Responding if the client says the phrases below
    elif message.content.startswith('hey twi, say') or message.content.startswith('hey purps, say') or message.content.startswith('hey twilight, say') or message.content.startswith('hey twiggles, say') or message.content.startswith('hey twiggle piggle, say') or message.content.startswith('Hey twi, say') or message.content.startswith('Hey purps, say') or message.content.startswith('Hey twilight, say') or message.content.startswith('Hey twiggles, say') or message.content.startswith('Hey twiggle piggle, say'):
        #"bool" to validate the below bit
        msgbool = 'f'
        #Stripping the start of the message to put the rest into the request
        #(due to the differnt sizes of string, there needs to be differnt amounts of "striping" done)
        #Make sure if there are any names that could be in names e.g twi in twilight. It doesn't like that
        if('purps' in message.content[0:13]):
            Tobesaid = message.content[14:]
            print(Tobesaid)
            msgbool = 't'
        elif('twiggles' in message.content[0:17]):
            Tobesaid = message.content[18:]
            print(Tobesaid)
            msgbool = 't'
        elif('twilight' in message.content[0:17]):
            Tobesaid = message.content[18:]
            print(Tobesaid)
            msgbool = 't'
        elif('twiggle piggle' in message.content[0:23]):
            Tobesaid = message.content[24:]
            print(Tobesaid)
            msgbool = 't'
        elif('twi' in message.content[0:12]):
            Tobesaid = message.content[13:]
            print(Tobesaid)
            msgbool = 't'
        else:
            print('error')

        #print(msgbool)
        #validating if the message managed to parse the message
        if(msgbool == 't'):

            #Making the data section of the request
            data = '{"text":"%s","character":"Twilight Sparkle"}' % (Tobesaid)
            
            #"debug" print of the above
            #print(data)

            #Constructing the request, passing in the headers and the data
            response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       

            #Checking if the api responds with a 500/ server error message
            if('server error' in response.text):
                print('error!')
                await message.channel.send('Something went wrong!')
            #Posting the response
            else:
                with open('test1.wav', 'wb') as file:
                    file.write(response.content)
                await message.channel.send('Test',file=discord.File('test1.wav'))
                #await message.channel.send(response.status_code)
                os.remove("test1.wav")
                #print("File Removed!")     
        else:
             #Showing that the parsing of the strings didnt work
             await message.channel.send('There was an error with this dumbasses code!')
        
####
#
####

    elif message.content.startswith('hey twi, say') or message.content.startswith('hey purps, say'):
        #"bool" to validate the below bit
        msgbool = 'f'
        #Stripping the start of the message to put the rest into the request
        #(due to the differnt sizes of string, there needs to be differnt amounts of "striping" done)
        #Make sure if there are any names that could be in names e.g twi in twilight. It doesn't like that
        if('purps' in message.content[0:13]):
            Tobesaid = message.content[14:]
            print(Tobesaid)
            msgbool = 't'
        elif('twiggles' in message.content[0:17]):
            Tobesaid = message.content[18:]
            print(Tobesaid)
            msgbool = 't'
        elif('twilight' in message.content[0:17]):
            Tobesaid = message.content[18:]
            print(Tobesaid)
            msgbool = 't'
        elif('twiggle piggle' in message.content[0:23]):
            Tobesaid = message.content[24:]
            print(Tobesaid)
            msgbool = 't'
        elif('twi' in message.content[0:12]):
            Tobesaid = message.content[13:]
            print(Tobesaid)
            msgbool = 't'
        else:
            print('error')

        #print(msgbool)
        #validating if the message managed to parse the message
        if(msgbool == 't'):

            #Making the data section of the request
            data = '{"text":"%s","character":"Twilight Sparkle"}' % (Tobesaid)
            
            #"debug" print of the above
            #print(data)

            #Constructing the request, passing in the headers and the data
            response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       

            #Checking if the api responds with a 500/ server error message
            if('server error' in response.text):
                print('error!')
                await message.channel.send('Something went wrong!')
            #Posting the response
            else:
                with open('test1.wav', 'wb') as file:
                    file.write(response.content)
                await message.channel.send('Test',file=discord.File('test1.wav'))
                #await message.channel.send(response.status_code)
                os.remove("test1.wav")
                #print("File Removed!")     
        else:
             #Showing that the parsing of the strings didnt work
             await message.channel.send('There was an error with this dumbasses code!')

    #Catching exceptions thrown by discord
    elif message.content == 'raise-exception':
        raise discord.DiscordException


#Running the script through the bot
client.run('Njk1MzM4NTQ2MDY3ODAwMTM1.Xod5Hw.KBBi0er7UmpbejGkViAaldRsQOQ')


