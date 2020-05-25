###################################################################################
#Using the brilliant API that I could only hope to call my own
#>>>>>>>>>>>>>>>>https://fifteen.ai/<<<<<<<<<<<<<<<<<<<<
###################################################################################

# bot.py
#importing modules
import os
#import random
import requests
import discord
import time
import wikipedia

#[characher name, phrase to catch, characters to remove, type of response]
#Creating a "2D array" that holds the request information and phrases to be checked
request_info=[["GLaDOS","hey glados, say" , 15, 0, "Neutral"],["Twilight Sparkle","hey twi, say" , 12, 0, "Neutral"],["Twilight Sparkle","hey purps, say" , 13, 0, "Neutral"],["Twilight Sparkle","hey twilight, say" , 17, 0, "Neutral"],["Twilight Sparkle","hey twiggles, say" , 17, 0, "Neutral"],["Twilight Sparkle","hey twiggle piggle, say" , 23, 0, "Neutral"],["Twilight Sparkle","hey twi, happily say" , 20, 0, "Happy"],["Twilight Sparkle","hey purps, happily say" , 22, 0, "Happy"],["Twilight Sparkle","hey twilight, happily say" , 25, 0, "Happy"],["Twilight Sparkle","hey twiggles, happily say" , 25, 0, "Happy"],["Twilight Sparkle","hey twiggle piggle, happily say" , 31, 0, "Happy"],["Wheatley","hey wheatley, say" , 17, 0, "Neutral"],["The Narrator","hey narrator, say" , 17, 0, "Neutral"],["Tenth Doctor","hey doc, say" , 12, 0, "Neutral"],["Tenth Doctor","hey doctor, say" , 15, 0, "Neutral"],["Soldier","hey soldier, say" , 16, 0, "Neutral"],["Soldier","hey soli, say" , 13, 0, "Neutral"],["Sans","hey sans, say" , 13, 0, "Neutral"],["Fluttershy","hey fluttershy, say" , 19, 0, "Neutral"],["Fluttershy","hey shy, say" , 12, 0, "Neutral"],["Fluttershy","hey flutters, say" , 17, 0, "Neutral"],["Fluttershy","hey flutterbutter, say" , 22, 0, "Neutral"],["Fluttershy","hey fluttershush, say" , 21, 0, "Neutral"],["Fluttershy","hey butter shush, say" , 20, 0, "Neutral"],["Fluttershy","hey flutter butter, say" , 22, 0, "Neutral"],["Fluttershy","hey flutter shush, say" , 21, 0, "Neutral"],["Fluttershy","hey butter shush, say" , 20, 0, "Neutral"],["Rarity","hey rarity, say" , 15, 0, "Neutral"],["Rarity","hey darling, say" , 16, 0, "Neutral"],["Rarity","hey white ranger, say" , 21, 0, "Neutral"],["Applejack","hey applejack, say" , 18, 0, "Neutral"],["Applejack","hey apples, say" , 15, 0, "Neutral"],["Applejack","hey applez, say" , 15, 0, "Neutral"],["Applejack","hey jackapple, say" , 18, 0, "Neutral"],["Applejack","hey aj, say", 11, 0, "Neutral"],["Rainbow Dash","hey rainbow dash, say" , 21, 0, "Neutral"],["Rainbow Dash","hey dash, say" , 13, 0, "Neutral"],["Rainbow Dash","hey dashie, say" , 15, 0, "Neutral"],["Rainbow Dash","hey rd, say" , 15, 0, "Neutral"],["Pinkie Pie","hey pinkie pie, say" , 19, 0, "Neutral"],["Pinkie Pie","hey pinkie, say" , 15, 0, "Neutral"],["Pinkie Pie","hey ponka pie, say" , 18, 0, "Neutral"],["Pinkie Pie","hey pinker ponk, say" , 20, 0, "Neutral"],["Princess Celestia","hey princess celestia, say" , 26, 0, "Neutral"],["Princess Celestia","hey princess, say" , 17, 0, "Neutral"],["Princess Celestia","hey sunbutt, say" , 16, 0, "Neutral"],["Princess Celestia","hey sun butt, say" , 17, 0, "Neutral"],["Princess Celestia","hey tia, say" , 12, 0, "Neutral"],["Princess Celestia","tia, say" , 8, 1, "Neutral"],['GlaDOS','hey glados, tell me about',25, 1, "Neutral"],['Twilight Sparkle','hey twi, tell me about',22, 1, "Neutral"],['Twilight Sparkle','hey purps, tell me about',24,1],['Twilight Sparkle','hey twilight, tell me about',27, 1, "Neutral"],['Twilight Sparkle','hey twiggles, tell me about',27, 1, "Neutral"],['Twilight Sparkle','hey twiggle piggle, tell me about',33, 1, "Neutral"],['Twilight Sparkle','hey twi, happily tell me about',30, 1, "Neutral"],['Twilight Sparkle','hey purps, happily tell me about',32,1],['Twilight Sparkle','hey twilight, happily tell me about',35, 1, "Neutral"],['Twilight Sparkle','hey twiggles, happily tell me about',35, 1, "Neutral"],['Twilight Sparkle','hey twiggle piggle, happily tell me about',41, 1, "Neutral"],['Wheatley','hey wheatley, tell me about',27, 1, "Neutral"],['The Narrator','hey narrator, tell me about',27, 1, "Neutral"],['Tenth Doctor','hey doc, tell me about',22, 1, "Neutral"],['Tenth Doctor','hey doctor, tell me about',25, 1, "Neutral"],['Soldier','hey soldier, tell me about',26, 1, "Neutral"],['Soldier','hey soli, tell me about',23, 1, "Neutral"],['Sans','hey sans, tell me about',23, 1, "Neutral"],['Fluttershy','hey fluttershy, tell me about',29, 1, "Neutral"],['Fluttershy','hey shy, tell me about',22, 1, "Neutral"],['Fluttershy','hey flutters, tell me about',27, 1, "Neutral"],['Fluttershy','hey flutterbutter, tell me about',32, 1, "Neutral"],['Fluttershy','hey fluttershush, tell me about',31, 1, "Neutral"],['Fluttershy','hey butter shush, tell me about',31, 1, "Neutral"],['Fluttershy','hey flutter butter, tell me about',33, 1, "Neutral"],['Fluttershy','hey flutter shush, tell me about',32, 1, "Neutral"],['Fluttershy','hey butter shush, tell me about',31, 1, "Neutral"],['Rarity','hey rarity, tell me about',25, 1, "Neutral"],['Rarity','hey darling, tell me about',26, 1, "Neutral"],['Rarity','hey white ranger, tell me about',31, 1, "Neutral"],['Applejack','hey applejack, tell me about',28, 1, "Neutral"],['Applejack','hey apples, tell me about',25, 1, "Neutral"],['Applejack','hey applez, tell me about',25, 1, "Neutral"],['Applejack','hey jackapple, tell me about',28, 1, "Neutral"],['Applejack','hey aj, tell me about',21, 1, "Neutral"],['Rainbow Dash','hey rainbow dash, tell me about',31, 1, "Neutral"],['Rainbow Dash','hey dash, tell me about',23, 1, "Neutral"],['Rainbow Dash','hey dashie, tell me about',25, 1, "Neutral"],['Rainbow Dash','hey rd, tell me about',21, 1, "Neutral"],['Pinkie Pie','hey pinkie pie, tell me about',29, 1, "Neutral"],['Pinkie Pie','hey pinkie, tell me about',25, 1, "Neutral"],['Pinkie Pie','hey ponka pie, tell me about',28, 1, "Neutral"],['Pinkie Pie','hey pinker ponk, tell me about',30, 1, "Neutral"],['Princess Celestia','hey princess celestia, tell me about',36, 1, "Neutral"],['Princess Celestia','hey princess, tell me about',27, 1, "Neutral"],['Princess Celestia','hey sunbutt, tell me about',26, 1, "Neutral"],['Princess Celestia','hey sun butt, tell me about',27, 1, "Neutral"],['Princess Celestia','hey tia, tell me about',22, 1, "Neutral"],['Princess Celestia','tia, tell me about',18, 1, "Neutral"]]

