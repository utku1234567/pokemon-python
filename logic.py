import aiohttp
import random


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer

        chance = random.randint(1, 100)
        if chance <= 5:
            self.pokemon_number = random.randint(800, 1000)
            self.is_rare = True
        else:
            self.pokemon_number = random.randint(1, 500)
            self.is_rare = False

        # 🔥 Yeni özellikler
        self.level = 1
        self.xp = 0
        self.hunger = 100

        self.hp = random.randint(80, 120)
        self.power = random.randint(10, 20)

        # API verileri
        self.name = None
        self.height = None
        self.weight = None
        self.types = []
        self.abilities = []
        self.stats = {}
        self.sprite = None

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self

    async def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    self.name = data['name']
                    self.height = data['height']
                    self.weight = data['weight']

                    self.types = [t['type']['name'] for t in data['types']]
                    self.abilities = [a['ability']['name'] for a in data['abilities']]

                    self.stats = {
                        stat['stat']['name']: stat['base_stat']
                        for stat in data['stats']
                    }

                    self.sprite = data['sprites']['front_default']
                else:
                    self.name = "pikachu"
                    self.sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"

    # 🔥 GENEL SALDIRI
    def attack(self, other):
        damage = self.power
        other.hp -= damage
        return f"{self.name} {other.name}'e {damage} hasar verdi!"

    # 🔥 CAN YENİLEME
    def heal(self):
        self.hp += 20
        return f"{self.name} iyileşti! HP: {self.hp}"

    def feed(self):
        self.xp += 10
        self.hunger = min(100, self.hunger + 20)

        if self.xp >= self.level * 50:
            self.xp = 0
            self.level += 1
            self.hp += 10  # 🔥 level bonusu
            return f"{self.name} seviye atladı! Yeni level: {self.level}"

        return f"{self.name} beslendi! XP: {self.xp}"

    def get_attack(self):
        return self.stats.get("attack", 0)

    def info(self):
        return (
            f"İsim: {self.name}\n"
            f"Level: {self.level}\n"
            f"HP: {self.hp}\n"
            f"Güç: {self.power}\n"
            f"Nadir: {'Evet' if self.is_rare else 'Hayır'}\n"
            f"Türler: {', '.join(self.types)}\n"
        )


# 🔮 Sihirbaz sınıfı
class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp += 30  # daha fazla sağlık

    def attack(self, other):
        # kalkan şansı
        if random.random() < 0.3:
            return f"{self.name} sihirli kalkan açtı! Hasar almadı!"
        return super().attack(other)

    def info(self):
        base = super().info()
        return "Sihirbaz pokémonunuz var.\n" + base


# 🥊 Dövüşçü sınıfı
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += 10  # daha güçlü

    def attack(self, other):
        # kritik vurma
        if random.random() < 0.3:
            damage = self.power * 2
            other.hp -= damage
            return f"{self.name} KRİTİK vurdu! {damage} hasar!"
        return super().attack(other)

    def info(self):
        base = super().info()
        return "Dövüşçü pokémonunuz var.\n" + base