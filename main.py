import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

# 🔹 Intent ayarları
intents = discord.Intents.default()
intents.message_content = True

# 🔹 Bot oluşturma (BU EN ÜSTTE OLMAK ZORUNDA)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')


# 🔹 Pokémon oluştur
@bot.command()
async def go(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:

        # 🔥 rastgele sınıf seç
        cls = random.choice([Pokemon, Wizard, Fighter])
        pokemon = cls(author)

        await pokemon.fetch_data()

        await ctx.send(pokemon.info())

        embed = discord.Embed()
        embed.set_image(url=pokemon.sprite)
        await ctx.send(embed=embed)

    else:
        await ctx.send("Zaten Pokémonun var!")


# 🔹 Besleme
@bot.command()
async def feed(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        await ctx.send("Önce Pokémon oluştur! (!go)")
        return

    pokemon = Pokemon.pokemons[author]
    result = pokemon.feed()

    await ctx.send(result)


# 🔹 Bilgi göster
@bot.command()
async def info(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        await ctx.send("Pokémonun yok!")
        return

    pokemon = Pokemon.pokemons[author]
    await ctx.send(pokemon.info())


# 🔹 İyileştirme
@bot.command()
async def heal(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        await ctx.send("Pokémonun yok!")
        return

    pokemon = Pokemon.pokemons[author]
    await ctx.send(pokemon.heal())

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz

bot.run(token)