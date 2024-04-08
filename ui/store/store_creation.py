import discord
from discord import embeds, ui


class StoreCreation(ui.Select):
    def __init__(self, bot, opts) -> None:
        self.bot = bot
        self.opts = opts

        super().__init__(
            placeholder="Selecione um item",
            options=self.opts,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        user_choice = self.values[0]
        item = await self.bot.database.get_item(user_choice)

        embed = embeds.Embed(title='Kilzy Comunnity | Produto', color=0x009933)
        embed.add_field(name=f"🏷 | **Produto: {item.get('name')}**", value="", inline=False)
        embed.add_field(name=f"💵 | **Preço: __R${item.get('price')}__**", value="", inline=False)
        embed.add_field(name=f"📦 | **Estoque: __{item.get('stock')}__**", value="", inline=False)

        await interaction.response.edit_message(embed=embed, content=None, view=None)


class StoreCreationView(ui.View):
    def __init__(self, bot, options=None):
        loading_option = discord.SelectOption(label="Carregando...", description="Carregando...", value="0")
        self.bot = bot
        self.options = options or [loading_option]
        super().__init__()
        self.add_item(StoreCreation(bot, options))

    @classmethod
    async def items(cls, bot):
        items = await bot.database.get_items()

        options = [
            discord.SelectOption(
                label=item.get("name"),
                description=item.get('description'),
                value=item.get("id"),
            )
            for item in items
        ]
        self = cls(bot, options)
        return self