#["GlaDOS","hey glados, tell me about" , 15, 1],["Twilight Sparkle","hey twi, tell me about" , 12, 1],["Twilight Sparkle","hey purps, tell me about" , 13, 1],["Twilight Sparkle","hey twilight, tell me about" , 17, 1],["Twilight Sparkle","hey twiggles, tell me about" , 17, 1],["Twilight Sparkle","hey twiggle piggle, tell me about" , 23, 1],["Wheatley","hey wheatley, tell me about" , 17, 1],["The Narrator","hey narrator, tell me about" , 17, 1],["Tenth Doctor","hey doc, tell me about" , 12, 1],["Tenth Doctor","hey doctor, tell me about" , 15, 1],["Soldier","hey soldier, tell me about" , 16, 1],["Soldier","hey soli, tell me about" , 13, 1],["Sans","hey sans, tell me about" , 13, 1],["Fluttershy","hey fluttershy, tell me about" , 19, 1],["Fluttershy","hey shy, tell me about" , 12, 1],["Fluttershy","hey flutters, tell me about" , 17, 1],["Fluttershy","hey flutterbutter, tell me about" , 22, 1],["Fluttershy","hey fluttershush, tell me about" , 21, 1],["Fluttershy","hey butter shush, tell me about" , 20, 1],["Fluttershy","hey flutter butter, tell me about" , 22, 1],["Fluttershy","hey flutter shush, tell me about" , 21, 1],["Fluttershy","hey butter shush, tell me about" , 20, 1],["Rarity","hey rarity, tell me about" , 15, 1],["Rarity","hey darling, tell me about" , 16, 1],["Rarity","hey white ranger, tell me about" , 21, 1],["Applejack","hey applejack, tell me about" , 18, 1],["Applejack","hey apples, tell me about" , 15, 1],["Applejack","hey applez, tell me about" , 15, 1],["Applejack","hey jackapple, tell me about" , 18, 1],["Applejack","hey aj, tell me about", 11, 1],["Rainbow Dash","hey rainbow dash, tell me about" , 21, 1],["Rainbow Dash","hey dash, tell me about" , 13, 1],["Rainbow Dash","hey dashie, tell me about" , 15, 1],["Rainbow Dash","hey rd, tell me about" , 15, 1],["Pinkie Pie","hey pinkie pie, tell me about" , 19, 1],["Pinkie Pie","hey pinkie, tell me about" , 15, 1],["Pinkie Pie","hey ponka pie, tell me about" , 18, 1],["Pinkie Pie","hey pinker ponk, tell me about" , 20, 1],["Princess Celestia","hey princess celestia, tell me about" , 26, 1],["Princess Celestia","hey princess, tell me about" , 17, 1],["Princess Celestia","hey sunbutt, tell me about" , 16, 1],["Princess Celestia","hey sun butt, tell me about" , 17, 1],["Princess Celestia","hey tia, tell me about" , 12, 1],["Princess Celestia","tia, tell me about" , 8, 1]

