import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot)

@slash.slash(name="test",
             description="This is just a test command, nothing more.",
             options=[
               create_option(
                 name="optone",
                 description="This is the first option we have.",
                 option_type=3,
                 required=False
               )
             ])
async def test(ctx, optone: str):
  await ctx.send(content=f"I got you, you said {optone}!")

bot.run("ODIxNDM1NzExODMxODAxODU2.YFDrnw.la8G5wac2NYpR5YX9EnimbGo5cg")