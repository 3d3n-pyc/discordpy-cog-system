import discord
from discord import app_commands
from discord.ext import commands

import modules.log as log


class ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name = "ping", description = "Obtenir le ping du bot")
    async def ping(
        self,
        interaction: discord.Interaction
    ) -> None:
        latency = round(self.bot.latency * 1000)
            
        color = 0x2ECC71 if latency < 200 else 0xE67E22
        embed = discord.Embed(title=f'**Le ping du bot est de `{latency}`ms.**', colour=color)
        await interaction.response.send_message(embed=embed)
        
    @ping.error
    async def ping_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        file = __file__.split('\\')[-1][:-3]
        log.write(file, f"Error while getting bot's ping", log.levels.error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        ping(bot)
    )