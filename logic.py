
import aiohttp # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}' # İstek için URL API
        async with aiohttp.ClientSession() as session: # HTTP oturumu açma
            async with session.get(url) as response: # GET isteği gönderme
                if response.status == 200:
                    data = await response.json() # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name'] # Pokémon adını döndürme
                else:
                    return "Pikachu" # İstek başarısız olursa varsayılan adı döndürür

        if not self.name:
            self.name = await self.get_name() # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}" # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}' # İstek için URL API
        async with aiohttp.ClientSession() as session: # HTTP oturumu açma
            async with session.get(url) as response: # GET isteği gönderme
                if response.status == 200:
                    data = await response.json() # JSON yanıtının alınması ve çözümlenmesi
                    return data['sprites']['front_default'] # Pokémon resminin URL'sini döndürme
                else:
                    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" # İstek başarısız olursa varsayılan resim URL'sini döndürür
                
    async def pokemon_type(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}' # İstek için URL API
        async with aiohttp.ClientSession() as session: # HTTP oturumu açma
            async with session.get(url) as response: # GET isteği gönderme
                if response.status == 200:
                    data = await response.json() # JSON yanıtının alınması ve çözümlenmesi
                    return data['types'][0]['type']['name'] # Pokémon türünü döndürme
                else:
                    return "electric" # İstek başarısız olursa varsayılan türünü döndürür
