//###################################################################################
//#Using the brilliant API that I could only hope to call my own
//#>>>>>>>>>>>>>>>>https://fifteen.ai/<<<<<<<<<<<<<<<<<<<<
//###################################################################################

using System;
using Discord;
using Discord.Net;
using Discord.Commands;
using Discord.WebSocket;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Threading;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Linq;
using System.Collections.Generic;
using System.Net;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Text;
using System.Collections.Specialized;
using System.Web;
using System.Xml;

namespace DiscordBot1
{   
    //Class to hold functions/ tasks that 
    public class RequestFunctions
    {             
        //public string[,] Characterinfo;       
        public JObject Characterinfo = new JObject();

        //JObject to hold the custom API JSON values
        public JObject CustomAPIObject = new JObject();

        //Populating the CustomAPI JObject using the json file
        public JObject PopulateCustomAPIObject()
        {
            //Catching errors
            try
            {
                //JObject jo = JObject.Parse("");
                //JToken pathResult = jo.SelectToken("Phrases[0].Phrase");           
                string tempjsonfile = File.ReadAllText(AppContext.BaseDirectory + "CustomAPIConfig.json");
                JObject jo = JObject.Parse(tempjsonfile);
                return jo;
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error with returning Custom API information \n" + ex);
                return null;
            }
        }

        //List of a list of strings that holds JSON values using the character json file
        public JObject Populatecharacters()
        {
            //Catching errors
            try
            {
                //Creating a config variable to be referenced
                IConfiguration _config;
                var _builder = new ConfigurationBuilder()
                    .SetBasePath(AppContext.BaseDirectory)
                    .AddJsonFile(path: "config.json");
                _config = _builder.Build();

                //String that will become the json file
                string filelines = "";

                //Shamelessly creating a string that is just the json file that will be converted to a JSON object
                foreach (string line in File.ReadAllLines(_config["CharacterInfoFile"]))
                {
                    filelines = filelines + line + "\n";
                }

                //Making the file's most outter object into a JObject
                JObject o = JObject.Parse(filelines);               
                return o;
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error with returning character phrases information \n" + ex);
                return null;
            }
        }

