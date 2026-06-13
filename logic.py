import aiohttp
import random
from random import randint
from datetime import datetime, timedelta
from discord.ext import commands

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.last_feed_time = datetime.now()
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"""Pokémon ismi: {self.name}
                Pokémon gücü: {self.power}
                Pokémon sağlığı: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
    
    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon sağlığı geri yüklendi. Mevcut sağlık: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            return f"Pokémonunuzu henüz besleyemezsiniz. Bir sonraki besleme zamanı: {next_feed_time.strftime('%H:%M:%S')}"

class Wizard(Pokemon):
    # Bu sınıfta, Sihirbaz sınıfına özgü metotlar  ve özellikler ekleyebiliriz
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"