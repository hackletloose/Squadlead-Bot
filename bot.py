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

# Übersetzungen für unterstützte Sprachen
translations = {
    'en': {
        'bot_ready': 'Bot is ready as {bot_user}',
        'squad_commands_added': "SquadCommands Cog added.",
        'squad_commands_error': "Error adding SquadCommands Cog: {error}",
        'sync_commands': 'Synced {count} global slash commands',
        'sync_error': 'Error syncing slash commands: {error}',
        'set_text_channel_success': 'Text channel has been set to {channel}.',
        'set_api_domain_invalid': 'Please provide a valid URL for the API domain (with http:// or https://).',
        'set_api_domain_success': 'API domain has been successfully set to **{api_domain}**.',
        'add_channel_success': 'Voice channel **{channel_name}** has been added.',
        'add_channel_exists': 'This channel is already registered in the database.',
        'remove_channel_success': 'Voice channel **{channel_name}** has been removed.',
        'remove_channel_not_found': 'This channel was not registered in the database.',
        'list_channels_title': 'Registered Squad Voice Channels',
        'list_channels_empty': 'No voice channels have been registered.',
        'squadlead_no_channels': 'No voice channels have been registered. Please add them using `/add_channel`.',
        'squadlead_not_in_channel': 'You are not in a registered voice channel.',
        'squadlead_no_members': 'No members found in the voice channel.',
        'squadlead_no_eligible': 'No eligible members found.',
        'squadlead_title': 'Who will be Squad Leader?',
        'squadlead_description': 'Created {squad_count} squad(s) for the channel **{channel_name}**!',
        'squadlead_no_map': 'Unknown',
        'current_map': 'Current Map',
        'squad_field': 'Squad {squad_number} (Leader: ⭐ **{leader_name}**)',
        'private_message': 'You are in Squad **{channel_name}** (Squad {squad_number}). Squad Leader: ⭐ **{leader_name}**.',
        'default_language': 'en',
        'set_language_success': 'Language has been set to **{language}**.',
    },
    'de': {
        'bot_ready': 'Bot ist bereit als {bot_user}',
        'squad_commands_added': "SquadCommands Cog hinzugefügt.",
        'squad_commands_error': "Fehler beim Hinzufügen des Cogs: {error}",
        'sync_commands': 'Synchronisierte {count} globale Slash-Befehle',
        'sync_error': 'Fehler beim Synchronisieren der Slash-Befehle: {error}',
        'set_text_channel_success': 'Der Textkanal wurde auf {channel} gesetzt.',
        'set_api_domain_invalid': 'Bitte gib eine gültige URL für die API-Domain an (mit http:// oder https://).',
        'set_api_domain_success': 'Die API-Domain wurde erfolgreich auf **{api_domain}** gesetzt.',
        'add_channel_success': 'Voice-Kanal **{channel_name}** wurde hinzugefügt.',
        'add_channel_exists': 'Dieser Kanal ist bereits in der Datenbank registriert.',
        'remove_channel_success': 'Voice-Kanal **{channel_name}** wurde entfernt.',
        'remove_channel_not_found': 'Dieser Kanal war nicht in der Datenbank registriert.',
        'list_channels_title': 'Registrierte Squad-Voice-Kanäle',
        'list_channels_empty': 'Es wurden keine Voice-Kanäle registriert.',
        'squadlead_no_channels': 'Es wurden keine Voice-Kanäle registriert. Bitte füge sie mit `/add_channel` hinzu.',
        'squadlead_not_in_channel': 'Du befindest dich in keinem registrierten Voice-Kanal.',
        'squadlead_no_members': 'Keine Mitglieder im Voice-Kanal gefunden.',
        'squadlead_no_eligible': 'Es konnten keine berechtigten Mitglieder gefunden werden.',
        'squadlead_title': 'Wer wird Squadleader?',
        'squadlead_description': 'Es wurden {squad_count} Squad(s) erstellt für den Kanal **{channel_name}**!',
        'squadlead_no_map': 'Unbekannt',
        'current_map': 'Aktuelle Map',
        'squad_field': 'Squad {squad_number} (Leader: ⭐ **{leader_name}**)',
        'private_message': 'Du bist im Squad **{channel_name}** (Squad {squad_number}). Squadleader: ⭐ **{leader_name}**.',
        'default_language': 'de',
        'set_language_success': 'Die Sprache wurde auf **{language}** gesetzt.',
    },
    'fr': {
        'bot_ready': 'Le bot est prêt en tant que {bot_user}',
        'squad_commands_added': "Cog SquadCommands ajouté.",
        'squad_commands_error': "Erreur lors de l'ajout du Cog SquadCommands : {error}",
        'sync_commands': 'Synchronisé {count} commandes slash globales',
        'sync_error': 'Erreur lors de la synchronisation des commandes slash : {error}',
        'set_text_channel_success': 'Le canal texte a été défini sur {channel}.',
        'set_api_domain_invalid': 'Veuillez fournir une URL valide pour le domaine de l\'API (avec http:// ou https://).',
        'set_api_domain_success': 'Le domaine de l\'API a été défini avec succès sur **{api_domain}**.',
        'add_channel_success': 'Le canal vocal **{channel_name}** a été ajouté.',
        'add_channel_exists': 'Ce canal est déjà enregistré dans la base de données.',
        'remove_channel_success': 'Le canal vocal **{channel_name}** a été supprimé.',
        'remove_channel_not_found': 'Ce canal n\'était pas enregistré dans la base de données.',
        'list_channels_title': 'Canaux vocaux Squad enregistrés',
        'list_channels_empty': 'Aucun canal vocal n\'a été enregistré.',
        'squadlead_no_channels': 'Aucun canal vocal n\'a été enregistré. Veuillez les ajouter en utilisant `/add_channel`.',
        'squadlead_not_in_channel': 'Vous n\'êtes dans aucun canal vocal enregistré.',
        'squadlead_no_members': 'Aucun membre trouvé dans le canal vocal.',
        'squadlead_no_eligible': 'Aucun membre éligible trouvé.',
        'squadlead_title': 'Qui sera le chef d\'escouade?',
        'squadlead_description': 'Créé {squad_count} escouade(s) pour le canal **{channel_name}**!',
        'squadlead_no_map': 'Inconnu',
        'current_map': 'Carte actuelle',
        'squad_field': 'Escouade {squad_number} (Chef: ⭐ **{leader_name}**)',
        'private_message': 'Vous êtes dans l\'escouade **{channel_name}** (Escouade {squad_number}). Chef d\'escouade: ⭐ **{leader_name}**.',
        'default_language': 'fr',
        'set_language_success': 'La langue a été définie sur **{language}**.',
    },
    'es': {
        'bot_ready': 'El bot está listo como {bot_user}',
        'squad_commands_added': "Cog SquadCommands añadido.",
        'squad_commands_error': "Error al añadir Cog SquadCommands: {error}",
        'sync_commands': 'Sincronizadas {count} comandos slash globales',
        'sync_error': 'Error al sincronizar los comandos slash: {error}',
        'set_text_channel_success': 'El canal de texto ha sido configurado a {channel}.',
        'set_api_domain_invalid': 'Por favor, proporciona una URL válida para el dominio de la API (con http:// o https://).',
        'set_api_domain_success': 'El dominio de la API se ha establecido correctamente en **{api_domain}**.',
        'add_channel_success': 'El canal de voz **{channel_name}** ha sido añadido.',
        'add_channel_exists': 'Este canal ya está registrado en la base de datos.',
        'remove_channel_success': 'El canal de voz **{channel_name}** ha sido eliminado.',
        'remove_channel_not_found': 'Este canal no estaba registrado en la base de datos.',
        'list_channels_title': 'Canales de voz Squad registrados',
        'list_channels_empty': 'No se han registrado canales de voz.',
        'squadlead_no_channels': 'No se han registrado canales de voz. Por favor, añádelos usando `/add_channel`.',
        'squadlead_not_in_channel': 'No estás en ningún canal de voz registrado.',
        'squadlead_no_members': 'No se encontraron miembros en el canal de voz.',
        'squadlead_no_eligible': 'No se encontraron miembros elegibles.',
        'squadlead_title': '¿Quién será el líder de escuadra?',
        'squadlead_description': '¡Creadas {squad_count} escuadra(s) para el canal **{channel_name}**!',
        'squadlead_no_map': 'Desconocido',
        'current_map': 'Mapa actual',
        'squad_field': 'Escuadra {squad_number} (Líder: ⭐ **{leader_name}**)',
        'private_message': 'Estás en la Escuadra **{channel_name}** (Escuadra {squad_number}). Líder de escuadra: ⭐ **{leader_name}**.',
        'default_language': 'es',
        'set_language_success': 'El idioma se ha establecido a **{language}**.',
    },
    # Weitere Sprachen können hier hinzugefügt werden
}

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
        # Erstelle die settings-Tabelle, falls sie nicht existiert
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                guild_id TEXT PRIMARY KEY,
                text_channel_id TEXT,
                api_domain TEXT,
                language TEXT DEFAULT 'en'
            )
        ''')
        # Überprüfe, ob die 'language'-Spalte existiert
        cursor = await db.execute("PRAGMA table_info(settings);")
        columns = await cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'language' not in column_names:
            await db.execute("ALTER TABLE settings ADD COLUMN language TEXT DEFAULT 'en';")
            print("Spalte 'language' zur settings-Tabelle hinzugefügt.")
        
        # Erstelle die voice_channels-Tabelle, falls sie nicht existiert
        await db.execute('''
            CREATE TABLE IF NOT EXISTS voice_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                channel_id TEXT UNIQUE,
                name TEXT
            )
        ''')
        await db.commit()

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
        cursor = await db.execute('SELECT channel_id, name FROM voice_channels WHERE guild_id = ?', (guild_id,))
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
                    print(f"Error querying API: Status {response.status}")
                    return None
    except asyncio.TimeoutError:
        print("API query timed out.")
        return None
    except aiohttp.ClientError as e:
        print(f"Error querying API: {e}")
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

async def get_guild_language(guild_id):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute('SELECT language FROM settings WHERE guild_id = ?', (str(guild_id),))
        row = await cursor.fetchone()
        if row and row[0]:
            return row[0]
        else:
            return translations['en']['default_language']  # Standardsprache Englisch

def translate(guild_language, key, **kwargs):
    lang_translations = translations.get(guild_language, translations['en'])
    text = lang_translations.get(key, translations['en'].get(key, ''))
    return text.format(**kwargs)

# Cog für Squad-Befehle
class SquadCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_text_channel", description="Set the text channel for squad commands")
    @app_commands.describe(channel="The text channel to be used for squad commands")
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

        # Hole die aktuelle Sprache der Guild
        language = await get_guild_language(interaction.guild.id)
        message = translate(language, 'set_text_channel_success', channel=channel.mention)
        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="set_api_domain", description="Set the API domain for this server")
    @app_commands.describe(api_domain="The API domain (e.g., https://rcon.1bv.eu)")
    async def set_api_domain(self, interaction: discord.Interaction, api_domain: str):
        if not (api_domain.startswith("http://") or api_domain.startswith("https://")):
            language = await get_guild_language(interaction.guild.id)
            message = translate(language, 'set_api_domain_invalid')
            await interaction.response.send_message(message, ephemeral=True)
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

        language = await get_guild_language(interaction.guild.id)
        message = translate(language, 'set_api_domain_success', api_domain=api_domain)
        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="add_channel", description="Add a voice channel as a squad channel")
    @app_commands.describe(channel="The voice channel to be added")
    async def add_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            try:
                await db.execute('INSERT INTO voice_channels (guild_id, channel_id, name) VALUES (?, ?, ?)', 
                                 (guild_id, str(channel.id), channel.name))
                await db.commit()
                language = await get_guild_language(interaction.guild.id)
                message = translate(language, 'add_channel_success', channel_name=channel.name)
                await interaction.response.send_message(message, ephemeral=True)
            except aiosqlite.IntegrityError:
                language = await get_guild_language(interaction.guild.id)
                message = translate(language, 'add_channel_exists')
                await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="remove_channel", description="Remove a voice channel from squad channels")
    @app_commands.describe(channel="The voice channel to be removed")
    async def remove_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute('DELETE FROM voice_channels WHERE guild_id = ? AND channel_id = ?', 
                                       (guild_id, str(channel.id)))
            await db.commit()
            language = await get_guild_language(interaction.guild.id)
            if cursor.rowcount > 0:
                message = translate(language, 'remove_channel_success', channel_name=channel.name)
                await interaction.response.send_message(message, ephemeral=True)
            else:
                message = translate(language, 'remove_channel_not_found')
                await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="list_channels", description="List all registered squad voice channels")
    async def list_channels(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute('SELECT channel_id, name FROM voice_channels WHERE guild_id = ?', (guild_id,))
            rows = await cursor.fetchall()

        language = await get_guild_language(interaction.guild.id)
        if rows:
            embed = discord.Embed(title=translate(language, 'list_channels_title'), color=0x72bd27)
            for row in rows:
                embed.add_field(name=row[1], value=f"<#{row[0]}>", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            message = translate(language, 'list_channels_empty')
            await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="set_language", description="Set the language for the bot")
    @app_commands.describe(language="The language to set (e.g., en, de, fr, es)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_language(self, interaction: discord.Interaction, language: str):
        language = language.lower()
        if language not in translations:
            available = ', '.join(translations.keys())
            await interaction.response.send_message(
                f"Unsupported language. Available languages: {available}",
                ephemeral=True
            )
            return

        guild_id = str(interaction.guild.id)
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('''
                UPDATE settings SET language = ?
                WHERE guild_id = ?
            ''', (language, guild_id))
            await db.commit()

        message = translate(language, 'set_language_success', language=language)
        await interaction.response.send_message(message, ephemeral=True)

# Übersetzung für den 'set_language_success' Befehl hinzufügen
# (Diese Einträge sind bereits in den Übersetzungs-Dictionaries enthalten)

@bot.event
async def on_ready():
    await setup_database()
    print(f'Bot ist bereit als {bot.user}')

    # Hinzufügen des Cogs
    try:
        await bot.add_cog(SquadCommands(bot))
        print(translations['en']['squad_commands_added'])  # Standard Englisch im Log
    except Exception as e:
        print(translations['en']['squad_commands_error'].format(error=e))

    # Synchronisieren der Slash-Befehle
    try:
        synced = await bot.tree.sync()
        print(translations['en']['sync_commands'].format(count=len(synced)))
    except Exception as e:
        print(translations['en']['sync_error'].format(error=e))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    text_channel = await get_text_channel(message.guild.id)
    if text_channel is None or message.channel.id != text_channel.id:
        return

    if message.content.lower() == "!squadlead":
        language = await get_guild_language(message.guild.id)

        # Überprüfe, ob eine API-Domain existiert
        api_domain = await get_api_domain(message.guild.id)
        map_info = None
        if api_domain:
            # Abrufen der Map-Informationen
            map_data = await query_game_server(api_domain)
            if map_data:
                map_info = map_data.get("current_map", {}).get("map", {}).get("pretty_name", translate(language, 'squadlead_no_map'))

        voice_channels = await get_voice_channels(message.guild.id)
        if not voice_channels:
            await message.channel.send(translate(language, 'squadlead_no_channels'))
            return

        member = message.guild.get_member(message.author.id)
        if not member:
            return

        member_voice_channel = get_member_voice_channel(member, voice_channels)
        if not member_voice_channel:
            await message.channel.send(translate(language, 'squadlead_not_in_channel'))
            return

        # Abrufen der Mitglieder im Voice-Kanal
        voice_channel = message.guild.get_channel(int(member_voice_channel['channel_id']))
        if not voice_channel or not voice_channel.members:
            await message.channel.send(translate(language, 'squadlead_no_members'))
            return

        # Filtere die berechtigten Mitglieder
        eligible_members = [m for m in voice_channel.members if not m.bot]
        if not eligible_members:
            await message.channel.send(translate(language, 'squadlead_no_eligible'))
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
            title=translate(language, 'squadlead_title'),
            description=translate(language, 'squadlead_description', squad_count=len(squads), channel_name=member_voice_channel['name']),
            color=0x72bd27
        )

        # Füge Map-Informationen hinzu, falls verfügbar
        if map_info:
            embed.add_field(name=translate(language, 'current_map'), value=map_info, inline=False)

        for idx, squad in enumerate(squads, start=1):
            squad_leader = squad_leaders[idx - 1]
            squad_list = [f"⭐ **{squad_leader.display_name}**"] + [
                f"🪖 {m.display_name}" for m in squad if m != squad_leader
            ]
            squad_members = "\n".join(squad_list)
            field_name = translate(language, 'squad_field', squad_number=idx, leader_name=squad_leader.display_name)
            embed.add_field(
                name=field_name,
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
                        private_message = translate(language, 'private_message', channel_name=member_voice_channel['name'], squad_number=idx, leader_name=squad_leader.display_name)
                        await member.send(private_message)
                    except Exception as e:
                        print(f"Fehler beim Senden der Nachricht an {member.display_name}: {e}")

# Bot-Token sicher laden
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    print('Bitte setze die Umgebungsvariable DISCORD_BOT_TOKEN in der .env-Datei.')
    exit(1)

# Bot starten
bot.run(TOKEN)
