import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
import aiohttp
from datetime import datetime, timedelta
from discord import message

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokemon görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokemon oluşturdunuz.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("Pokémon sahibi değilsiniz!")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        # logic.py'deki feed metodunu çağırıyoruz
        result = await pokemon.feed()
        await ctx.send(result)
    else:
        await ctx.send("Henüz bir Pokémon'unuz yok! Önce !go komutu ile bir Pokémon edinin.")

bot.run(token)