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
//using System.Text.Json;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Text;
using System.Collections.Specialized;
using System.Web;

namespace DiscordBot1
{

    public class Request
    {
        //ew ew ew ew ew ew ew                                                   \/
        //Should be something else but I forget what it should be :thonk:
        //Currently 4 by 13
        //hey x say y
        public string[,] Characterinfo =  {
        {"GLaDOS","hey glados, say" , "0", "Neutral"},
        {"Twilight Sparkle","hey twi, say" , "0", "Neutral"},{"Twilight Sparkle","hey purps, say" , "0", "Neutral"},{"Twilight Sparkle","hey twilight, say" , "0", "Neutral"},{"Twilight Sparkle","hey twiggles, say" , "0", "Neutral"},{"Twilight Sparkle","hey twiggle piggle, say", "0", "Neutral"},
        {"Twilight Sparkle","hey twi, happily say" , "0", "Happy"},{"Twilight Sparkle","hey purps, happily say" , "0", "Happy"},{"Twilight Sparkle","hey twilight, happily say" , "0", "Happy"},{"Twilight Sparkle","hey twiggles, happily say" , "0", "Happy"},{"Twilight Sparkle","hey twiggle piggle, happily say", "0", "Happy"},
        {"Wheatley","hey wheatley, say" , "0", "Neutral"},
        {"The Narrator","hey narrator, say" , "0", "Neutral"},
        {"Tenth Doctor","hey doc, say" , "0", "Neutral"},{"Tenth Doctor","hey doctor, say" , "0", "Neutral"},
        {"Soldier","hey soldier, say" , "0", "Neutral"},{"Soldier","hey soli, say" , "0", "Neutral"},
        {"Sans","hey sans, say" , "0", "Neutral"},
        {"Fluttershy","hey fluttershy, say" , "0", "Neutral"},{"Fluttershy","hey shy, say" , "0", "Neutral"},{"Fluttershy","hey flutters, say" , "0", "Neutral"},{"Fluttershy","hey flutterbutter, say" , "0", "Neutral"},{"Fluttershy","hey fluttershush, say" , "0", "Neutral"},{"Fluttershy","hey butter shush, say", "0", "Neutral"},{"Fluttershy","hey flutter butter, say" , "0", "Neutral"},{"Fluttershy","hey flutter shush, say" , "0", "Neutral"},{"Fluttershy","hey butter shush, say", "0", "Neutral"},
        {"Rarity","hey rarity, say" , "0", "Neutral"},{"Rarity","hey darling, say" , "0", "Neutral"},{"Rarity","hey white ranger, say" , "0", "Neutral"},
        {"Applejack","hey applejack, say" , "0", "Neutral"},{"Applejack","hey apples, say" , "0", "Neutral"},{"Applejack","hey applez, say" , "0", "Neutral"},{"Applejack","hey jackapple, say" , "0", "Neutral"},{"Applejack","hey aj, say", "0", "Neutral"},
        {"Rainbow Dash","hey rainbow dash, say" , "0", "Neutral"},{"Rainbow Dash","hey dash, say" , "0", "Neutral"},{"Rainbow Dash","hey dashie, say" , "0", "Neutral"},{"Rainbow Dash","hey rd, say" , "0", "Neutral"},
        {"Pinkie Pie","hey pinkie pie, say" , "0", "Neutral"},{"Pinkie Pie","hey pinkie, say" , "0", "Neutral"},{"Pinkie Pie","hey ponka pie, say" , "0", "Neutral"},{"Pinkie Pie","hey pinker ponk, say", "0", "Neutral"},
        {"Announcer","announcer! say","0","Neutral"},
        /*{"Princess Celestia","hey princess celestia, say" , "0", "Neutral"},{"Princess Celestia","hey princess, say" , "0", "Neutral"},{"Princess Celestia","hey sunbutt, say" , "0", "Neutral"},{"Princess Celestia","hey sun butt, say" , "0", "Neutral"},{"Princess Celestia","hey tia, say" , "0", "Neutral"} ,{"Princess Celestia","tia, say", "0", "Neutral"},*/
        //"Tell me about"
        {"GlaDOS","hey glados, tell me about", "1", "Neutral"},
        {"Twilight Sparkle","hey twi, tell me about", "1", "Neutral"},{"Twilight Sparkle","hey purps, tell me about", "1", "Neutral"},{"Twilight Sparkle","hey twilight, tell me about", "1", "Neutral"},{"Twilight Sparkle","hey twiggles, tell me about", "1", "Neutral"},{"Twilight Sparkle","hey twiggle piggle, tell me about", "1", "Neutral"},
        {"Twilight Sparkle","hey twi, happily tell me about", "1", "Happy"},{"Twilight Sparkle","hey purps, happily tell me about", "1", "Happy"},{"Twilight Sparkle","hey twilight, happily tell me about", "1", "Happy"},{"Twilight Sparkle","hey twiggles, happily tell me about", "1", "Happy"},{"Twilight Sparkle","hey twiggle piggle, happily tell me about", "1", "Happy"},
        {"Wheatley","hey wheatley, tell me about", "1", "Neutral"},
        {"The Narrator","hey narrator, tell me about", "1", "Neutral"},
        {"Tenth Doctor","hey doc, tell me about", "1", "Neutral"},{"Tenth Doctor","hey doctor, tell me about", "1", "Neutral"},
        {"Soldier","hey soldier, tell me about", "1", "Neutral"},{"Soldier","hey soli, tell me about", "1", "Neutral"},
        {"Sans","hey sans, tell me about", "1", "Neutral"},
        {"Fluttershy","hey fluttershy, tell me about", "1", "Neutral"},{"Fluttershy","hey shy, tell me about", "1", "Neutral"},{"Fluttershy","hey flutters, tell me about", "1", "Neutral"},{"Fluttershy","hey flutterbutter, tell me about", "1", "Neutral"},{"Fluttershy","hey fluttershush, tell me about", "1", "Neutral"},{"Fluttershy","hey butter shush, tell me about", "1", "Neutral"},{"Fluttershy","hey flutter butter, tell me about", "1", "Neutral"},{"Fluttershy","hey flutter shush, tell me about", "1", "Neutral"},{"Fluttershy","hey butter shush, tell me about", "1", "Neutral"},
        {"Rarity","hey rarity, tell me about", "1", "Neutral"},{"Rarity","hey darling, tell me about", "1", "Neutral"},{"Rarity","hey white ranger, tell me about", "1", "Neutral"},
        {"Applejack","hey applejack, tell me about", "1", "Neutral"},{"Applejack","hey apples, tell me about", "1", "Neutral"},{"Applejack","hey applez, tell me about", "1", "Neutral"},{"Applejack","hey jackapple, tell me about", "1", "Neutral"},{"Applejack","hey aj, tell me about", "1", "Neutral"},
        {"Rainbow Dash","hey rainbow dash, tell me about", "1", "Neutral"},{"Rainbow Dash","hey dash, tell me about", "1", "Neutral"},{"Rainbow Dash","hey dashie, tell me about", "1", "Neutral"},{"Rainbow Dash","hey rd, tell me about", "1", "Neutral"},
        {"Pinkie Pie","hey pinkie pie, tell me about", "1", "Neutral"},{"Pinkie Pie","hey pinkie, tell me about", "1", "Neutral"},{"Pinkie Pie","hey ponka pie, tell me about", "1", "Neutral"},{"Pinkie Pie","hey pinker ponk, tell me about", "1", "Neutral"}        
        /*{"Princess Celestia","hey princess celestia, tell me about", "1", "Neutral"},{"Princess Celestia","hey princess, tell me about", "1", "Neutral"},{"Princess Celestia","hey sunbutt, tell me about", "1", "Neutral"},{"Princess Celestia","hey sun butt, tell me about", "1", "Neutral"},{"Princess Celestia","hey tia, tell me about", "1", "Neutral"},{"Princess Celestia","tia, tell me about", "1", "Neutral"}*/
        };

