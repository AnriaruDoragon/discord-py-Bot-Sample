import logging, time
from discord.ext import commands
from config.secret import token
from config.logging import *
from config.client import *

# Logging data
logging.basicConfig(filename=log_file, filemode="w", encoding=log_encoding, format=log_format, datefmt=log_dateformat, level=logging.INFO)

client = commands.Bot(command_prefix=command_prefix)

@client.event
async def on_ready():
    logging.info("{0.user} is Ready!".format(client))

while True:
    try:
        client.run(token)
    except BaseException as run_error:
        logging.critical(run_error)
        time.sleep(30)