        //Making a request and responding accordingly
        public static async Task MakerequestAsync(string position, string character, string basemessage, SocketMessage message, string emotion, string uncpath, int RequestTries,string UseDiagonal)
        {
            //Declaring handler
            var handler = new HttpClientHandler();

            //Keeping just in case the wavs are zipped with gzip n' co
            //handler.AutomaticDecompression = ~DecompressionMethods.None;

            //Catching errors
            try
            {
                //Creaing a HTTP client using the HTTP handler
                using (var httpClient = new HttpClient(handler))
                {
                    using (var request = new HttpRequestMessage(new HttpMethod("POST"), "https://api.15.ai/app/getAudioFile"))
                    {
                        //request.Headers.TryAddWithoutValidation("user-agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36");

                        //Setting headers/ POST content to use the API
                        request.Headers.TryAddWithoutValidation("user-agent", "FifteenCLI");
                        //Console.WriteLine("{\"text\":\"" + basemessage + "\",\"character\":\"" + character + "\" ,\"emotion\":\"" + emotion + "\" ,\"use_diagonal\":" + UseDiagonal + "}");
                        request.Content = new StringContent("{\"text\":\"" + basemessage + "\",\"character\":\"" + character + "\" ,\"emotion\":\"" + emotion + "\" ,\"use_diagonal\":"+ UseDiagonal + "}");
                        request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json;charset=UTF-8");
                        //Storing the response as a variable to be made into a byte array
                        var response = await httpClient.SendAsync(request);

                        //Checking if the request came back OK
                        if (response.StatusCode.ToString() != "OK")
                        {
                            //Responding to error msg given
                            Console.WriteLine(response.StatusCode.ToString());

                            //Either sending the message again or letting the user know that the request they made didn't work
                            if (RequestTries == 3)
                            {
                                await message.Channel.SendMessageAsync("Error! The API didn't respond!");
                            }
                            else
                            {
                                //Waiting 10 seconds (There are better methods of waiting ik but a 1 liner suits me for now)
                                Console.WriteLine("Will send again");
                                Thread.Sleep(10000);

                                //Sending the request again                      
                                Console.WriteLine("Sending");
                                RequestTries = RequestTries + 1;
                                Console.WriteLine(RequestTries);
                                _ = MakerequestAsync(position, character, basemessage, message, emotion, uncpath, RequestTries, UseDiagonal);
                            }
                        }
                        else
                        {
                            //Responding with OK
                            Console.WriteLine(response.StatusCode.ToString());

                            //Storing the audio file locally and posting the file as a message on Discord
                            byte[] data = await response.Content.ReadAsByteArrayAsync();
                            System.IO.File.WriteAllBytes(uncpath, data);
                            await message.Channel.SendFileAsync(uncpath, "Test");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error making request to 15.ai");
                await message.Channel.SendMessageAsync("Error! The 15.ai API didn't respond!");
            }
        }
    }

    //Main Class
    class Program
    {
        //Instantiating the message handling class
        static readonly RequestFunctions requestclass = new RequestFunctions();

        //Discord stuff (shamelessly robbed from https://github.com/gngrninja/csharpi/tree/intro)
        private readonly DiscordSocketClient _client;
        private readonly IConfiguration _config;

        //Starting the program
        static void Main(string[] args)
        {
            new Program().MainAsync().GetAwaiter().GetResult();
        }

        //Constructor that defines/ starts the bot's functions
        public Program()
        {          
            _client = new DiscordSocketClient();

            //Hook into log event and write it out to the console
            _client.Log += LogAsync;

            //Hook into the client ready event
            _client.Ready += ReadyAsync;

            //Hook into the message received event, this is how we handle the hello world example
            _client.MessageReceived += MessageReceivedAsync;

            //Setting config stuff including token
            var _builder = new ConfigurationBuilder()
                .SetBasePath(AppContext.BaseDirectory)
                .AddJsonFile(path: "config.json");
            _config = _builder.Build();         
            
        }

        //Task that logs in the bot user and starts the bots' functions
        public async Task MainAsync()
        {
            //Creating a list of string arrays to hold character data
            requestclass.Characterinfo = requestclass.Populatecharacters();
            
            //Creating a JObject to hold custom API data
            requestclass.CustomAPIObject = requestclass.PopulateCustomAPIObject();

            //Not continuing if an error occurs
            if (requestclass.Characterinfo == null || requestclass.CustomAPIObject == null)
            {
                Console.WriteLine("Error! The character/ custom API information returned an error!");
            }
            else
            {
                //This is where we get the Token value from the configuration file           
                await _client.LoginAsync(TokenType.Bot, _config["Token"]);
                await _client.StartAsync();

                // Block the program until it is closed.
                await Task.Delay(-1);
            }
        }

        //Task that returns Discord Logs
        private Task LogAsync(LogMessage log)
        {
            Console.WriteLine(log.ToString());
            return Task.CompletedTask;
        }

        //Displaying that the bot has connected to Discord
        private Task ReadyAsync()
        {
            Console.WriteLine($"Connected");
            return Task.CompletedTask;
        }

        //Function to break up a sting into a list of strings as the 15.ai requests have a character limit.
        private List<string> Splitbasestring(string basemessage)
        {
            List<string> messagelist = new List<string>();
            int chunkSize = 275;
            int stringLength = basemessage.Length;
            for (int i = 0; i < stringLength; i += chunkSize)
            {
                if (i + chunkSize > stringLength) chunkSize = stringLength - i;
                //Console.WriteLine(basemessage.Substring(i, chunkSize));
                messagelist.Add(basemessage.Substring(i, chunkSize) + ".");
            }
            return messagelist;
        }

        //Function to make a request to wikipedia's REST API and returning a text summary that will then be put through 15.ai's API
        private async Task<string> WikiRequestAsync(string basemessage)
        {
            try
            {
                //Declaring handler
                var handler = new HttpClientHandler();

                //Keeping just in case the wavs are zipped with gzip n' co
                //handler.AutomaticDecompression = ~DecompressionMethods.None;

                //Setting string to the wiki page's request + the text the user wanted to have the character tell them about
                string apirequest = "https://en.wikipedia.org/api/rest_v1/page/summary/" + basemessage;
                //Console.WriteLine(apirequest);        

                //Declaring HTTP clients to handle making GET requests
                using (var httpClient = new HttpClient(handler))
                {
                    using (var request = new HttpRequestMessage(new HttpMethod("GET"), apirequest))
                    {
                        //Console.WriteLine(request);
                        //Making the request to the API
                        var response = await httpClient.SendAsync(request);

                        //Checking if a 200 response is given
                        if (response.StatusCode.ToString() != "OK")
                        {
                            //Responding to error msg given
                            Console.WriteLine(response.StatusCode.ToString());

                            //Erroring immidiately to make sure not too much time is taken up                    
                            return null;
                        }
                        else
                        {
                            //Getting the response body, parsing the JSON within and making sure that it can be used in a 15.ai POST request 
                            string responsejsonstring = await response.Content.ReadAsStringAsync();
                            //Console.WriteLine(responsejsonstring);

                            //Making the content body into a JObject to be parsed from.
                            JObject jo = JObject.Parse(responsejsonstring);
                            string responseparsedjson = jo.GetValue("extract").ToString();
                            //Console.WriteLine(responseparsedjson);

                            //Removing any characters from the string that might break the call to 15.ai and sending the string to the API.
                            string cleanresponseparsedjson = CleanForAPI(responseparsedjson);
                            //Console.WriteLine(cleanresponseparsedjson);
                            return cleanresponseparsedjson;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error with Making a request to wikipedia!");
                return null;
            }
        }

        //There's a better way of handling this as highlighted in the git repo but eh 
        private async Task MessageReceivedAsync(SocketMessage message)
        {                
            //This makes sure that the bot doesn't respond to itself
            if (message.Author.Id == _client.CurrentUser.Id)
                return;

            int JSONIndex = 0;
            //Spaz tier method of extracting and acting on message given
            foreach (var i in requestclass.Characterinfo.SelectToken("Phrases"))
            {
                //Console.WriteLine((string)i.SelectToken("Phrase"));
                //Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases[" + JSONIndex + "].Phrase"));
                //Console.WriteLine(requestclass.Characterinfo[JSONIndex][0]);
                //Checking the message if it contains a command phrase
                if (message.Content.Contains((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Phrase")))
                {
                    //Displaying returned quote details
                    //Console.WriteLine(JSONIndex);
                    /*Console.WriteLine(requestclass.Characterinfo[JSONIndex][0]);
                    Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Character"));
                    Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Function"));
                    Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Emotionr"));*/

                    //Checking (Function type e.g hey 'x' say 'y' or 'x' tell me about, that meant to return wiki paragraph sections)
                    if ((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Function") == "0")
                    {
                        //Stripping string of "hey x, say" and adding a . (all requests need it/ is the reason on the fifteen.ai/app page the counter goes to 1 instead of 0)
                        string basemessage = ParsedString(JSONIndex, message);

                        //Making showing the text that is going to be sent along with the character saying it in the console
                        Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Character") + " says : " + basemessage + ".");

                        //basemessage = basemessage.Replace(" ", "%20");

                        //Adding a '.' at the end to 
                        basemessage += ".";

                        //Making the request using the string given
                        _ = HandleMessageLength(JSONIndex, basemessage, message);

                        //Debug message to be uncommented if needed
                        //await message.Channel.SendMessageAsync(requestclass.Characterinfo[i, 0] + "  " + requestclass.Characterinfo[i, 1] + "  " + requestclass.Characterinfo[i, 2]); 

                    }
                    else if ((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Function") == "1")
                    {
                        //Message sent to wiki then responded with x saying the paragraph in the wiki
                        string basemessage = ParsedString(JSONIndex, message);

                        //Making a request to an the wikipedia API and returning the short description text
                        string respondedstring = await WikiRequestAsync(basemessage);
                        Thread.Sleep(3000);
                        // Not continuing if there is an error
                        if (respondedstring == null)
                        {

                        }
                        else
                        {
                            Console.WriteLine((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Character") + " says : " + respondedstring);

                            //Checking if the response was OK and erroring as such
                            if (respondedstring == null)
                            {
                                await message.Channel.SendMessageAsync("Error! The wiki didn't respond!");
                            }
                            else
                            {
                                _ = HandleMessageLength(JSONIndex, respondedstring, message);
                            }
                        }
                    }
                    else if ((string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Function") == "2")
                    {
                        //Making a custom API call, using the character API reference
                        string temp = (string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].APIReference");
                        _ = HandleCustomAPICallInfo(JSONIndex, temp, message);
                        //Console.WriteLine(CustomAPIString);
                    }
                }
                JSONIndex++;
            }
        }

        //Removing the quote from the message string
        private string ParsedString(int JSONIndex, SocketMessage message)
        {
            string parsedmessage = (string)requestclass.Characterinfo.SelectToken("Phrases[" + JSONIndex + "].Phrase");
            string basemessage = message.Content.Replace(parsedmessage, "");
            return basemessage;
        }

        //Task that either makes a single request for text given that is under 75 charaters or makes multiple requests if the text is any larger
        private async Task HandleMessageLength(int JSONIndex, string basemessage, SocketMessage message)
        {
            //Checking if the message sent is over 275 characters to make sure either a single or multiple requests would be needed
            if (basemessage.Length <= 275)
            {
                //Setting audio file path that will be used to send the message containing an audio file to Discord.
                string uncpath = _config["SingleAudiofilepath"] + "test.wav";
                _ = RequestFunctions.MakerequestAsync("", (string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Character"), basemessage, message, (string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].Emotion"), uncpath,0, (string)requestclass.Characterinfo.SelectToken("Phrases["+JSONIndex+"].use_diagonal"));
            }
            else
            {
                //Letting the user know it will take around a minute to get a response. 
                await message.Channel.SendMessageAsync("Just a minute");

                //Creating a list of strings 75 characters long 
                List<string> messagelist = Splitbasestring(basemessage);

                //Going through each of the strings in the list and running them throuh the API.
                for (int j = 0; j < messagelist.Count; j++)
                {
                    //Showing what text and character is going to be entered into the API.
                    Console.WriteLine(requestclass.Characterinfo[JSONIndex][0] + " says : " + messagelist[j]);
                    
                    //Setting a string to a filename based on the Index in the loop.
                    string uncpath = _config["SingleAudiofilepath"] + "test" + j + ".wav";

                    //Starting the task that handles making requests to the API.
                    _ = RequestFunctions.MakerequestAsync("", (string)requestclass.Characterinfo.SelectToken("Phrases[" + JSONIndex + "].Character"), basemessage, message, (string)requestclass.Characterinfo.SelectToken("Phrases[" + JSONIndex + "].Emotion"), uncpath, 0, (string)requestclass.Characterinfo.SelectToken("Phrases[" + JSONIndex + "].use_diagonal"));
                }

                //Waiting a minute to ensure that all the requests have been passed through.
                Thread.Sleep(10000);
                Console.WriteLine("a");
                //Sending the audio file messages in order based on the Indexs in the loop.
                for (int j = 0; j < messagelist.Count; j++)
                {
                    await message.Channel.SendFileAsync(_config["SingleAudiofilepath"] + "test" + j.ToString() + ".wav", "Test");
                }
            }
        }

        //Handling the request information and passing it to the appropriate Tasks
        private async Task HandleCustomAPICallInfo(int CharacterJSONIndex, string CustomAPIRef, SocketMessage message)
        {
            /*JToken pathResult = o.SelectToken("Phrases[0].Phrase");
            string a = pathResult.ToString();
            Console.WriteLine(a);*/
            //JToken pathresult = jo.SelectToken("APIs.[0].BaseAPICall");
            //string responseparsedjson = pathresult.ToString();
            //Console.WriteLine(responseparsedjson);

            //Declaring JObject/ Tokens to hold custom API information
            JObject jo = requestclass.CustomAPIObject;
            JToken ObjectReferenceValue = null;
            JToken APICallValue = null;
            JToken JSONPathValue = null;
            JToken RequestTypeValue = null;
            JToken OutputTypeValue = null;
            JToken XMLPathValue = null;

            //Declaring variables to be used as a loop index/ boolean to break the loop when the 
            int JSONObjectIndex = 0;
            bool FoundAPI = false;

            //Looping through all the objects and, based on the object reference, pulling the data within that object
            do
            {
                //Console.WriteLine(x.Value.ToString());
                //JObject jo2 = JObject.Parse(x.Value.ToString());

                //Getting the object reference from the inner object
                ObjectReferenceValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].ObjectReference");
                //Console.WriteLine(ObjectReferenceValue.ToString());

                //Checking the object referenece against the object reference in the character object given
                if (ObjectReferenceValue.ToString() == CustomAPIRef)
                {
                    try
                    {
                        //Assigning the json values to the appropriats JSON tokens
                        RequestTypeValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].ReqType");
                        OutputTypeValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].OutputType");
                        JSONPathValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].JSONPath");
                        XMLPathValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].XMLPath");

                        //Assigning the API call value and either adding the message or just assigning the call by itself
                        string APICallstring = "";
                        APICallValue = jo.SelectToken("APIs.[" + JSONObjectIndex + "].BaseAPICall");
                        if (APICallValue.ToString().Contains("{0}"))
                        {
                            string basemessage = ParsedString(CharacterJSONIndex, message);
                            APICallstring = APICallValue.ToString().Replace("{0}", basemessage);
                        }
                        else
                        {
                            APICallstring = APICallValue.ToString();
                        }

                        //Checking what request type the API is going to be used
                        if (RequestTypeValue.ToString() == "GET")
                        {
                            await MakeGETCustomAPICall(CharacterJSONIndex, APICallstring, OutputTypeValue.ToString(), JSONPathValue.ToString(), XMLPathValue.ToString(), message);
                            FoundAPI = true;
                        }
                        else
                        {
                            FoundAPI = true;
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("Error handling custom API information " + ex);
                    }
                }
                //Incrementing the loop index
                JSONObjectIndex++;
            }
            while (FoundAPI != true && JSONObjectIndex >= jo.Count);
            
        }

        //Making a GET request and handling the output
        private async Task MakeGETCustomAPICall(int CharacterJSONIndex, string APICall, string OutputType, string JSONPath, string XMLPath, SocketMessage message)
        {
            try {
                //Declaring handler
                var handler = new HttpClientHandler();

                //Declaring HTTP clients to handle making GET requests 
                using (var httpClient = new HttpClient(handler))
                {
                    using (var request = new HttpRequestMessage(new HttpMethod("GET"), APICall))
                    {
                        //Console.WriteLine(request);

                        //Making the request to the API
                        var response = await httpClient.SendAsync(request);

                        //Checking if a 200 response is given
                        if (response.StatusCode.ToString() != "OK")
                        {
                            //Responding to error msg given
                            Console.WriteLine(response.StatusCode.ToString());

                            //Erroring immidiately to make sure not too much time is taken up                    
                            await message.Channel.SendMessageAsync("Error! The API didn't respond correctly!");

                        }
                        else
                        {
                            //Getting the response body, parsing the JSON within and making sure that it can be used in a 15.ai POST request 
                            string responsestring = await response.Content.ReadAsStringAsync();

                            //Checking what output format is and parsing accordingly.
                            if (OutputType == "JSON")
                            {
                                //Making the content body into a JObject to be parsed from.
                                //Console.WriteLine(responsejsonstring);
                                JObject jo = JObject.Parse(responsestring);
                                //string responseparsedjson = jo.GetValue("extract").ToString();

                                //Parsing the JToken from the JObject and pulling the string value from the token.
                                JToken pathResult = jo.SelectToken(JSONPath);
                                string responseparsedjson = pathResult.ToString();
                                //Console.WriteLine(responseparsedjson);

                                //Removing any characters from the string that might break the call to 15.ai and sending the string to the API.
                                string cleanresponseparsedjson = CleanForAPI(responseparsedjson);
                                Console.WriteLine(cleanresponseparsedjson);
                                await HandleMessageLength(CharacterJSONIndex, cleanresponseparsedjson, message);
                            }
                            else
                            {
                                //Links to sources used in order to read XML:                            
                                //https://stackoverflow.com/questions/1444809/extracting-an-xml-element-from-an-xml-file-using-xpath
                                //Browser extention to get XPath from page: https://microsoftedge.microsoft.com/addons/detail/xml-tree/oaejbeendohihffilopfgmgigfbgnknf?hl=en-GB

                                //Declaring an xml document and passing the response body into it
                                XmlDocument xmlDoc = new XmlDocument();
                                xmlDoc.LoadXml(responsestring);

                                //Selectnig a node using the given XML Xpath and retreiving its string value
                                XmlNode node = xmlDoc.SelectSingleNode(XMLPath);
                                string responseparsedXML = node.InnerText;
                                string cleanresponseparsedXML = CleanForAPI(responseparsedXML);
                                //Console.WriteLine(cleanresponseparsedXML);

                                //Sending the string to the 15.ai API
                                await HandleMessageLength(CharacterJSONIndex,cleanresponseparsedXML,message);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error with making a request to the custom API " + ex);
            }
        }
        
        //Function that cleans strings so that they can be passed to the 15.ai API
        private string CleanForAPI(string UncleanedText)
        { 
            //Removing all characters that can break the API calls
            string tempcleanresponseparsed = UncleanedText.Replace("[", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace("]", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace("/", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace("\\", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace(":", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace("\n", "");
            tempcleanresponseparsed = tempcleanresponseparsed.Replace("\r", "");
            return tempcleanresponseparsed;
        }


    }
}