import discord 
from discord.ext import commands
import modules
import nacl
from database import db_controller 
from model_1 import first_impression as initial_ChatLog

controller = db_controller.db_controller();

anger_level = 0;
sadness_level = 2;
fear_level = 0;
joy_level = 1;
surprise_level = 0;
love_level = 0;

angerSong = "";
sadnessSong = "moonlight sonata";
fearSong = "";
joySong = "Mozart - Sonata No.3"
surpriseSong = "";
loveSong = "Fur elise";

customization_level = 0;

#Function to request resonse from model1(GPT-3) and send it on discord
async def send_message(message, user_message, is_private):
    try:
        result = modules.get_response_with_sentiment(str(message.author) ,user_message)
        response_and_sentiment = result[0];
        sentiments_array = result[1];
        
        await check_customization(sentiments_array, message);
        
        #finalMsg = str(response) + " (" + str(sentiment) + ")";
        await message.author.send(response_and_sentiment) if is_private else await message.channel.send(response_and_sentiment);
        
    except Exception as e:
        print(e);
        
async def check_customization(sentiment_array, message):
    if max(sentiment_array) > 0.5:
        sentiment = ['anger','sadness','fear','joy','surprise','love'][sentiment_array.index(max(sentiment_array))];
    else:
        sentiment = 'neutral';
        
    print(sentiment, joy_level, sentiment_array[3]);

    if anger_level > 0 and sentiment == 'anger':
        if anger_level == 1:
            if sentiment_array[0] > 0.5:
                await message.channel.send("<@547905866255433758> play ", angerSong);
        elif anger_level == 2:
            if sentiment_array[0] > 0.7:
                await message.channel.send("<@547905866255433758> play ", angerSong);
        elif anger_level == 3:
            if sentiment_array[0] > 0.9:
                await message.channel.send("<@547905866255433758> play ", angerSong);
                
    if sadness_level > 0 and sentiment == 'sadness':
        if sadness_level == 1:
            str1 = "<@547905866255433758> play "+ sadnessSong
            if sentiment_array[1] > 0.5:
                await message.channel.send(str1);
        elif sadness_level == 2:
            if sentiment_array[1] > 0.7:
                await message.channel.send(str1);
        elif sadness_level == 3:
            if sentiment_array[1] > 0.9:
                await message.channel.send(str1);
                
    if fear_level > 0 and sentiment == 'fear':
        if fear_level == 1:
            if sentiment_array[2] > 0.5:
                await message.channel.send("<@547905866255433758> play ", fearSong);
        elif fear_level == 2:
            if sentiment_array[2] > 0.7:
                await message.channel.send("<@547905866255433758> play ", fearSong);
        elif fear_level == 3:
            if sentiment_array[2] > 0.9:
                await message.channel.send("<@547905866255433758> play ", fearSong);
                
    if joy_level > 0 and sentiment == 'joy':
        print("joy sentiment:", sentiment_array[3] );
        if joy_level == 1:
            str1 = "<@547905866255433758> play "+ joySong
            if sentiment_array[3] > 0.6:
                await message.channel.send(str1);
        elif joy_level == 2:
            if sentiment_array[3] > 0.7:
                await message.channel.send(str1);
        elif joy_level == 3:
            if sentiment_array[3] > 0.9:
                await message.channel.send(str1);
                
    if surprise_level > 0 and sentiment == 'surprise':
        if surprise_level == 1:
            str1 = "<@547905866255433758> play "+ surpriseSong
            if sentiment_array[3] > 0.5:
                await message.channel.send(str1);
        elif surprise_level == 2:
            if sentiment_array[3] > 0.7:
                await message.channel.send(str1);
        elif surprise_level == 3:
            if sentiment_array[3] > 0.9:
                await message.channel.send(str1);
                
    if love_level > 0 and sentiment == 'love':
        if love_level == 1:
            if sentiment_array[3] > 0.5:
                await message.channel.send("<@547905866255433758> play ", loveSong);
        elif love_level == 2:
            if sentiment_array[3] > 0.7:
                await message.channel.send("<@547905866255433758> play ", loveSong);
        elif love_level == 3:
            if sentiment_array[3] > 0.9:
                await message.channel.send("<@547905866255433758> play ", loveSong);
    
        
