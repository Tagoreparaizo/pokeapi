# Servidor MCP da PokeAPI

Um servidor construído com `FastMCP` que fornece informações sobre Pokémon usando a biblioteca `aiopoke`. Este projeto permite que você recupere facilmente informações detalhadas sobre Pokémon por nome ou número da Pokédex através de uma API estruturada.

## Funcionalidades

*   **Recuperação de Informações de Pokémon:** Busque detalhes abrangentes de qualquer Pokémon usando seu nome ou número da Pokédex.
*   **Saída Legível:** Formata os dados do Pokémon (habilidades, tipos, estatísticas, sprites) em uma string de fácil leitura.
*   **Integração com FastMCP:** Expõe a funcionalidade `get_pokemon_info` como uma ferramenta através de um servidor `FastMCP`, permitindo uma integração perfeita com outros serviços compatíveis com MCP.

## Instalação

Este projeto requer Python 3.12 ou superior.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Tagoreparaizo/pokeapi.git
    cd pokeapi
    ```
    (Nota: Substitua `<url_do_repositorio>` pela URL real se este projeto estiver hospedado em um repositório remoto.)

2.  **Instale as dependências:**
    Este projeto usa `uv` para gerenciamento de dependências. Se você não tiver o `uv` instalado, pode instalá-lo via `pip`:
    ```bash
    pip install uv
    ```
    Em seguida, instale as dependências do projeto:
    ```bash
    uv sync
    ```

## Uso

### Executando o Servidor

Para iniciar o servidor MCP da PokeAPI, execute o script `pokemon.py`:

```bash
python pokemon.py
```

O servidor será iniciado no modo HTTP (streamable-http), aguardando por requisições.

### Usando a Ferramenta `get_pokemon_info`

Quando o servidor estiver em execução, você pode interagir com ele usando um cliente MCP. O servidor expõe uma ferramenta chamada `get_pokemon_info`.

**Exemplo (uso conceitual com um cliente MCP):**

```python
import mcp

# Supondo que seu cliente MCP esteja configurado para se conectar ao 'pokemon-server'
client = mcp.Client("pokemon-server") 

# Obter informações pelo nome do Pokémon
dados_charmander = client.get_tool("get_pokemon_info")(pokemon_name="charmander")
print(dados_charmander)

# Obter informações pelo número da Pokédex
dados_pikachu = client.get_tool("get_pokemon_info")(pokedex_number=25)
print(dados_pikachu)
```

Isso retornará uma string formatada contendo o ID, nome, habilidades, tipos, estatísticas e URLs dos sprites do Pokémon.

## Dependências

*   [`mcp`](https://pypi.org/project/mcp/): O framework para construir o servidor MCP.
*   [`aiopoke`](https://pypi.org/project/aiopoke/): Um wrapper Python assíncrono para a PokeAPI.
