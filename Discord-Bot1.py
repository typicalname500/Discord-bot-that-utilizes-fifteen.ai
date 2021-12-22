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
from num2words import num2words

#Getting the JSON data for the 
#---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

#Opening JSON files and storing information as object variables (Thanks to https://github.com/alierenbozbulut, who spotted a few blunders I made in documentation/ methods of calling the json data )
with open('TokenConfig.json') as json_file:
    string0 = json_file.read()

data0 = json.loads(string0)
Token_info = data0
data0 = None 

#Opening the file within the tokenconfig file relating to the character phrases and saving the JSON
with open(Token_info['CharacterInfoFile']) as json_file:
    string1 = json_file.read()

data1 = json.loads(string1)    
Character_info = data1
data1 = None

#Opening the file within the tokenconfig file relating to the custom API info and saving the JSON
with open(Token_info['CustomAPIfilepath']) as json_file:
    string2 = json_file.read()

data2 = json.loads(string2)
CustomAPI_info = data2
data2 = None

#---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


#Headers to use to make a request to 15.ai
FirstRequestHeaders = {
  'authority': 'api.15.ai',
  'access-control-allow-origin': '*',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
  'sec-ch-ua': '\\"Chromium\\";v=\\"94\\", \\"Microsoft Edge\\";v=\\"94\\", \\";Not A Brand\\";v=\\"99\\"',
  'sec-ch-ua-platform': '\\"Windows\\"',
  'content-type': 'application/json;charset=UTF-8',
  'origin': 'https://15.ai',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://15.ai/'
}

SecondReqheaders = {
  'authority': 'cdn.15.ai',
  'sec-ch-ua': '\\"Chromium\\";v=\\"94\\", \\"Microsoft Edge\\";v=\\"94\\", \\";Not A Brand\\";v=\\"99\\"',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
  'sec-ch-ua-platform': '\\"Windows\\"',
  'accept': '*/*',
  'origin': 'https://15.ai',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://15.ai/',
  'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'
}  

#Null payload for GET requests (because for some reason the function still needs one)
Nullpayload={}

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
            #0. Making a request to 15.ai using the stripped message content
            #1. Using the stripped message content to make a request to wikipedia's API and then using the extract from that in the 15.ai request(s) 
            #2. Using the stripped message content to make a request to a custom API specified within the CustomAPIConfig.json file and using the parse response from that within a request to 15.ai
            #3. Making a request to 15.ai using the stripped message content in a voice call
            if CharacterObject['Function'] == '0':
                asyncio.create_task(HandleMessageLength(PhraseRemovedString,ObjectIndex,message))
                break
            elif CharacterObject['Function'] == '1':                            
                await MakeWikiRequest(PhraseRemovedString,message,ObjectIndex)
                break
            elif CharacterObject['Function'] == '2':
                asyncio.create_task(HandleCustomAPIInfo(PhraseRemovedString,CharacterObject['APIReference'],message,ObjectIndex))
                break
            elif CharacterObject['Function'] == '3':
                asyncio.create_task(VC_HandleMessageLength(PhraseRemovedString,ObjectIndex,message))             
                break
        #Incrementing the characte object index
        ObjectIndex = ObjectIndex + 1

    #Checking if the message has either of the strings within it
    if "Hey bot join our voice chat" in message.content or "bot join vc" in message.content:
        #Getting the current voice channel the user is in and joining it 
        channel = message.author.voice.channel
        await channel.connect()

    #https://stackoverflow.com/questions/50651305/message-object-has-no-attribute-server
    if "Hey bot, leave our voice chat" in message.content or "bot leave vc" in message.content:
        #Getting the current voice channel the user is in and leaving it
        for x in client.voice_clients:
            if x.guild == message.guild:
                return await x.disconnect()

