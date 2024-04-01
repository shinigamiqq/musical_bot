import discord
from discord.ext import commands
import requests
import json
import youtube_dl
import openai
import os
import asyncio
import random
import yt_dlp


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

openai.api_key = 'ENTER_YOUR_OPENAI_TOKEN'
model_engine = "text-davinci-003"

@bot.command()
async def chat(ctx, *, message):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    reply = response.choices[0].text

    await ctx.send(reply)

@bot.command(name='play', help='Command is used to playing videos(youtube, twitch, etc): !play <url>')
async def play(ctx, url):
    await ctx.send("Track is playing. 🎵")
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '96',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options))
        while voice_client.is_playing():
            await asyncio.sleep(1)

        await ctx.send("Track finished playing. 🎵")

@bot.command(name='stop', help='Command is used to stop playing and exit from voice chat: !stop')
async def stop(ctx):
    voice_channel = ctx.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await ctx.send('Bye bye! 🧏🏼‍♂️ 🤫')
        await voice.disconnect()

@bot.command(name='pause', help='Command is used to pause playing in voice chat: !pause')
async def pause(ctx):
    voice_client = ctx.voice_client
    voice_client.pause()
    await ctx.send("Track paused.")

@bot.command(name='resume', help='Command is used to resume playing in voice chat: !resume')
async def resume(ctx):
    voice_client = ctx.voice_client
    voice_client.resume()
    await ctx.send("Track resumed.")


@bot.command(name='search', help='Command is used to search video to play on YouTube: !search <name>')
async def search(ctx, *urlq):
    query = ' '.join(urlq)
    await ctx.send("Track is playing. 🎵")
    yt_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '96',
        }],
        'default_search': 'auto',
        'noplaylist': True,
        'verbose': True
    }
    yt_search = yt_dlp.YoutubeDL(yt_opts)
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: yt_search.extract_info(url=query, download=False))
    if 'entries' in data:
        data = data['entries'][0]       
        data1 = [data['title'], data['url']]
        data2 = data['webpage_url']
        data3 = data['thumbnail']
    else:
        data1 = [data['title'], data['url']]
        data2 = [data['webpage_url']]
        data3 = [data['thumbnail']]
    
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(data1[1]))
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await ctx.send("Track finished playing. 🎵")
    return data1, data2, data3

@bot.command(name='image', help='Command is used to find images: !image cat')
async def image(ctx, query):
    url = f'https://api.unsplash.com/search/photos?query={query}&client_id=P8ClmW7M-LPsSEfXarr8obXBuTLXQBhInzyaqYTl6wE'
    response = requests.get(url)
    data = response.json()
    image_url = data['results'][0]['urls']['regular']
    await ctx.send(image_url)

@bot.event
async def member_join(member):
    welcome_channel = member.guild.get_channel(1153004665726832702)
    welcome_message = f'🤖\nWelcome home, {member.mention}!!!'

    await welcome_channel.send(welcome_message)

@bot.event
async def member_leave(member):
    channel = member.guilt.get_channel(1153004665726832702)
    await channel.send(f'🤖\n{member.display_name} покинул сервер((.')

@bot.command(name='server', help='Command is used to get information about server: !server')
async def server(ctx):
    server = ctx.guild
    await ctx.send(f'Server name: {server.name}\nУчастников на сервере: {server.member_count}')

@bot.command(name='info', help='Command is used to find information about user: !info <user_name>')
async def info(ctx, member: discord.Member):
    user_info = f"Name: {member.name}\nNickname: {member.display_name}\nПрисоединился: {member.joined_at}"
    await ctx.send(f"🤖\n{user_info}")


@bot.command(name='weather', help='Command is used to find information about weather: !weather London')
async def weather(ctx, city):
    api_key = 'aaad98b4785f5ff183037d5decbd4ce3'
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'main' in data:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            
            await ctx.send(f'🤖\nWeather in {city}: Temperature {temperature}°C, {description}')
        else:
            await ctx.send('Information is not found.')

    except Exception as e:
        await ctx.send(f'Error: {str(e)}')



class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", colour=discord.Colour.gold())
        for command in self.context.bot.commands:
            embed.add_field(name=f"{command.name}", value=command.help, inline=False)
        await self.get_destination().send(embed=embed)
        
    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help to: {command.qualified_name}", description=command.help, colour=discord.Colour.gold())
        await self.get_destination().send(embed=embed)
        
bot.help_command = MyHelp()


bot.run('ENTER_YOUR_TOKEN')
