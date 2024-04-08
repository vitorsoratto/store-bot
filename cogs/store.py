import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from ui.store.store_creation import StoreCreationView


class Store(commands.Cog, name="loja"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="loja",
        description="Comandos relacionados a loja.",
    )
    async def loja(self, context: Context) -> None:
        """
        Manage the server's store.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Por favor especifique um subcomando.\n\n**Subcomandos:**\n`create` - Cria uma loja.\n`remove` - Remove uma loja.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @loja.command(
        name="create",
        description="Cria uma loja.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        channel="Canal onde a loja será criada.",
    )
    async def create(
            self,
            context: Context,
            channel: discord.TextChannel,
    ) -> None:
        """
        Esse comando cria uma loja em um determinado canal.

        :param context: Contexto da aplicação.
        :param channel: Canal onde a loja será criada.
        :param title: Título da loja.
        """
        view = await StoreCreationView.items(self.bot)
        await channel.send("Bem-vindo a loja!", view=view)


async def setup(bot) -> None:
    await bot.add_cog(Store(bot))