#Function to make a request to the 15.ai api and handle the output
async def Make15APIRequest(MessageText,CharacterIndex,message,RequestTries,FileName):   
    print(Character_info['Phrases'][CharacterIndex]['Character'] + " says: " +MessageText)
    
    #Variable to store POST content to use within the request
    #data = '{"text":"%s","character":"%s","emotion":"%s","use_diagonal":%s}' % (MessageText+".", Character_info['Phrases'][CharacterIndex]['Character'], Character_info['Phrases'][CharacterIndex]['Emotion'],Character_info['Phrases'][CharacterIndex]['use_diagonal'])
    data = '{"text":"%s","character":"%s","emotion":"%s"}' % (MessageText+".", Character_info['Phrases'][CharacterIndex]['Character'], Character_info['Phrases'][CharacterIndex]['Emotion'])
    
    #Debug print that shows the data section (makes sure the correct string is passed)
    print(data)
    try:
        #Constructing the request, passing in the headers and the data 
        firstresponse = requests.post('https://api.15.ai/app/getAudioFile5', headers=FirstRequestHeaders, data=data)              
        #Checking if the api responds with a 500/ server error message
        if firstresponse.status_code != 200:
            print('15.ai response error!')
            #print(response.text)
            #Checking if 3 bad responses have been made and erroring as such
            if RequestTries >= 3:
                await message.channel.send('Something went wrong with making the first call to 15.ai!')
            else:
                #Showing the status code of the respomse
                print(firstresponse.status_code)
                #Waiting 10 seconds and sending the request again
                await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
                TempRequestTries = RequestTries + 1
                print(TempRequestTries)
                asyncio.create_task(Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))
        else:
            #Parsing the json from the first request's response
            fifteenaijsontext = json.loads(firstresponse.text)
            
            #Selecting the generated wav file name
            wavfilelocation = fifteenaijsontext['wavNames'][0]

            #Creating a URL based on the output of the past request
            newrequesturl = "https://cdn.15.ai/audio/" + wavfilelocation
           
            #Making the second request to get the generated wav file
            secondresponse = requests.request("GET", newrequesturl, headers=SecondReqheaders, data=Nullpayload)

            #Creating a wav file with the response content and posting the response on discord 
            with open(FileName, 'wb') as file:
                #Saving the response as a wav file
                file.write(secondresponse.content)
            
                #Setting the name of the bot depending on the character chosen
                #await client.user.edit(username=Character_info['Phrases'][CharacterIndex]['Character'])

                #Text to be entered with file \/  file being specified \/
                await message.channel.send('Test',file=discord.File(FileName))             

                #Debug checking status code of response (403 may mean there will need to be a change to the request)
                #await message.channel.send(response.status_code)
        
            #Removing the file after use
            os.remove(FileName)

    except Exception as inst:
        print('15.ai response error! (Respone error)')
        print(inst)

        #Checking if 3 bad responses have been made and erroring as such
        if RequestTries >= 3:
            await message.channel.send('Something went wrong with making a call to 15.ai!')
        else:
            #Waiting 10 seconds and sending the request again
            await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
            TempRequestTries = RequestTries + 1
            print(TempRequestTries)
            asyncio.create_task(Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))          

