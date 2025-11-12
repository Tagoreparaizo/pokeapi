import asyncio
import aiopoke
# Formatando o logging para STDERR (seguro para MCP
def format_pokemon_info(pokemon_info: aiopoke.Pokemon) -> str:
    """Format Pokemon information into a readable string."""
    # Para obter uma lista limpa com os nomes das habilidades:
    abilities_list = [ability.ability.name.capitalize() for ability in pokemon_info.abilities]
    abilities = " or ".join(abilities_list)

    types_list = [type.type.name.capitalize() for type in pokemon_info.types]
    types = " and ".join(types_list)
    
    stats_list = [f"{stat.stat.name.capitalize()}: {stat.base_stat}" for stat in pokemon_info.stats]
    return f"""
Pokedex: #{pokemon_info.id}
Name: {pokemon_info.name.capitalize()}
Abilities: {abilities}
Types: {types}
Stats: {', '.join(stats_list)}
Sprites: {pokemon_info.sprites.front_default}
Sprites (Shiny): {pokemon_info.sprites.front_shiny}
"""
async def main():
    client = aiopoke.AiopokeClient()

    pokemon = await client.get_pokemon("bidoof")
    print(format_pokemon_info(pokemon))
    await client.close()


asyncio.run(main())
