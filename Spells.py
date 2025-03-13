import discord
from discord.ext import commands
from translate import Translator
import os
import datetime

# Setup translator
translator = Translator(from_lang = "autodetect", to_lang="la")

# Unicode replacement function - Corrected to use Mathematical Bold Script
def convert_to_fancy_unicode(text):
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':  # Capital letters A-Z to 𝓐-𝓩 (U+1D4D0 to U+1D4E9)
            unicode_val = 0x1D4D0 + (ord(char) - ord('A'))
            result += chr(unicode_val)
        elif 'a' <= char <= 'z':  # Small letters a-z to 𝓪-𝓹 (U+1D4EA to U+1D503)
            unicode_val = 0x1D4EA + (ord(char) - ord('a'))
            result += chr(unicode_val)
        elif '0' <= char <= '9':  # Numbers 0-9 to 𝟎-𝟗 (U+1D7CE to U+1D7D7)
            unicode_val = 0x1D7CE + (ord(char) - ord('0'))
            result += chr(unicode_val)
        else:
            result += char  # Keep other characters unchanged
    return result

# Read token from file
with open('token', 'r') as file:
    TOKEN = file.read().strip()

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Debug print: Log all incoming messages
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    channel_name = message.channel.name if hasattr(message.channel, 'name') else "DM"
    print(f"[{timestamp}] {message.author} in {channel_name}: {message.content}")

    # Process commands if any
    await bot.process_commands(message)
    
    # If someone mentions the bot or sends a direct message
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        # Get the content to translate
        content = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        
        # If there's content to translate
        if content:
            print(f"[DEBUG] Attempting to translate: '{content}'")
            # Translate to Latin
            try:
                translation = translator.translate(content)
                print(f"[DEBUG] Translation result: '{translation}'")
                
                # Apply Unicode character replacement with correct Math Bold Script
                fancy_translation = convert_to_fancy_unicode(translation)
                print(f"[DEBUG] After Unicode conversion: '{fancy_translation}'")
                
                # Debug info before reply
                print(f"[DEBUG] Preparing to reply to {message.author.name} with fancy translation")
                
                await message.reply(fancy_translation)
                
                # Debug info after reply
                print(f"[DEBUG] Reply sent successfully to {message.author.name}")
            except Exception as e:
                print(f"[ERROR] Translation failed: {str(e)}")
                await message.reply(f"Error translating: {str(e)}")
                print(f"[DEBUG] Error message sent to {message.author.name}")

# Run the bot
bot.run(TOKEN)