async def send_custome_message(message, user_message, client):
    print(len(user_message));

    if user_message[1:] == "#customize":
        await message.channel.send("You can customize my reaction to a certain level of emotions that you pick. You can customize:\n\n1- play a song after detecting a level of emotion [emotions: anger, sadness, fear, joy, surprise, love] [levels: 1, 2, 3] \n\t-------------------------------\n\tTo customize, type: !#1,  <emotion>,  <level>,  <song name>\n\tExample: !#1,  sad,  2,  Für Elise\n\t-------------------------------\n\n")# \nTo see the current level of a certain emotion, type: !#<emotion> \nExample: !#anger
    elif len(user_message) > 2 :
        if user_message[2] == '1':
            customization_level = 1;
            await message.channel.send("Customization level 1: SET!");
            customization_parameters = user_message.split(',');
            print("CP:",customization_parameters[2].strip());
            print("joy level:", int(customization_parameters[2].strip()))
            
            match  customization_parameters[1].strip():
                case 'anger':
                    anger_level = int(customization_parameters[2].strip());
                    angerSong = customization_parameters[3].strip();
                case 'sadness':
                    sadness_level = int(customization_parameters[2].strip());
                    sadnessSong = customization_parameters[3].strip();
                case 'fear':
                    fear_level = int(customization_parameters[2].strip());
                    fearSong = customization_parameters[3].strip();
                case 'joy':
                    joy_level = int(customization_parameters[2].strip());
                    joySong = customization_parameters[3].strip();
                case 'surprise':
                    surprise_level = int(customization_parameters[2].strip());
                    surpriseSong = customization_parameters[3].strip();
                case 'love':
                    love_level = int(customization_parameters[2].strip());
                    loveSong = customization_parameters[3].strip();
                    
            
        elif user_message[2] == '2':
            customization_level = 2;
            
            
        elif user_message[2] == '3':
            print("Hehew3");
            
            #channel = discord.utils.find(lambda x: x.name == 'General', message.guild.channels)
            #member = client.get_member({ message.author.id})
            #await member.move_to(channel);

            #await client.move_member(message.author, channel)
        else:
            await message.channel.send("You can customize:\n\n1- play a song after detecting a level of emotion [emotions: anger, sadness, fear, joy, surprise, love] [levels: 1, 2, 3] (exclusive to discord server)\n\t-------------------------------\n\tTo customize, type: !#1  <emotion>  <level>  <song name>\n\tExample: !#1  sad  2  Moonlight Sonata\n\t------------------------------- ")
    else:
        await message.channel.send("You can customize my reaction to a certain level of emotions that you pick. You can customize:\n\n1- play a song after detecting a level of emotion [emotions: anger, sadness, fear, joy, surprise, love] [levels: 1, 2, 3] (exclusive to discord server)\n\t-------------------------------\n\tTo customize, type: !#1,  <emotion>,  <level>,  <song name>\n\tExample: !#1,  sad,  2,  Moonlight Sonata\n\t------------------------------- ")# \nTo see the current level of a certain emotion, type: !#<emotion> \nExample: !#anger
            
        

def run_discord_bot():
    TOKEN = 'MTAzOTMyMDU5MDYzODY1MzQ3MQ.GYSpDb.Z52pyHT19qz3E5eeE1CzL8ojBDXwGJCqRJ2Sjg'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='§', intents=intents)
    #client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.command(pass_context = True)
    async def join(ctx):
        print("heheehehehehehwwww")
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            
        else:
            await ctx.send("You are not connected to a voice channel");
    
            
    @client.event
    async def on_message(message):
        await client.process_commands(message)
        username = str(message.author);
        user_message = str(message.content);
        channel = str(message.channel);
        print(username, channel);
        
        #if message from bot, break out of function
        if message.author == client.user:
                return 
        
        #if direct message
        if channel == "Direct Message with Unknown User":
            if(controller.select_user(username) == None):
                controller.insert_user(username); #add this new user in database
                controller.add_Chatlog(username, initial_ChatLog);#add initial_chatlog to his chatlog

            print(f'{username} said: "{user_message}" ({channel})')

            if user_message[1] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)
                
        #if message is on channel user has to send '!' before each sentence
        else:
            if user_message[0] == '!':
                if(controller.select_user(username) == None):
                    controller.insert_user(username); #add this new user in database
                    controller.add_Chatlog(username, initial_ChatLog,"neutral",0,0,0,0,0,0);#add initial_chatlog to his chatlog

                print(f'{username} said: "{user_message}" ({channel})')
                print(user_message)
                if user_message[1] == '#':
                    await send_custome_message(message, user_message, client);
                elif user_message[1] == '?':
                    user_message = user_message[1:]
                    await send_message(message, user_message, is_private=True)
                else:
                    await send_message(message, user_message, is_private=False)
    
    client.run(TOKEN)