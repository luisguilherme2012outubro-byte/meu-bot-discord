import os
import ast
import operator
import discord
from discord import app_commands

# =========================
# CONFIGURAÇÃO
# =========================

WELCOME_MESSAGE = """Bem vindo(a) ao Staaaaarrrr Park! Nesse incrível park de diversão você verá de tudo! Minigames, eventos, lutas, cargos e até mesmo canais de texto e de voz focados em Brawl Stars!

%#>&- se vir algo ^#%#%fora do comum, não *#<#entre em pânico<#& isso é normal >#&#&- isso é normal @&@ this is normal **×>*@ this is normal*!>@>"""

# =========================
# BOT
# =========================

class RT(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sincroniza os comandos / com o Discord
        await self.tree.sync()


bot = RT()


# =========================
# QUANDO O BOT LIGA
# =========================

@bot.event
async def on_ready():
    print(f" R-T está online como {bot.user}!")
    print(" R-T está observando")


# =========================
# /olá
# =========================

@bot.tree.command(
    name="olá",
    description="Welcome to Staaaaarrrr Park!"
)
async def ola(interaction: discord.Interaction):
    await interaction.response.send_message(WELCOME_MESSAGE)


# =========================
# /sou_novo
# =========================

@bot.tree.command(
    name="oque é o caminho de troféus?",
    description="Perguntar"
)
async def sou_novo(interaction: discord.Interaction):
    await interaction.response.send_message(
      "O caminho de troféus é onde você poderá acumular todos os seus valiosos troféus! Quanto mais troféus você tiver,mais recompensas você ganhará!")


# =========================
# /ajuda
# =========================

@bot.tree.command(
    name="ajuda",
    description="this is normal"
)
async def ajuda(interaction: discord.Interaction):
    await interaction.response.send_message(
        "No panic, this is normal"
    )


# =========================
# CALCULADORA SEGURA
# =========================

OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def calcular(expressao):
    arvore = ast.parse(expressao, mode="eval")

    def resolver(no):
        if isinstance(no, ast.Constant):
            if isinstance(no.value, (int, float)):
                return no.value
            raise ValueError("Número inválido.")

        if isinstance(no, ast.BinOp):
            operador = OPERADORES.get(type(no.op))

            if operador is None:
                raise ValueError("Operação não permitida.")

            esquerda = resolver(no.left)
            direita = resolver(no.right)

            # Evita contas absurdamente grandes
            if isinstance(no.op, ast.Pow) and abs(direita) > 10:
                raise ValueError("Expoente muito grande.")

            return operador(esquerda, direita)

        if isinstance(no, ast.UnaryOp):
            operador = OPERADORES.get(type(no.op))

            if operador is None:
                raise ValueError("Operação não permitida.")

            return operador(resolver(no.operand))

        raise ValueError("Expressão inválida.")

    return resolver(arvore.body)


# =========================
# /calcular
# =========================

@bot.tree.command(
    name="calcular",
    description="Resolve uma conta matemática."
)
@app_commands.describe(
    conta="Exemplo: 25 * 4 + 10"
)
async def calcular_comando(
    interaction: discord.Interaction,
    conta: str
):
    try:
        resultado = calcular(conta)

        await interaction.response.send_message(
            f" **Conta:** `{conta}`\n"
            f"**Resultado:** `{resultado}`"
        )

    except Exception:
        await interaction.response.send_message(
            "R-T olhou para essa conta...\n"
            "Não entendi. Tente algo como `25 * 4 + 10`."
        )


# =========================
# TOKEN
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN não foi configurado."
    )

bot.run(TOKEN)