#['GlaDOS','hey glados, tell me about',25,1],['Twilight Sparkle','hey twi, tell me about',22,1],['Twilight Sparkle','hey purps, tell me about',24,1],['Twilight Sparkle','hey twilight, tell me about',27,1],['Twilight Sparkle','hey twiggles, tell me about',27,1],['Twilight Sparkle','hey twiggle piggle, tell me about',33,1],['Wheatley','hey wheatley, tell me about',27,1],['The Narrator','hey narrator, tell me about',27,1],['Tenth Doctor','hey doc, tell me about',22,1],['Tenth Doctor','hey doctor, tell me about',25,1],['Soldier','hey soldier, tell me about',26,1],['Soldier','hey soli, tell me about',23,1],['Sans','hey sans, tell me about',23,1],['Fluttershy','hey fluttershy, tell me about',29,1],['Fluttershy','hey shy, tell me about',22,1],['Fluttershy','hey flutters, tell me about',27,1],['Fluttershy','hey flutterbutter, tell me about',32,1],['Fluttershy','hey fluttershush, tell me about',31,1],['Fluttershy','hey butter shush, tell me about',31,1],['Fluttershy','hey flutter butter, tell me about',33,1],['Fluttershy','hey flutter shush, tell me about',32,1],['Fluttershy','hey butter shush, tell me about',31,1],['Rarity','hey rarity, tell me about',25,1],['Rarity','hey darling, tell me about',26,1],['Rarity','hey white ranger, tell me about',31,1],['Applejack','hey applejack, tell me about',28,1],['Applejack','hey apples, tell me about',25,1],['Applejack','hey applez, tell me about',25,1],['Applejack','hey jackapple, tell me about',28,1],['Applejack','hey aj, tell me about',21,1],['Rainbow Dash','hey rainbow dash, tell me about',31,1],['Rainbow Dash','hey dash, tell me about',23,1],['Rainbow Dash','hey dashie, tell me about',25,1],['Rainbow Dash','hey rd, tell me about',21,1],['Pinkie Pie','hey pinkie pie, tell me about',29,1],['Pinkie Pie','hey pinkie, tell me about',25,1],['Pinkie Pie','hey ponka pie, tell me about',28,1],['Pinkie Pie','hey pinker ponk, tell me about',30,1],['Princess Celestia','hey princess celestia, tell me about',36,1],['Princess Celestia','hey princess, tell me about',27,1],['Princess Celestia','hey sunbutt, tell me about',26,1],['Princess Celestia','hey sun butt, tell me about',27,1],['Princess Celestia','hey tia, tell me about',22,1],['Princess Celestia','tia, tell me about',18,1]

