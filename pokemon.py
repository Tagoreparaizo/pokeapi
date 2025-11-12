import logging
logging.basicConfig(
    level=logging.INFO, 
    format='[POKEMON_SERVER] %(levelname)s - %(message)s'
)

from mcp.server.fastmcp import FastMCP 
import aiopoke

# E a inicialização:
mcp = FastMCP("pokemon-server")

def format_pokemon_info(pokemon_info: aiopoke.Pokemon) -> str:
    """Format Pokemon information into a readable string."""
    
    abilities_list = []
    for ability in pokemon_info.abilities:
        try:
            abilities_list.append(ability.ability.name.capitalize())
        except AttributeError:
            abilities_list.append('N/A')
    abilities = " or ".join(abilities_list)

    types_list = []
    for type_obj in pokemon_info.types:
        try:
            types_list.append(type_obj.type.name.capitalize())
        except AttributeError:
            types_list.append('N/A')
    types = " and ".join(types_list)
    
    stats_list = []
    for stat_obj in pokemon_info.stats:
        stat_name = 'N/A'
        base_stat = 'N/A'
        try:
            stat_name = stat_obj.stat.name.capitalize()
        except AttributeError:
            pass
        try:
            base_stat = stat_obj.base_stat
        except AttributeError:
            pass
        stats_list.append(f"{stat_name}: {base_stat}")
    return f"""
Pokedex: #{pokemon_info.id}
Name: {pokemon_info.name.capitalize()}
Abilities: {abilities}
Types: {types}
Stats: {', '.join(stats_list)}
Sprites: {pokemon_info.sprites.front_default if pokemon_info.sprites.front_default else "N/A"}
Sprites (Shiny): {pokemon_info.sprites.front_shiny if pokemon_info.sprites.front_shiny else "N/A"}
"""
    

@mcp.tool()
async def get_pokemon_info(pokemon_name:str=None, pokedex_number:int = None) -> str:
    """Get information about a Pokemon by name or pokedex number.
    Args:
        pokemon_name: Name of the Pokemon
        pokedex_number: Pokedex number of the Pokemon"""
    if pokemon_name is not None and pokedex_number is not None:
        raise ValueError("Please provide either a pokemon name OR a pokedex number, but not both.")
    if pokemon_name is None and pokedex_number is None:
        raise ValueError("Please provide either a pokemon name OR a pokedex number.")
    search_param = pokemon_name if pokemon_name else pokedex_number
    async with aiopoke.AiopokeClient() as client:
        pokemon_info = await client.get_pokemon(search_param)
    if not pokemon_info:
        logging.warning(f"Pokemon {search_param} not found.")
        raise ValueError(f"Pokemon {search_param} not found.")
    return format_pokemon_info(pokemon_info)

def main():
    logging.info("Iniciando servidor em modo HTTP (streamable-http)...")
    mcp.run(
        transport="streamable-http"  # <--- ESSENCIAL
    )

if __name__ == "__main__":
    main()