#Function to make a request to the 15.ai api and play the output in a voice chat
async def VC_Make15APIRequest(MessageText,CharacterIndex,message,RequestTries,FileName):   
    print(Character_info['Phrases'][CharacterIndex]['Character'] + " says: " +MessageText)
    
    #Variable to store POST content to use within the request
    data = '{"text":"%s","character":"%s","emotion":"%s"}' % (MessageText+".", Character_info['Phrases'][CharacterIndex]['Character'], Character_info['Phrases'][CharacterIndex]['Emotion'])
    
    #Debug print that shows the data section (makes sure the correct string is passed)
    print(data)
    try:
        #Constructing the request, passing in the headers and the data 
        firstresponse = requests.post('https://api.15.ai/app/getAudioFile5', headers=FirstRequestHeaders, data=data)
        
        #Checking if the api responds with a 500/ server error message
        if firstresponse.status_code != 200:
            print('15.ai response error!')

            #Checking if 3 bad responses have been made and erroring as such
            if RequestTries >= 3:
                await message.channel.send('Something went wrong with making the first call to 15.ai!')
            else:
                #Showing the status code of the respomse
                print(firstresponse.status_code)
                #Waiting 10 seconds and sending the request again
                await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
                TempRequestTries = RequestTries + 1
                print(TempRequestTries)
                asyncio.create_task(VC_Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))
        else:
            #Parsing the json from the first request's response
            fifteenaijsontext = json.loads(firstresponse.text)
            
            #Selecting the generated wav file name
            wavfilelocation = fifteenaijsontext['wavNames'][0]

            #Creating a URL based on the output of the past request
            newrequesturl = "https://cdn.15.ai/audio/" + wavfilelocation
           
            #Making the second request to get the generated wav file
            secondresponse = requests.request("GET", newrequesturl, headers=SecondReqheaders, data=Nullpayload)

            #Creating a wav file with the response content and posting the response on discord 
            with open(FileName, 'wb') as file:
                #Saving the response as a wav file
                file.write(secondresponse.content)

                #Getting the voice clients currently in use
                for vc in client.voice_clients:
                    #Checking if the voice client channel is the same as the users' current voice channel
                    if vc.guild == message.guild:
                        #Playing the wav file via ffmpeg in the voice channel
                        vc.play(discord.FFmpegPCMAudio(executable=Token_info['ffmpeg_location'], source=FileName))    

            await asyncio.sleep(10)  
            os.remove(FileName)
    
    except Exception as inst:
        print('15.ai response error! (Respone error)')

        #Checking if 3 bad responses have been made and erroring as such
        print(inst)
        if RequestTries >= 3:
            await message.channel.send('Something went wrong with making a call to 15.ai!')
        else:
            #Waiting 10 seconds and sending the request again
            await asyncio.sleep(10) #https://stackoverflow.com/questions/42279675/synchronous-sleep-into-asyncio-coroutine#:~:text=then%20your_sync_function%20is%20running%20in%20a%20separate%20thread,,into%20the%20janus%20library.%20More%20tips%20on%20this:
            TempRequestTries = RequestTries + 1
            print(TempRequestTries)
            asyncio.create_task(VC_Make15APIRequest(MessageText,CharacterIndex,message,TempRequestTries,FileName))          

#Function that makes a GET request to the Wikipedia API and then using the parsed text within a POST request to 15.ai
async def MakeWikiRequest(GivenPrompt,message,ObjectIndex):
    #https://realpython.com/python-requests/#:~:text=%20Python%E2%80%99s%20Requests%20Library%20%28Guide%29%20%201%20Getting,values%20through%20query%20string%20parameters%20in...%20More%20
    #Variable to hold wiki request
    WikiRequestString = 'https://en.wikipedia.org/api/rest_v1/page/summary/'+GivenPrompt
    #Making GET request using the above variable
    WikiRequest = requests.get(WikiRequestString)
    #Checking if the request responds OK and erroring if it doesn't
    if WikiRequest.status_code != 200:
        print('Other API call error!')
        await message.channel.send('Something went wrong with making a call to the Wiki API!')
    else:          
        #Parsing the JSON returned and either outputting an error "if nothing comes back for that search" or using the parsed string within a call to 15.ai
        try:
            WikiExtract = WikiRequest.json()['extract']
            asyncio.create_task(HandleMessageLength(WikiExtract,ObjectIndex,message))
        except Exception as inst:
            print(inst)
            await message.channel.send('Something went wrong with parsing the Custom API!')

#Function that handles how many requests to the 15.ai api need to be made
async def HandleMessageLength(GivenText,ObjectIndex,message):
    GivenText = await CleanStrings(GivenText)
    current_date = datetime.datetime.now()    
    FileName = Token_info['SingleAudiofilepath'] + 'TempAudio' + str(current_date.microsecond) + '.wav'   
    #Checking if the text is above 200 characters (15.ai character limit)
    if len(GivenText) <= 198:
        #Making a single request to 15.ai
        asyncio.create_task(Make15APIRequest(GivenText,ObjectIndex,message,0,FileName))
    else:
        #Character "Chunk" number
        n = 198
        # Using list comprehension to split the string into 73 chharacter "chunks" (https://pythonexamples.org/python-split-string-into-specific-length-chunks/)
        out = [(GivenText[i:i+n]) for i in range(0, len(GivenText), n)]
        
        #Declaring a list to hold the temporary file names
        filenames = []
        
        #Creating the temporary file names using the milisecond that the file name is created (ish)
        for substring in out:
            #Waiting a smol amount of time to make sure that the same milisecond isn't used
            await asyncio.sleep(0.001)
            current_date = datetime.datetime.now()         
            FileName = Token_info['SingleAudiofilepath'] + 'TempAudio' + str(current_date.microsecond) + '.wav'
            filenames.append(FileName)
            #print(FileName)
        
        #Creating an index to call the temporary file names
        stringindex = 0
        for Substring in out:
            asyncio.create_task(Make15APIRequest(Substring,ObjectIndex,message,0,filenames[stringindex]))
            #print(filenames[stringindex])
            stringindex = stringindex + 1

