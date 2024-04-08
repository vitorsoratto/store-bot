import discord
from discord import app_commands, embeds
from discord.ext import commands
from discord.ext.commands import Context


class Item(commands.Cog, name="item"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="item",
        description="Comandos relacionados aos itens.",
    )
    async def item(self, context: Context) -> None:
        """
        Manage the server's items.

        :param context: The hybrid command context.
        """
        # TODO: Implement the item subcommand warning.
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Por favor especifique um subcomando.\n\n**Subcomandos:**\n`create` - Cria uma loja.\n`remove` - Remove uma loja.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
    @item.command(
        name="add",
        description="Cria um item.",
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(
        name="Nome do item.",
        description="Descrição do item.",
        price="Preço do item.",
        stock="Estoque do item.",
    )
    async def create(
            self, context: Context, name: str, description: str, price: float, stock: int,
        ) -> None:
        """
        Esse comando cria uma loja em um determinado canal.

        :param context: Contexto da aplicação.
        :param name: Nome do item.
        :param description: Descrição do item.
        :param price: Preço do item.
        :param stock: Estoque do item.
        """

        await self.bot.database.add_item(name, description, price, stock)
        embed = embeds.Embed(title="Produto adicionado com sucesso!", description=f"O produto {name} foi adicionado com sucesso!", color=0x009933)
        await context.send(embed=embed)

    @item.command(
        name="update",
        description="Atualiza o estoque de um item.",
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(
        item_id="ID do item.",
        stock="Estoque do item.",
    )
    async def update(
            self, context: Context, item_id: int, stock: int,
        ) -> None:
        """
        Esse comando atualiza o estoque de um item.

        :param context: Contexto da aplicação.
        :param item_id: ID do item.
        :param stock: Estoque do item.
        """

        await self.bot.database.update_item_stock(item_id, stock)
        embed = embeds.Embed(title="Estoque atualizado com sucesso!", description=f"O estoque do item {item_id} foi atualizado com sucesso!", color=0x009933)
        await context.send(embed=embed)

    @item.command(
        name="get",
        description="Pega um item.",
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(
        item_id="ID do item.",
    )
    async def get(
            self, context: Context, item_id: int,
        ) -> None:
        """
        Esse comando pega um item.

        :param context: Contexto da aplicação.
        :param item_id: ID do item.
        """

        item = await self.bot.database.get_item(item_id)
        embed = embeds.Embed(title="Item encontrado com sucesso!", description=f"O item {item_id} foi encontrado com sucesso!", color=0x009933)
        embed.add_field(name="ID", value=f"{item[0]}", inline=False)
        embed.add_field(name="Nome", value=f"{item[1]}", inline=False)
        embed.add_field(name="Descrição", value=f"{item[2]}", inline=False)
        embed.add_field(name="Preço", value=f"{item[3]}", inline=False)
        embed.add_field(name="Estoque", value=f"{item[4]}", inline=False)
        await context.send(embed=embed)

    @item.command(
        name="listall",
        description="Lista todos os itens.",
    )
    @commands.has_permissions(administrator=True)
    async def listall(
            self, context: Context,
        ) -> None:
        """
        Esse comando lista todos os itens.

        :param context: Contexto da aplicação.
        """

        items = await self.bot.database.get_items()
        embed = embeds.Embed(title="Itens cadastrados!", description=f"Items cadastrados no servidor.", color=0x009933)
        if len(items) == 0:
            embed.add_field(name="Nenhum item encontrado.", value="Nenhum item foi encontrado.", inline=False)
        else:
            for item in items:
                price_string = f"R$ {item[3]:.2f}"
                embed.add_field(name="---------------------------------", value="", inline=False)
                embed.add_field(name="ID", value=f"{item[0]}", inline=False)
                embed.add_field(name="Nome", value=f"{item[1]}", inline=False)
                embed.add_field(name="Descrição", value=f"{item[2]}", inline=False)
                embed.add_field(name="Preço", value=f"{item[3]}", inline=False)
                embed.add_field(name="Estoque", value=price_string, inline=False)

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Item(bot))
