###################################################################################
#Using the brilliant API that I could only hope to call my own
#>>>>>>>>>>>>>>>>>>>>>https://fifteen.ai/<<<<<<<<<<<<<<<<<<<<<
###################################################################################

#importing modules
import os
import requests
import discord
import time
import json
import asyncio
import re
import datetime

#Opening JSON files and storing information as object variables
with open('characters.json') as json_file:
    data = json.load(json_file)    
    Character_info = data
           
with open('CustomAPIConfig.json') as json_file:
        data = json.load(json_file)
        CustomAPI_info = data 
        
with open('TokenConfig.json') as json_file:
        data = json.load(json_file)
        Token_info = data 

headers = {
   'authority': 'api.15.ai',
   'access-control-allow-origin': '*',
   'accept': 'application/json, text/plain, */*',
   'dnt': '1',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
   'content-type': 'application/json;charset=UTF-8',
   'origin': 'https://15.ai',
   'sec-fetch-site': 'same-site',
   'sec-fetch-mode': 'cors',
   'sec-fetch-dest': 'empty',
   'referer': 'https://15.ai/',
   'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'
}
  
#Establishes client connection
client = discord.Client()

#Announcing the bots entrance
@client.event
async def on_ready():  
    print(f'{client.user.name} has connected to Discord!')

#Event declaration for a message being received ('main' function)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #Variable to hold character object
    ObjectIndex = 0
    #Looping through each phrase object and passing in the relevant information
    for CharacterObject in Character_info['Phrases']:
        #Checking if the phrase used is within the character quote file
        if CharacterObject['Phrase'] in message.content:
            #Variable to store string which has had the specified phrase removed 
            PhraseRemovedString = message.content.replace(CharacterObject['Phrase'],'')
           
            #Checking what "Function is being asked for" and calling the relevant function/ breaking after it to stop the loop's itterations (I'm too lazy for a simple while loop, sue me.)
            #1. Making a request to 15.ai using the stripped message content
            #2. Using the stripped message content to make a request to wikipedia's API and then using the extract from that in the 15.ai request(s) 
            #3. Using the stripped message content to make a request to a custom API specified within the CustomAPIConfig.json file and using the parse response from that within a request to 15.ai
            if CharacterObject['Function'] == '0':
                asyncio.create_task(HandleMessageLength(PhraseRemovedString,ObjectIndex,message))
                break                                
            elif CharacterObject['Function'] == '1':                            
                await MakeWikiRequest(PhraseRemovedString,message,ObjectIndex)
                break
            elif CharacterObject['Function'] == '2':
                asyncio.create_task(HandleCustomAPIInfo(PhraseRemovedString,CharacterObject['APIReference'],message,ObjectIndex))
                break
        #Incrementing the characte object index
        ObjectIndex = ObjectIndex + 1

#Function to make a request to the 15.ai api and handle the output
async def Make15APIRequest(MessageText,CharacterIndex,message,RequestTries,FileName):   
    print(Character_info['Phrases'][CharacterIndex]['Character'] + " says: " +MessageText)
    
    #Variable to store POST content to use within the request
    data = '{"text":"%s","character":"%s","emotion":"%s","use_diagonal":%s}' % (MessageText+".", Character_info['Phrases'][CharacterIndex]['Character'], Character_info['Phrases'][CharacterIndex]['Emotion'],Character_info['Phrases'][CharacterIndex]['use_diagonal'])
    #Debug print that shows the data section (makes sure the correct sting is passed)
    #print(data)
    try:
        #Constructing the request, passing in the headers and the data
        response = requests.post('https://api.15.ai/app/getAudioFile', headers=headers, data=data)       
        #print('response recevied!')            
        #Checking if the api responds with a 500/ server error message
        if response.status_code != 200:
            print('15.ai response error!')
            #print(response.text)
            #Checking if 3 bad responses have been made and erroring as such
            if RequestTries >= 3:
                await message.channel.send('Something went wrong with making a call to 15.ai!')
            else:
                print(response.status_code)
                #Waiting 10 seconds and sending the request again
                await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
                TempRequestTries = RequestTries + 1
                print(TempRequestTries)
                asyncio.create_task(Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))
        else:
            #Creating a wav file with the response content and posting the response on discord 
            with open(FileName, 'wb') as file:
                #Saving the response as a wav file      
                file.write(response.content)
            
                #Text to be entered with file \/  file being specified \/
                await message.channel.send('Test',file=discord.File(FileName))      
                #Debug checking status code of response (403 may mean there will need to be a change to the request)
                #await message.channel.send(response.status_code)

            #Removing the file once it has been posted
            #os.remove("test1.wav")
            os.remove(FileName)
            #print("File Removed!")
            #break
    except Exception as inst:
        print('15.ai response error 2!')
        #print(response.text)
        #Checking if 3 bad responses have been made and erroring as such
        if RequestTries >= 3:
            await message.channel.send('Something went wrong with making a call to 15.ai!')
        else:
            #Waiting 10 seconds and sending the request again
            await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
            TempRequestTries = RequestTries + 1
            print(TempRequestTries)
            asyncio.create_task(Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))

#Function that makes a GET request to the Wikipedia API and then using the parsed text within a POST request to 15.ai
async def MakeWikiRequest(GivenPrompt,message,ObjectIndex):
    #https://realpython.com/python-requests/#:~:text=%20Python%E2%80%99s%20Requests%20Library%20%28Guide%29%20%201%20Getting,values%20through%20query%20string%20parameters%20in...%20More%20
    #Variable to hold wiki request
    WikiRequestString = 'https://en.wikipedia.org/api/rest_v1/page/summary/'+GivenPrompt
    #Making GET request using the above variable
    WikiRequest = requests.get(WikiRequestString)
    #Checking if the request responds OK and erroring if it doesn't
    if WikiRequest.status_code != 200:
        print('Error!')            
        await message.channel.send('Something went wrong with making a call to the Wiki API!')
    else:          
        #Parsing the JSON returned and either outputting an error "if nothing comes back for that search" or using the parsed string within a call to 15.ai
        try:
            WikiExtract = WikiRequest.json()['extract']
            #print(WikiRequest.json()['extract'])
            asyncio.create_task(HandleMessageLength(WikiExtract,ObjectIndex,message))
        except Exception as inst:
            print(inst)
            await message.channel.send('Something went wrong with parsing the Custom API!')