        //Making a request and responding accordingly
        public static async Task MakerequestAsync(string position, bool multi, string character, string basemessage, SocketMessage message, string emotion)
        {
            //Declaring handler
            var handler = new HttpClientHandler();

            //Keeping just in case the wavs are zipped with gzip n' co
            //handler.AutomaticDecompression = ~DecompressionMethods.None;


            using (var httpClient = new HttpClient(handler))
            {
                using (var request = new HttpRequestMessage(new HttpMethod("POST"), "https://api.fifteen.ai/app/getAudioFile"))
                {
                    //request.Headers.TryAddWithoutValidation("user-agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36");
                    request.Headers.TryAddWithoutValidation("user-agent", "FifteenCLI");
                    request.Content = new StringContent("{\"text\":\"" + basemessage + "\",\"character\":\"" + character + "\" ,\"emotion\":\"" + emotion + "\"}");
                    request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json;charset=UTF-8");
                    var response = await httpClient.SendAsync(request);

                    if (response.StatusCode.ToString() != "OK")
                    {
                        //Responding to error msg given
                        Console.WriteLine(response.StatusCode.ToString());

                        //Waiting 10 seconds (There are better methods of waiting ik but a 1 liner suits me for now)
                        Console.WriteLine("Will send again");
                        Thread.Sleep(10000);

                        //Sending the request again
                        Console.WriteLine("Sending");
                        _ = MakerequestAsync(position,multi, character, basemessage, message,emotion);

                    }
                    else
                    {
                        if (multi == false)
                        {
                            //Responding with OK
                            Console.WriteLine(response.StatusCode.ToString());

                            //Storing locally and posting from local because reasons (will be set to variable to suit > 75 char strings given)
                            byte[] data = await response.Content.ReadAsByteArrayAsync();
                            System.IO.File.WriteAllBytes("C:\\Users\\Tom\\Documents\\Projectz\\AI API\\test.wav", data);
                            await message.Channel.SendFileAsync("C:\\Users\\Tom\\Documents\\Projectz\\AI API\\test.wav", "Test");
                        }
                        else
                        {
                            //Responding with OK
                            Console.WriteLine(response.StatusCode.ToString());
                            //Storing locally and posting from local because reasons (will be set to variable to suit > 75 char strings given)
                            byte[] data = await response.Content.ReadAsByteArrayAsync();
                            System.IO.File.WriteAllBytes("C:\\Users\\Tom\\Documents\\Projectz\\AI API\\test"+position+".wav", data);
                            //await message.Channel.SendFileAsync("C:\\Users\\Tom\\Documents\\Projectz\\AI API\\test.wav", "Test");
                        }
                    }
                }
            }
        }


