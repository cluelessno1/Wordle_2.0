from . import *
import logging
import os
from dotenv import dotenv_values

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the .env file
env_path = os.path.join(current_dir, '.env')

# Load the data from the .env file
config = dotenv_values(env_path)

# Set up logging with the level from the .env file
logging_level = getattr(logging, config['LOGGING_LEVEL'].upper(), None)
if logging_level is not None:
    # Configure the logging
    logging.basicConfig(filename='wordle_2_backend.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
else:
    logging.warning('Invalid LOGGING_LEVEL value in .env file')

logging.info("Starting a new game session. All ther best!!!")