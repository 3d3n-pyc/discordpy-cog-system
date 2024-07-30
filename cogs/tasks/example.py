from discord.ext import tasks, commands

import modules.log as log


class Example(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop(minutes=1)
    async def TASK_NAME(self):
        file = __file__.split('\\')[-1][:-3]
        log.write(file, "Task Example handled", log.levels.debug)
    
    @commands.Cog.listener()
    async def on_ready(self):
        Example(self.bot).TASK_NAME.start()


async def setup(bot: commands.Bot) -> None:
    if bot.is_ready():
        Example(bot).TASK_NAME.start()
    else:
        await bot.add_cog(
            Example(bot)
        )