#Function that handles how many requests to the 15.ai api need to be made
async def VC_HandleMessageLength(GivenText,ObjectIndex,message):
    GivenText = await CleanStrings(GivenText)
    #print(GivenText)
    current_date = datetime.datetime.now()
    FileName = Token_info['SingleAudiofilepath'] + 'TempAudio' + str(current_date.microsecond) + '.wav'   
    #Checking if the text is above 200 characters (15.ai character limit)
    if len(GivenText) <= 198:
        #Making a single request to 15.ai
        asyncio.create_task(VC_Make15APIRequest(GivenText,ObjectIndex,message,0,FileName))
    else:
        #Character "Chunk" number
        n = 198
        # Using list comprehension to split the string into 73 chharacter "chunks" (https://pythonexamples.org/python-split-string-into-specific-length-chunks/)
        out = [(GivenText[i:i+n]) for i in range(0, len(GivenText), n)]
        
        #Declaring a list to hold the temporary file names
        filenames = []
        
        #Creating the temporary file names using the milisecond that the file name is created (ish)
        for substring in out:
            #Waiting a smol amount of time to make sure that the same milisecond isn't used
            await asyncio.sleep(0.001)
            current_date = datetime.datetime.now()         
            FileName = Token_info['SingleAudiofilepath'] + 'TempAudio' + str(current_date.microsecond) + '.wav'
            filenames.append(FileName)
            #print(FileName)
        
        #Creating an index to call the temporary file names
        stringindex = 0
        for Substring in out:
            asyncio.create_task(VC_Make15APIRequest(Substring,ObjectIndex,message,0,filenames[stringindex]))
            stringindex = stringindex + 1

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
                print('POST Attempt')
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
                xmlstring = CustomAPIRequest.text
                response = fromstring(xmlstring.encode('utf-8'))
                xmlextract = response.xpath(CustomAPI_info['APIs'][CustomAPIIndex]['XMLPath']).pop()
                CustomAPIExtract = xmlextract.text                
                #Calling the fucntion to use the parsed string in a request to 15.ai
                asyncio.create_task(HandleMessageLength(CustomAPIExtract,ObjectIndex,message))
            except Exception as inst:
                #Showing error in console/ letting the user know that there was an error
                print(inst)
                await message.channel.send('Something went wrong with parsing the Custom API!')

#Function to remove non ASCII characters, special characters and converts numbers to words
async def CleanStrings(string_nonASCII):
    #Making the given string encoded in ascii  
    string_encode = string_nonASCII.encode("ascii", "ignore") # https://pythonguides.com/remove-unicode-characters-in-python/#:~:text=In%20python,%20to%20remove%20non-ASCII%20characters%20in%20python,,a%20string%20without%20ASCII%20character%20use%20string.decode().%20Example:
    string_decode = string_encode.decode()
    
    #Searching within the given string for integers that are in sequence (123)
    for x in reversed(range(1, 20)):
        #Creatinga regex string to find a interger sequence that would match [0-9]{Ranged amount}
        x = re.findall(r"[0-9]{"+str(x)+ r"}", string_decode)
        #Looping through each found occurance
        for foundint in x:
            #Creating the replacement string
            replacemntstring = num2words(int(foundint))

            #Replacing the interger with the word(s)
            regex =r"" +foundint+ r""
            replaced_string = re.sub(regex, replacemntstring, string_decode)

            #Setting the main string to the converted string 
            string_decode = replaced_string

    #Removing special characters
    string_decode = re.sub(r"[^a-zA-Z0-9\.\,\s\?\!]+", '', string_decode) # https://stackoverflow.com/questions/43358857/how-to-remove-special-characters-except-space-from-a-file-in-python

    return string_decode

#Running the script through the bot
client.run(Token_info['token'])
