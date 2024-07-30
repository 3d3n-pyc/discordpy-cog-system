import discord
from discord.ext import commands

import modules.log as log


class Message(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        
        file = __file__.split('\\')[-1][:-3]
        log.write(file, f"Message from {message.author.name} received", log.levels.info)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Message(bot)
    )