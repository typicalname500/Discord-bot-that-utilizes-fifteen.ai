//###################################################################################
//#Using the brilliant API that I could only hope to call my own
//#>>>>>>>>>>>>>>>>>>>>>https://fifteen.ai/<<<<<<<<<<<<<<<<<<<<<
//###################################################################################
//Using the NodeJS discord bot template from: https://github.com/zfbx/Discord-Bot-Template

//Declaring configurations/ 
const config = require('./config.json');
const CharacterConfig = require('./characters.json');
const CustomAPIConfig = require('./CustomAPIConfig.json');
const Discord = require('discord.js');
const util = require('util');
const { Console } = require('console');
const bot = new Discord.Client({
    disableEveryone: true,
    disabledEvents: ['TYPING_START']
});

bot.on("ready", () => {
    bot.user.setGame('Awesome Fun Game'); //you can set a default game
    console.log(`Bot is online!\n${bot.users.size} users, in ${bot.guilds.size} servers connected.`);
});

bot.on("guildCreate", guild => {
    console.log(`I've joined the guild ${guild.name} (${guild.id}), owned by ${guild.owner.user.username} (${guild.owner.user.id}).`);
});

bot.on("message", async message => { 

    if(message.author.bot || message.system) return; // Ignore bots
    
    if(message.channel.type === 'dm') { // Direct Message
        return; //Optionally handle direct messages
    } 

    //console.log(message.content); // Log chat to console for debugging/testing
    
    var CharacterObjectIndex = 0;
    var CharacterObjectFound = false;
    for(var CharacterObject in CharacterConfig.Phrases)
    {
        if(message.content === CharacterObject.Phrase)
        {
            Console.log(CharacterObject.Function);
        }
        CharacterObjectIndex ++;
    }
    
    
    if(message.content === "hi")
    {
        message.channel.send(`Hi there ${message.author.toString()}`);
    }
    
    return;
});

// Catch Errors before they crash the app.
process.on('uncaughtException', (err) => {
    const errorMsg = err.stack.replace(new RegExp(`${__dirname}/`, 'g'), './');
    console.error('Uncaught Exception: ', errorMsg);
    // process.exit(1); //Eh, should be fine, but maybe handle this?
});

process.on('unhandledRejection', err => {
    console.error('Uncaught Promise Error: ', err);
    // process.exit(1); //Eh, should be fine, but maybe handle this?
});

bot.login(config.token);