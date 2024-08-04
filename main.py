import discord
from discord.ext import commands

import os
import json; data = json.load(open('config.json', 'r'))
import asyncio
import modules.log as log

import sys
sys.dont_write_bytecode = True if data['PythonDontWriteBytecode'] else False

async def console():
    while True:
        response = await asyncio.to_thread(input)
        
        if response.startswith('load '):
            ext = response[5:]
            try:
                await bot.load_extension(ext)
                print(f'{ext} chargé')
            except Exception as e:
                print(e)
        elif response.startswith('unload '):
            ext = response[7:]
            try:
                await bot.unload_extension(ext)
                print(f'{ext} déchargé')
            except Exception as e:
                print(e)
        elif response.startswith('reload '):
            ext = response[7:]
            try:
                await bot.reload_extension(ext)
                print(f'{ext} rechargé')
            except Exception as e:
                print(e)


class client(commands.Bot):
    
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents = discord.Intents.all(),
            application_id = data["app_id"]
        )

        self.initial_extensions = []
        
        types = [dir for dir in os.listdir('cogs') if os.path.isdir(f'cogs/{dir}')]
        
        for type in types:
            for root, _, files in os.walk(f"cogs/{type}"):
                for file in files:
                    if file != '__pycache__' and file.endswith('.py'):
                        if root == f"cogs/{type}":
                            self.initial_extensions.append(f"cogs.{type}.{file[:-3]}")
                        else:
                            dir = os.path.basename(root)
                            self.initial_extensions.append(f"cogs.{type}.{dir}.{file[:-3]}")


    async def setup_hook(self):
        log.write('main', 'Mode débug activé', log.levels.debug)
        
        for ext in self.initial_extensions:
            await self.load_extension(ext)
            log.write('main', f'{ext} chargé', log.levels.debug)
        
        self.synced = await bot.tree.sync()
        
    async def on_ready(self):
        log.write('main', f'{self.user} est connecté avec {len(self.synced)} commande(s) synchronisée(s) sous la version {data["version"]}', log.levels.info)
        await asyncio.create_task(console())
    

bot = client(); bot.run(data["token"])
