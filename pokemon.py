import logging
from mcp.server.fastmcp import FastMCP 
import aiopoke
import sys

# --- CORREÇÃO: MOVER BASICCONFIG PARA CIMA ---
# Configure o logging PRIMEIRO
logging.basicConfig(
    level=logging.INFO, 
    stream=sys.stderr, 
    format='[POKEMON_SERVER] %(levelname)s - %(message)s'
)

# --- AGORA ADICIONE AS LINHAS DE DEBUG ---
import mcp.shared.version
import mcp.types
logging.info(f"--------------------------------------------")
logging.info(f"--- [DEBUG] VERSÕES DO SDK DO SERVIDOR ---")
logging.info(f"  LATEST_PROTOCOL_VERSION (mcp.types): {mcp.types.LATEST_PROTOCOL_VERSION}")
logging.info(f"  DEFAULT_NEGOTIATED_VERSION (mcp.types): {mcp.types.DEFAULT_NEGOTIATED_VERSION}")
logging.info(f"  SUPPORTED_PROTOCOL_VERSIONS (mcp.shared.version): {mcp.shared.version.SUPPORTED_PROTOCOL_VERSIONS}")
logging.info(f"--------------------------------------------")
# --- FIM DAS LINHAS ADICIONADAS ---


# E a inicialização:
mcp = FastMCP("pokemon-server")

def format_pokemon_info(pokemon_info: aiopoke.Pokemon) -> str:
    """Format Pokemon information into a readable string."""
    
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
    

@mcp.tool()
async def get_pokemon_info(pokemon_name:str=None, pokedex_number:int = None) -> str:
    """Get information about a Pokemon by name or pokedex number.
    Args:
        pokemon_name: Name of the Pokemon
        pokedex_number: Pokedex number of the Pokemon"""
    if not pokemon_name and not pokedex_number:
        logging.info(f"No valid parameters provided, please provide a pokemon name or pokedex number. ")
        return "No valid parameters provided, please provide a pokemon name or pokedex number."
    search_param = pokemon_name if pokemon_name else pokedex_number
    client = aiopoke.AiopokeClient()
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