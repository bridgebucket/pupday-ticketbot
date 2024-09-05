import discord, dotenv, os
from discord import application_command

dotenv.load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())


class puppy_tickets(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id="ticketing", 
                       placeholder="open a ticket",
                       min_values=1,
                       max_values=1,
                       options=[discord.SelectOption(label="Minecraft server", description="Is your ticket related to the Minecraft server?"),
                                discord.SelectOption(label="Discord server", description="Is your ticket related to this Discord server?")])
    async def select_callback(self, select, interaction):
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), 
                      interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, embed_links = True),
                      interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)}
        channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, reason=f"ticket for {interaction.user}")
        await interaction.response.send_message(f"created your ticket in {channel.mention}!!!!", ephemeral=True)
        if select.values[0] == "Minecraft server":
            await channel.send(f"sum1 will be here soon :3 in the meantime, you should send a message detailing what da issue wit the minecraft server is!!")
        elif select.values[0] == "Discord server":
            await channel.send(f"sum1 will be here soon :3 in the meantime, tell us what you think we could improve about the server!!!!")

@bot.command(description="start the ticket system")
@discord.default_permissions(administrator=True)
async def ticketing(ctx):
    embed = discord.Embed(title="have an issue?? create a ticket!",
                          description="select a category wit the dropdown menu 2 start ur ticket",
                          color=12884911)
    await ctx.respond("done :3", ephemeral=True)
    await ctx.send(embed=embed, view=puppy_tickets())

bot.persistent_views_added = False

@bot.event
async def on_ready():
    print(f"{bot.user} is FINALLY up and running")
    if not bot.persistent_views_added:
        bot.add_view(puppy_tickets())
        bot.persistent_views_added = True

bot.run(os.getenv('TOKEN'))