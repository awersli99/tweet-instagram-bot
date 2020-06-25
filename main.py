from discord.ext import commands
import discord
import os
import imgkit
import time
import requests

BASEDIR = os.path.dirname(os.path.realpath(__file__))
USERDIR = os.getcwd()

def generate_tweet(name, username, body, pfp):
    with open(BASEDIR + "/tweet_template/template.html", "r") as file:
        data = file.read()
        data = data.replace("_BASEDIR_", BASEDIR)
        data = data.replace("_name_", name)
        data = data.replace("_pfp_", pfp)
        data = data.replace("_username_", username)
        data = data.replace("_body_", body)
        data = data.replace("_time_", time.strftime("%I:%M %p"))
        data = data.replace("_date_", time.strftime("%d %B %Y"))
    options = {"format": "png", "width": 640}
    imgkit.from_string(data, USERDIR + "/tweet.png", options = options)

def generate_insta(name, body, pfp, image):
    with open(BASEDIR + "/insta_template/template.html", "r") as file:
        data = file.read()
        data = data.replace("_BASEDIR_", BASEDIR)
        data = data.replace("_image_", image)
        data = data.replace("_name_", name)
        data = data.replace("_pfp_", pfp)
        data = data.replace("_body_", body)
        data = data.replace("_date_", time.strftime("%d %B"))
    options = {"format": "png", "width": 640}
    imgkit.from_string(data, USERDIR + "/insta.png", options = options)

prefix = "?"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("bot running")
    bot.remove_command('help')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("?tweet"))

@bot.command()
async def tweet(ctx, *args):
    if args == ():
        await ctx.message.channel.send("Usage: ?tweet 'text'")
    else:
        avatarurl = str(ctx.message.author.avatar_url).replace("webp?size=1024", "png?size=1024")
        await ctx.message.delete()
        print(str(args))
        tweetcontent = ""
        for i in args:
            tweetcontent += " " + i
        generate_tweet(ctx.message.author.display_name, ctx.message.author.name, tweetcontent[1:], avatarurl)
        await ctx.message.channel.send(file=discord.File(USERDIR + "/tweet.png"))

@bot.command()
async def insta(ctx, *args):
    if args == ():
        await ctx.message.channel.send("Usage: ?insta 'image link' 'caption'")
    else:
        avatarurl = str(ctx.message.author.avatar_url).replace("webp?size=1024", "png?size=1024")
        await ctx.message.delete()
        print(str(args))
        tweetcontent = ""
        image = args[0]
        for i in args[1:]:
            tweetcontent += " " + i
        generate_insta(ctx.message.author.display_name, tweetcontent[1:], avatarurl, image)
        await ctx.message.channel.send(file=discord.File(USERDIR + "/insta.png"))

bot.run("INSERT BOT TOKEN HERE", bot=True)  # Where 'TOKEN' is your bot token