        public static async Task MultirequestAsync(List<string> messagelist,string character)
        {
            /*
            using (WebClient client = new WebClient())
            {
                client.Headers.Add("application/json;charset=UTF-8");
                client.Headers.Add("user - agent", "FifteenCLI");
                client.

            }*/
            /*
            int position = 0;
            foreach (string i in messagelist)
            {
                string address = "https://api.fifteen.ai/app/getAudioFile";
                ///string data = "{\"text\":\"" + i + "\",\"character\":\"" + character + "\"}";
                //NameValueCollection qscoll = HttpUtility.ParseQueryString(data);
                //WebClient client = new WebClient();
                // Optionally specify an encoding for uploading and downloading strings.
                //client.Encoding = System.Text.Encoding.UTF8;
                // Upload the data.
                //string reply = client.UploadString(address, data);
                // Display the server's response.
                //Console.WriteLine(reply);

                // Create web client simulating IE6.
                using (WebClient client = new WebClient())
                {
                    client.Headers["User-Agent"] ="Mozilla/4.0 (Compatible; Windows NT 5.1; MSIE 6.0)";
                    client.QueryString = 
                    // Download data.
                    byte[] arr = client.DownloadData("http://www.dotnetperls.com/");

                    // Write values.
                    Console.WriteLine("--- WebClient result ---");
                    Console.WriteLine(arr.Length);
                }

            }*/
        }

    }

