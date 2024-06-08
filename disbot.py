import discord
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('TOKEN')

# Initialize bot with specified intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message-related intents
client = discord.Client(intents=intents)


# List of jokes
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "I'm reading a book on the history of glue. I just can't seem to put it down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts!",
]

# List of greetings and their responses
GREETINGS = {
    "hello": ["Hello!", "Hi there!", "Hey!"], # Responds to "hello" with various options
    "hi": ["Hi!", "Hey!", "Selam!"], # Responds to "hi" with various options
    "hey": ["Hey!", "Hello!", "Selam!"], # Responds to "hey" with various options
    "selam": ["Selam!", "ሰላም!"],  # Adding Tigrgna greeting
    "whatsapp": ["WhatsApp!", "What's up?", "Yo!"],  # Responds to "whatsapp" with WhatsApp
    "goodbye": ["See you later!", "Bye!", "Goodbye!", "Cheers!"],  # Responds to "goodbye" with various options
    "bye": ["See you later!", "Goodbye!", "Cheers!"],  # Responds to "bye" with various options
    "cheers": ["Cheers!", "Take it easy!", "Catch you later!"],  # Responds to "cheers" with various options
    "take it easy": ["Cheers!", "Take it easy!", "Catch you later!"],  # Responds to "take it easy" with various options
}

def print_ec2_metadata():
    try:
        # Attempt to fetch EC2 metadata
        instance_id = ec2_metadata.instance_id
        instance_type = ec2_metadata.instance_type
        availability_zone = ec2_metadata.availability_zone
        print(f"EC2 Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"Availability Zone: {availability_zone}")
    except Exception as e:
        print(f"Error fetching EC2 metadata: {e}")

print_ec2_metadata()

# Event triggered when the bot is ready
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent loops
    if message.author == client.user:
        return
    
    # Check if the message content is not empty
    if message.content.strip() != "":
        # Print message details
        print(f'Message "{message.content}" by {message.author.name} in channel "{message.channel.name}"')

    # Check if the message contains specific keywords and respond accordingly
    for greeting in GREETINGS:
        if greeting in message_content:
            response = random.choice(GREETINGS[greeting])
            await message.channel.send(f"{response} {message.author.name}")
            return
    
    # Respond to jokes request
    if "tell me a joke" in message_content or "say something funny" in message_content:
        await message.channel.send(random.choice(JOKES))
        return
    
    # Respond to server info request
    if "tell me about my server" in message_content:
        try:
            # Attempt to fetch EC2 metadata
            instance_id = ec2_metadata.instance_id
            instance_type = ec2_metadata.instance_type
            availability_zone = ec2_metadata.availability_zone
            metadata_str = f"EC2 Instance ID: {instance_id}, Instance Type: {instance_type}, Availability Zone: {availability_zone}"
            # Send metadata information to the Discord channel
            await message.channel.send(metadata_str)
        except ConnectionError:
            # Inform the user about the connection issue
            await message.channel.send("Error: Unable to connect to EC2 metadata service.")
        except TimeoutError:
            # Inform the user about the timeout issue
            await message.channel.send("Error: Connection to EC2 metadata service timed out.")
        except Exception as e:
            await message.channel.send(f"Error fetching EC2 metadata: {e}")

# Run the bot using the token from the environment variables
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print(f"Error logging in: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