#Function that handles how many requests to the 15.ai api need to be made
async def HandleMessageLength(GivenText,ObjectIndex,message):
    GivenText = await CleanStrings(GivenText)
    print(GivenText)
    current_date = datetime.datetime.now()    
    FileName = 'TempAudio' + str(current_date.microsecond) + '.wav'   
    #Checking if the text is above 200 characters (15.ai character limit)
    if len(GivenText) <= 275:
        #Making a single request to 15.ai
        asyncio.create_task(Make15APIRequest(GivenText,ObjectIndex,message,0,FileName))
    else:
        #Character "Chunk" number
        n = 275
        # Using list comprehension to split the string into 73 chharacter "chunks" (https://pythonexamples.org/python-split-string-into-specific-length-chunks/)
        out = [(GivenText[i:i+n]) for i in range(0, len(GivenText), n)]
        for Substring in out:
            current_date = datetime.datetime.now()         
            FileName = 'TempAudio' + str(current_date.microsecond) + '.wav'
            print(FileName)
            #print(Substring)
            asyncio.create_task(Make15APIRequest(Substring,ObjectIndex,message,0,FileName))
        
#Function to handle what custom API should be being used and what API call should be used
async def HandleCustomAPIInfo(GivenText,CustomAPIReference,message,ObjectIndex):
    #Index to allow passing of what object to use
    CustomAPIIndex = 0
    #Looping through each of the custom API objects
    for CustomAPIObject in CustomAPI_info['APIs']:       
        #Checking the object reference to see if it is the one specified by the quote
        if CustomAPIObject['ObjectReference'] == CustomAPIReference:
            #Temporary variable to be passed to the request function to be the APICall to use
            TempAPICall = ''
            if '{0}' in CustomAPIObject['BaseAPICall']:
                #Making the API call that will be passed with the specified section being replaced with the text after the quote
                TempAPICall = CustomAPIObject['BaseAPICall'].replace('{0}',GivenText)
            else:
                #Making the API call that will be passed just the request
                TempAPICall = CustomAPIObject['BaseAPICall']
                
            if CustomAPIObject['ReqType'] == 'GET':
                #Calling function to handle making a get request/ parsing its output
                asyncio.create_task(MakeCustomGETAPICall(message,CustomAPIIndex,TempAPICall,ObjectIndex))
            else:
                #Making Post requests seem to be a little more tricky. Will add soon (hopefully)
                print('b')
        #Incrementing index
        CustomAPIIndex = CustomAPIIndex + 1
       
#Function to make GET request and handle its output     
async def MakeCustomGETAPICall(message,CustomAPIIndex,APICall,ObjectIndex):   
    #Making a get request to the custom API
    CustomAPIRequest = requests.get(APICall)
    if CustomAPIRequest.status_code != 200:
        #Showing "error" in console/ letting the user know that there was an error
        print('Error!')       
        await message.channel.send('Something went wrong with making a call to the Custom API!')
    else:          
        #Checking the type of output (XML/ JSON)
        if CustomAPI_info['APIs'][CustomAPIIndex]['OutputType'] == 'JSON':
            try:
                #Parsing text from the path given
                CustomAPIExtract = CustomAPIRequest.json()[CustomAPI_info['APIs'][CustomAPIIndex]['JSONPath']]
                #print(WikiRequest.json()['extract'])
                #Calling the fucntion to use the parsed string in a request to 15.ai
                asyncio.create_task(HandleMessageLength(CustomAPIExtract,ObjectIndex,message))
            except Exception as inst:
                #Showing error in console/ letting the user know that there was an error
                print(inst)
                await message.channel.send('Something went wrong with parsing the Custom API!')
        else:
            try:                               
                #Using etree to parse the XML using (https://stackoverflow.com/a/52506999)
                from lxml.etree import fromstring
                string = CustomAPIRequest.text
                response = fromstring(string.encode('utf-8'))
                elm = response.xpath(CustomAPI_info['APIs'][CustomAPIIndex]['XMLPath']).pop()
                CustomAPIExtract = elm.text                
                #Calling the fucntion to use the parsed string in a request to 15.ai
                asyncio.create_task(HandleMessageLength(CustomAPIExtract,ObjectIndex,message))
            except Exception as inst:
                #Showing error in console/ letting the user know that there was an error
                print(inst)
                await message.channel.send('Something went wrong with parsing the Custom API!')           

#Function to remove non ASCII characters and also remove special characters
async def CleanStrings(string_nonASCII):
    #Making the given string encoded in ascii  
    string_encode = string_nonASCII.encode("ascii", "ignore") # https://pythonguides.com/remove-unicode-characters-in-python/#:~:text=In%20python,%20to%20remove%20non-ASCII%20characters%20in%20python,,a%20string%20without%20ASCII%20character%20use%20string.decode().%20Example:
    string_decode = string_encode.decode()
    #Removing special characters
    string_decode = re.sub(r"[^a-zA-Z0-9\.\,\s]+", '', string_decode) # https://stackoverflow.com/questions/43358857/how-to-remove-special-characters-except-space-from-a-file-in-python
    return string_decode

#Running the script through the bot
client.run(Token_info['token'])