    class Program
    {     
        //Discord stuff (shamelessly robbed from https://github.com/gngrninja/csharpi/tree/intro)
        private readonly DiscordSocketClient _client;
        private readonly IConfiguration _config;

        //Starting the program
        static void Main(string[] args)
        {
            new Program().MainAsync().GetAwaiter().GetResult();
        }

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

        public async Task MainAsync()
        {
            //This is where we get the Token value from the configuration file           
            await _client.LoginAsync(TokenType.Bot, _config["Token"]);
            await _client.StartAsync();

            // Block the program until it is closed.
            await Task.Delay(-1);
        }

        private Task LogAsync(LogMessage log)
        {
            Console.WriteLine(log.ToString());
            return Task.CompletedTask;
        }

        private Task ReadyAsync()
        {
            Console.WriteLine($"Connected");
            return Task.CompletedTask;
        }

        private List<string> Splitbasestring(string basemessage)
        {
            List<string> messagelist = new List<string>();
            int chunkSize = 73;
            int stringLength = basemessage.Length;
            for (int i = 0; i < stringLength; i += chunkSize)
            {
                if (i + chunkSize > stringLength) chunkSize = stringLength - i;
                Console.WriteLine(basemessage.Substring(i, chunkSize));
                messagelist.Add(basemessage.Substring(i, chunkSize) + ".");
            }
            return messagelist;
        }