#Setting the fifteen.ai post request headers
headers = {
    'authority': 'api.fifteen.ai',
    'access-control-allow-origin': '*',
    'accept': 'application/json, text/plain, */*',
    'sec-fetch-dest': 'empty',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36',
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


#Making a single request and responding to it
async def make_request(i, message):
    print(request_info[i][3])
    if request_info[i][3] == 0:
        #Stripping the start of the message to put the rest into the request "text" section
        Tobesaid = message.content[request_info[i][2] + 1:]
        #Printing the character and the 
        print(request_info[i][0]+" says: "+Tobesaid)
    
        #print(len(Tobesaid))
        #Making the data section of the request
        data = '{"text":"%s","character":"%s","emotion":"%s"}' % (Tobesaid+".", request_info[i][0], request_info[i][4])

        #Debug print that shows the data section (makes sure the correct sting is passed)
        print(data)

        #Constructing the request, passing in the headers and the data
        response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       
        print('response recevied!')            
        #Checking if the api responds with a 500/ server error message
        #print(response.text)
        if('server error' in response.text):
            print('error!')
            print(response.text)
            await message.channel.send('Something went wrong!')
            #time.sleep(20)
            #break
        else:
            #Posting the response 
            with open('test1.wav', 'wb') as file:               
                file.write(response.content)
            #print(response.text)
            #Text to be entered with image \/  Image being specified \/
            await message.channel.send('Test',file=discord.File('test1.wav'))

            #Debug checking status code of response (403 may mean there will need to be a change to the request)
            #await message.channel.send(response.status_code)

            #Removing the file once it has been posted
            os.remove("test1.wav")
            #print("File Removed!")
            #break
    elif request_info[i][3] == 1:
        #Stripping the start of the message to put the rest into the request "text" section
        Tobegiven = message.content[request_info[i][2] + 1:]                  
        #print(wikipedia.summary(One, sentences=1))
                    
        Tobesaid = str(wikipedia.summary(Tobegiven, sentences=1))
        #print(Two)
        
        #Stripping the start of the message to put the rest into the request "text" section
        #Tobesaid = message.content[request_info[i][2] + 1:]
        #Printing the character and the 
        print(request_info[i][0]+" says: "+Tobesaid)
    
        #print(len(Tobesaid))
        #Making the data section of the request
        data = '{"text":"%s","character":"%s","emotion":"%s"}' % (Tobesaid+".", request_info[i][0], request_info[i][4])

        #Debug print that shows the data section (makes sure the correct sting is passed)
        print(data)

        #Constructing the request, passing in the headers and the data
        response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       
        print('response recevied!')            
        #Checking if the api responds with a 500/ server error message
        #print(response.text)
        if('server error' in response.text):
            print('error!')
            print(response.text)
            await message.channel.send('Something went wrong!')
            #time.sleep(20)
            #break
        else:
            #Posting the response 
            with open('test1.wav', 'wb') as file:               
                file.write(response.content)
            #print(response.text)
            #Text to be entered with image \/  Image being specified \/
            await message.channel.send('Test',file=discord.File('test1.wav'))

            #Debug checking status code of response (403 may mean there will need to be a change to the request)
            #await message.channel.send(response.status_code)

            #Removing the file once it has been posted
            os.remove("test1.wav")
            #print("File Removed!")
            #break

async def make_several_requests(i,Tobesaid,message):
    n = 74
    # Using list comprehension 
    out = [(Tobesaid[i:i+n]) for i in range(0, len(Tobesaid), n)] 
    #Printing the character and the 
    print(request_info[i][0]+" says: "+Tobesaid)
    # Printing output 
    #print(out)
    #print(len(out))

    for x in out:
        #Making the data section of the request
        data = '{"text":"%s","character":"%s","emotion":"%s"}' % (Tobesaid+".", request_info[i][0], request_info[i][4])

        #Debug print that shows the data section (makes sure the correct sting is passed)
        print(data)

        #Constructing the request, passing in the headers and the data
        response = requests.post('https://api.fifteen.ai/app/getAudioFile', headers=headers, data=data)       
        #print('sent request')            
        #Checking if the api responds with a 500/ server error message
        #print(response.text)
        if('server error' in response.text):
            print('error!')
            print(str(response.text))
            await message.channel.send('Something went wrong!')
            #time.sleep(20)
            #break
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
            #break                     




#Announcing the bots entrance
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#Event declaration
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Itterating through each object in the array to see if the phrases match
    i = -1
    while i < 96:
        i = i + 1
        #Debug prints the index and the phrases
        #print(i)
        #print(request_info[i][1])

        #Checking if the phrase and the message content match
        Msgstartwith = message.content[0:request_info[i][2]]
        #print(Msgstartwith)
        #boop = request_info[i][1]
        #print(boop)
        
        #if message.content.startswith(request_info[i][1].lower()):
        if Msgstartwith == request_info[i][1]:
            #Debug to show the 'function type'
            #print(request_info[i][3])

            #Checking what 'function' to use (hey x say y)
            if request_info[i][3] == 0:
                #Stripping the start of the message to put the rest into the request "text" section
                Tobesaid = message.content[request_info[i][2] + 1:]                
                #print(len(Tobesaid))

                if len(Tobesaid) >= 80:
                    #print("a")
                    await make_several_requests(i,Tobesaid,message)                         
                else:       
                    #print("b")      
                    await make_request(i, message)
            #Function 2: 
            elif request_info[i][3] == 1:                                      
                try:
                    #Stripping the start of the message to put the rest into the request "text" section
                    Tobegiven = message.content[request_info[i][2] + 1:]                  
                    #print(wikipedia.summary(One, sentences=1))
                    
                    Tobesaid = str(wikipedia.summary(Tobegiven, sentences=1))
                    #print(Two)
                    if len(Tobesaid) >= 75:
                        #print("c")
                        await make_several_requests(i,Tobesaid,message)
                    else:       
                        #print("d")      
                        await make_request(i, message)
                    
                    #await message.channel.send(wikipedia.summary(Tobesaid, sentences=1))
                except Exception as inst:
                    print(inst)
            else:
                print("boop")

#Running the script through the bot
client.run('Tolen')
