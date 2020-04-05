###################################################################################
#Using the brilliant API that I could only hope to call my own
#>>>>>>>>>>>>>>>>https://fifteen.ai/<<<<<<<<<<<<<<<<<<<<
###################################################################################

# bot.py
#importing modules
import os
import random
import requests
import discord

#[characher name, phrase to catch, characters to remove, type of response]
request_info=[["GlaDOS","hey glados, say" , 15, 0],["Twilight Sparkle","hey twi, say" , 12, 0],["Twilight Sparkle","hey purps, say" , 13, 0],["Twilight Sparkle","hey twilight, say" , 17, 0],["Twilight Sparkle","hey twiggles, say" , 17, 0],["Twilight Sparkle","hey twiggle piggle, say" , 23, 0],["Wheatley","hey wheatley, say" , 17, 0],["The Narrator","hey narrator, say" , 17, 0],["Tenth Doctor","hey doc, say" , 12, 0],["Tenth Doctor","hey doctor, say" , 15, 0],["Soldier","hey soldier, say" , 16, 0],["Soldier","hey soli, say" , 13, 0],["Sans","hey sans, say" , 13, 0],["Fluttershy","hey fluttershy, say" , 19, 0],["Fluttershy","hey shy, say" , 12, 0],["Fluttershy","hey flutters, say" , 17, 0],["Fluttershy","hey flutterbutter, say" , 22, 0],["Fluttershy","hey fluttershush, say" , 21, 0],["Fluttershy","hey butter shush, say" , 20, 0],["Fluttershy","hey flutter butter, say" , 22, 0],["Fluttershy","hey flutter shush, say" , 21, 0],["Fluttershy","hey butter shush, say" , 20, 0],["Rarity","hey rarity, say" , 15, 0],["Rarity","hey darling, say" , 16, 0],["Rarity","hey white ranger, say" , 21, 0],["Applejack","hey applejack, say" , 18, 0],["Applejack","hey apples, say" , 15, 0],["Applejack","hey applez, say" , 15, 0],["Applejack","hey jackapple, say" , 18, 0],["Applejack","hey aj, say", 11, 0],["Rainbow Dash","hey rainbow dash, say" , 21, 0],["Rainbow Dash","hey dash, say" , 13, 0],["Rainbow Dash","hey dashie, say" , 15, 0],["Rainbow Dash","hey rd, say" , 15, 0],["Pinkie Pie","hey pinkie pie, say" , 19, 0],["Pinkie Pie","hey pinkie, say" , 15, 0],["Pinkie Pie","hey ponka pie, say" , 18, 0],["Pinkie Pie","hey pinker ponk, say" , 20, 0],["Princess Celestia","hey princess celestia, say" , 26, 0],["Princess Celestia","hey princess, say" , 17, 0],["Princess Celestia","hey sunbutt, say" , 16, 0],["Princess Celestia","hey sun butt, say" , 17, 0],["Princess Celestia","hey tia, say" , 12, 0],["Princess Celestia","tia, say" , 8, 1]]


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

#Establishes client connection
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

    #Itterating through
    i = -1
    while i < 43:
        i = i + 1
        #print(i)
        #print(request_info[i][1])
        if message.content.startswith(request_info[i][1]):
            #print(request_info[i][3])
            if request_info[i][3] == 0:
                #Stripping the start of the message to put the rest into the request "text" section
                Tobesaid = message.content[request_info[i][2] + 1:]

                print(request_info[i][0]+" says: "+Tobesaid)

                #Making the data section of the request
                data = '{"text":"%s","character":"%s"}' % (Tobesaid, request_info[i][0])

                #Debug print that shows the data section (makes sure the correct sting is passed)
                #print(data)

                #Constructing the request, passing in the headers and the data
                response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       
            
                #Checking if the api responds with a 500/ server error message
                if('server error' in response.text):
                    print('error!')
                    await message.channel.send('Something went wrong!')
                    break
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
                    break
            elif request_info[i][3] == 1:            
                await message.channel.send("boop")
            else:
                print("boop")

#Running the script through the bot
client.run('Token')
