        private async Task<string> RequestAsync(string basemessage)
        {         
            //Declaring handler
            var handler = new HttpClientHandler();

            //Keeping just in case the wavs are zipped with gzip n' co
            //handler.AutomaticDecompression = ~DecompressionMethods.None;


            using (var httpClient = new HttpClient(handler))
            {
                using (var request = new HttpRequestMessage(new HttpMethod("GET"), "https://mashape-community-urban-dictionary.p.rapidapi.com/define?term="+basemessage))
                {
                    //request.Headers.TryAddWithoutValidation("user-agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36");
                    //request.Headers.TryAddWithoutValidation("user-agent", "FifteenCLI");  
                    request.Headers.TryAddWithoutValidation("x-rapidapi-host", "mashape-community-urban-dictionary.p.rapidapi.com");
                    request.Headers.TryAddWithoutValidation("x-rapidapi-key", _config["rapidapikey"]);

                    var response = await httpClient.SendAsync(request);

                    if (response.StatusCode.ToString() != "OK")
                    {
                        //Responding to error msg given
                        Console.WriteLine(response.StatusCode.ToString());

                        //Waiting 10 seconds (There are better methods of waiting ik but a 1 liner suits me for now)
                        Console.WriteLine("Will send again");
                        Thread.Sleep(10000);

                        //Sending the request again
                        Console.WriteLine("Sending");
                        return await RequestAsync(basemessage);
                    }
                    else
                    {
                        //                       
                        string responsejsonstring = await response.Content.ReadAsStringAsync();
                        //Console.WriteLine(responsejsonstring);
                        JObject jo = JObject.Parse(responsejsonstring);
                        string responseparsedjson = (string)jo.SelectToken("list[0].definition");
                        //Console.WriteLine(responseparsedjson);
                        string cleanresponseparsedjson = responseparsedjson.Replace("[","");
                        // Console.WriteLine(cleanresponseparsedjson);
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace("]", "");
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace("/", "");
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace("\\", "");
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace(":", "");
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace("\n", "");
                        cleanresponseparsedjson = cleanresponseparsedjson.Replace("\r", "");
                        //Console.WriteLine(cleanresponseparsedjson);
                        return cleanresponseparsedjson;
                    }
                }
            }
        }

       
        //There's a better way of handling this as highlighted in the git repo but eh 
        private async Task MessageReceivedAsync(SocketMessage message)
        {
            //Calling mah class
            Request requestclass = new Request();

            //This the bot doesn't respond to itself
            if (message.Author.Id == _client.CurrentUser.Id)
                return;        
        

            //Spaz tier method of extracting and acting on message given
            for (int i = 0; i < 87;i++)
            {
                //Checking the message if it fits
                if (message.Content.Contains(requestclass.Characterinfo[i, 1]))
                {
                    //Checking (Response type e.g hey x say y or tell me about, that meant to return wiki paragraph sections)
                    if (requestclass.Characterinfo[i,2] == "0")
                    {                     
                        //Stripping string of "hey x, say" and adding a . (all requests need it/ is the reason on the fifteen.ai/app page the counter goes to 1 instead of 0)
                        //In addition, for some reason simply using "substring(x,y) + "." "isn't liked by this
                        string parsedmessage = requestclass.Characterinfo[i, 1] + " ";
                        string basemessage = message.Content.Replace(parsedmessage,"");
                        basemessage = basemessage + ".";

                        if (basemessage.Length <= 75)
                        {                          
                            //Making the request and showing it in console
                            Console.WriteLine(requestclass.Characterinfo[i, 0] + " says : " + basemessage);
                            _ = Request.MakerequestAsync("",false,requestclass.Characterinfo[i, 0], basemessage, message, requestclass.Characterinfo[i, 3]);
                        }
                        else
                        {
                            await message.Channel.SendMessageAsync("Just a minute");
                            List<string> messagelist = Splitbasestring(basemessage);                            
                            for (int j = 0; j < messagelist.Count;j++)
                            {
                                Console.WriteLine(requestclass.Characterinfo[i, 0] + " says : " + messagelist[j]);
                                _ = Request.MakerequestAsync(j.ToString(),true, requestclass.Characterinfo[i, 0], messagelist[j]+".", message, requestclass.Characterinfo[i, 3]);                              
                            }
                            Thread.Sleep(60000);
                            for (int j = 0; j < messagelist.Count; j++)
                            {
                                await message.Channel.SendFileAsync("C:\\Users\\Tom\\Documents\\Projectz\\AI API\\test"+j.ToString()+".wav", "Test");
                            }
                        }
                                           
                        //Debug message to be uncommented if needed
                        //await message.Channel.SendMessageAsync(requestclass.Characterinfo[i, 0] + "  " + requestclass.Characterinfo[i, 1] + "  " + requestclass.Characterinfo[i, 2]);                     
                    }
                    else if (requestclass.Characterinfo[i,2] == "1")
                    {
                        //Message sent to wiki then responded with x saying the paragraph in the wiki (may need to look into further parsing however as some things may not be as precise with what I want)    
                        string parsedmessage = requestclass.Characterinfo[i, 1] + " ";
                        string basemessage = message.Content.Replace(parsedmessage, "");
                        basemessage = message.Content.Replace(" ", "%20");
                        basemessage = basemessage + ".";
                        string respondedstring = await RequestAsync(basemessage);
                        Thread.Sleep(3000);

                        if (respondedstring.Length <= 75)
                        {
                            //Making the request and showing it in console
                            Console.WriteLine(requestclass.Characterinfo[i, 0] + " says : " + respondedstring);
                            _ = Request.MakerequestAsync("", false, requestclass.Characterinfo[i, 0], respondedstring, message, requestclass.Characterinfo[i,3]);
                        }
                        else
                        {
                            await message.Channel.SendMessageAsync("Just a minute");
                            List<string> messagelist = Splitbasestring(respondedstring);
                            _ = Request.MultirequestAsync(messagelist, requestclass.Characterinfo[i, 0]);                       

                        }
                    }
                }
            }
        }
    }
}