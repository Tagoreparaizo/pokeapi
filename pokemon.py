import logging
from mcp.server.fastmcp import FastMCP 
import aiopoke
import sys

# --- CORREÇÃO: MOVER BASICCONFIG PARA CIMA ---
# Configure o logging PRIMEIRO
logging.basicConfig(
    level=logging.INFO, 
    format='[POKEMON_SERVER] %(levelname)s - %(message)s'
)




# E a inicialização:
mcp = FastMCP("pokemon-server")

def format_pokemon_info(pokemon_info: aiopoke.Pokemon) -> str:
    """Format Pokemon information into a readable string."""
    
    abilities_list = [getattr(getattr(ability, 'ability', None), 'name', 'N/A').capitalize() for ability in pokemon_info.abilities]
    abilities = " or ".join(abilities_list)

    types_list = [getattr(getattr(type_obj, 'type', None), 'name', 'N/A').capitalize() for type_obj in pokemon_info.types]
    types = " and ".join(types_list)
    
    stats_list = [f"{getattr(getattr(stat_obj, 'stat', None), 'name', 'N/A').capitalize()}: {getattr(stat_obj, 'base_stat', 'N/A')}" for stat_obj in pokemon_info.stats]
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
    if (pokemon_name is None and pokedex_number is None) or \
       (pokemon_name is not None and pokedex_number is not None):
        logging.info(f"Please provide either a pokemon name OR a pokedex number, but not both. ")
        raise ValueError("Please provide either a pokemon name OR a pokedex number, but not both.")
    search_param = pokemon_name if pokemon_name else pokedex_number
    async with aiopoke.AiopokeClient() as client:
        pokemon_info = await client.get_pokemon(search_param)
    if not pokemon_info:
        logging.info(f"Pokemon {search_param} not found.")
        return f"Pokemon {search_param} not found."
    return format_pokemon_info(pokemon_info)
def main():
    logging.info("Iniciando servidor em modo HTTP (streamable-http)...")
    mcp.run(
        transport="streamable-http"  # <--- ESSENCIAL
    )

if __name__ == "__main__":
    main()