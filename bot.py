import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite
import asyncio
import random
import os
import aiohttp
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Einstellungen
DATABASE = os.path.join(os.path.dirname(__file__), 'squads.db')
SEND_PRIVATE_MESSAGE = False  # Optional: Private Nachrichten an Squad-Leader senden

# Intents einstellen
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.voice_states = True
intents.message_content = True

# Bot-Client initialisieren
bot = commands.Bot(command_prefix='!', intents=intents)

# Datenstrukturen zur Verwaltung der Squadleader
current_squad_leaders = {}

# Datenbank-Setup
async def setup_database():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                guild_id TEXT PRIMARY KEY,
                text_channel_id TEXT,
                api_domain TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS voice_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                channel_id TEXT UNIQUE,
                name TEXT
            )
        ''')
        await db.commit()

@bot.event
async def on_ready():
    await setup_database()
    print(f'Bot ist bereit als {bot.user}')

    # Hinzufügen des Cogs
    try:
        await bot.add_cog(SquadCommands(bot))
        print("SquadCommands Cog hinzugefügt.")
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Cogs: {e}")

    # Synchronisieren der Slash-Befehle
    try:
        synced = await bot.tree.sync()
        print(f'Synchronisierte {len(synced)} globale Slash-Befehle')
    except Exception as e:
        print(f'Fehler beim Synchronisieren der Slash-Befehle: {e}')

# Hilfsfunktionen
async def get_text_channel(guild_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute('SELECT text_channel_id FROM settings WHERE guild_id = ?', (str(guild_id),))
        row = await cursor.fetchone()
        if row and row[0]:
            return bot.get_channel(int(row[0]))
        else:
            return None  # Kein Textkanal gesetzt

async def get_api_domain(guild_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute('SELECT api_domain FROM settings WHERE guild_id = ?', (str(guild_id),))
        row = await cursor.fetchone()
        if row and row[0]:
            return row[0]
        else:
            return None  # Keine API-Domain gesetzt

async def get_voice_channels(guild_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute('SELECT channel_id, name FROM voice_channels WHERE guild_id = ?', (str(guild_id),))
        rows = await cursor.fetchall()
        return [{'channel_id': row[0], 'name': row[1]} for row in rows]

async def query_game_server(api_domain):
    url = f"{api_domain}/api/get_public_info"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('result', {})
                else:
                    print(f"Fehler bei der API-Abfrage: Status {response.status}")
                    return None
    except asyncio.TimeoutError:
        print("Die API-Abfrage hat zu lange gedauert (Timeout).")
        return None
    except aiohttp.ClientError as e:
        print(f"Fehler bei der API-Abfrage: {e}")
        return None

def get_member_voice_channel(member, voice_channels):
    voice_state = member.voice
    if not voice_state or not voice_state.channel:
        return None
    for channel in voice_channels:
        if str(channel['channel_id']) == str(voice_state.channel.id):
            return channel
    return None

async def assign_squad_leader(voice_channel, members):
    eligible_members = [m for m in members if not m.bot]
    if not eligible_members:
        return None
    return random.choice(eligible_members)

# Cog für Squad-Befehle
class SquadCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_text_channel", description="Setze den Textkanal für Squad-Befehle")
    @app_commands.describe(channel="Der Textkanal, der für Squad-Befehle verwendet werden soll")
    async def set_text_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        text_channel_id = str(channel.id)

        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('''
                INSERT INTO settings (guild_id, text_channel_id)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET text_channel_id=excluded.text_channel_id
            ''', (guild_id, text_channel_id))
            await db.commit()

        await interaction.response.send_message(f'Der Textkanal wurde auf {channel.mention} gesetzt.', ephemeral=True)

    @app_commands.command(name="set_api_domain", description="Setze die API-Domain für diesen Server")
    @app_commands.describe(api_domain="Die API-Domain (z.B. https://rcon.1bv.eu)")
    async def set_api_domain(self, interaction: discord.Interaction, api_domain: str):
        if not (api_domain.startswith("http://") or api_domain.startswith("https://")):
            await interaction.response.send_message(
                "Bitte gib eine gültige URL für die API-Domain an (mit http:// oder https://).", 
                ephemeral=True
            )
            return

        api_domain = api_domain.rstrip('/')
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('''
                INSERT INTO settings (guild_id, api_domain)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET api_domain=excluded.api_domain
            ''', (guild_id, api_domain))
            await db.commit()

        await interaction.response.send_message(f'Die API-Domain wurde erfolgreich auf **{api_domain}** gesetzt.', ephemeral=True)

    @app_commands.command(name="add_channel", description="Füge einen Voice-Kanal als Squad-Kanal hinzu")
    @app_commands.describe(channel="Der Voice-Kanal, der hinzugefügt werden soll")
    async def add_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            try:
                await db.execute('INSERT INTO voice_channels (guild_id, channel_id, name) VALUES (?, ?, ?)', 
                                 (guild_id, str(channel.id), channel.name))
                await db.commit()
                await interaction.response.send_message(
                    f'Voice-Kanal **{channel.name}** wurde hinzugefügt.', 
                    ephemeral=True
                )
            except aiosqlite.IntegrityError:
                await interaction.response.send_message('Dieser Kanal ist bereits in der Datenbank registriert.', ephemeral=True)

    @app_commands.command(name="remove_channel", description="Entferne einen Voice-Kanal aus den Squad-Kanälen")
    @app_commands.describe(channel="Der Voice-Kanal, der entfernt werden soll")
    async def remove_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute('DELETE FROM voice_channels WHERE guild_id = ? AND channel_id = ?', 
                                       (guild_id, str(channel.id)))
            await db.commit()
            if cursor.rowcount > 0:
                await interaction.response.send_message(f'Voice-Kanal **{channel.name}** wurde entfernt.', ephemeral=True)
            else:
                await interaction.response.send_message('Dieser Kanal war nicht in der Datenbank registriert.', ephemeral=True)

    @app_commands.command(name="list_channels", description="Listet alle registrierten Squad-Voice-Kanäle auf")
    async def list_channels(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute('SELECT channel_id, name FROM voice_channels WHERE guild_id = ?', (guild_id,))
            rows = await cursor.fetchall()

        if rows:
            embed = discord.Embed(title="Registrierte Squad-Voice-Kanäle", color=0x72bd27)
            for row in rows:
                embed.add_field(name=row[1], value=f"<#{row[0]}>", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Es wurden keine Voice-Kanäle registriert.", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text_channel = await get_text_channel(message.guild.id)
    if text_channel is None or message.channel.id != text_channel.id:
        return

    if message.content.lower() == "!squadlead":
        # Überprüfe, ob eine API-Domain existiert
        api_domain = await get_api_domain(message.guild.id)
        map_info = None
        if api_domain:
            # Abrufen der Map-Informationen
            map_data = await query_game_server(api_domain)
            if map_data:
                map_info = map_data.get("current_map", {}).get("map", {}).get("pretty_name", "Unbekannt")

        voice_channels = await get_voice_channels(message.guild.id)
        if not voice_channels:
            await message.channel.send('Es wurden keine Voice-Kanäle registriert. Bitte füge sie mit `/add_channel` hinzu.')
            return

        member = message.guild.get_member(message.author.id)
        if not member:
            return

        member_voice_channel = get_member_voice_channel(member, voice_channels)
        if not member_voice_channel:
            await message.channel.send('Du befindest dich in keinem registrierten Voice-Kanal.')
            return

        # Abrufen der Mitglieder im Voice-Kanal
        voice_channel = message.guild.get_channel(int(member_voice_channel['channel_id']))
        if not voice_channel or not voice_channel.members:
            await message.channel.send('Keine Mitglieder im Voice-Kanal gefunden.')
            return

        # Filtere die berechtigten Mitglieder
        eligible_members = [m for m in voice_channel.members if not m.bot]
        if not eligible_members:
            await message.channel.send('Es konnten keine berechtigten Mitglieder gefunden werden.')
            return

        # Teile die Mitglieder in Squads von maximal 6 auf
        squads = []
        random.shuffle(eligible_members)
        for i in range(0, len(eligible_members), 6):
            squads.append(eligible_members[i:i + 6])

        # Wähle Squadleader für jeden Squad aus
        squad_leaders = []
        for squad in squads:
            squad_leader = random.choice(squad)
            squad_leaders.append(squad_leader)

        # Erstelle eine Nachricht mit den Squadleadern, Squadmitgliedern und optional der Map-Information
        embed = discord.Embed(
            title="Squadleader und Squads",
            description=f"Es wurden {len(squads)} Squad(s) erstellt für den Kanal **{member_voice_channel['name']}**!",
            color=0x72bd27
        )

        # Füge Map-Informationen hinzu, falls verfügbar
        if map_info:
            embed.add_field(name="Aktuelle Map", value=map_info, inline=False)

        for idx, squad in enumerate(squads, start=1):
            squad_leader = squad_leaders[idx - 1]
            # Fügt eine Leerzeile nach dem Squadleader ein
            squad_list = [f"⭐ **{squad_leader.display_name}**"] + [
                f"🪖 {m.display_name}" for m in squad if m != squad_leader
            ]
            squad_members = "\n".join(squad_list)
            embed.add_field(
                name=f"Squad {idx} (Leader: ⭐ **{squad_leader.display_name}**)",
                value=squad_members,
                inline=False
            )

        await message.channel.send(embed=embed)

        # Optional: Sende private Nachrichten an die Squadmitglieder
        if SEND_PRIVATE_MESSAGE:
            for idx, squad in enumerate(squads, start=1):
                squad_leader = squad_leaders[idx - 1]
                for member in squad:
                    try:
                        await member.send(
                            f"Du bist im Squad **{member_voice_channel['name']}** (Squad {idx}). "
                            f"Squadleader: ⭐ **{squad_leader.display_name}**."
                        )
                    except Exception as e:
                        print(f"Fehler beim Senden der Nachricht an {member.display_name}: {e}")

# Bot-Token sicher laden
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    print('Bitte setze die Umgebungsvariable DISCORD_BOT_TOKEN in der .env-Datei.')
    exit(1)

# Bot starten
bot.run(TOKEN)
