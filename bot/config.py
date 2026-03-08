import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('DISCORD_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Embed colors
    PRIMARY_COLOR = 0x5865F2
    SUCCESS_COLOR = 0x57F287
    ERROR_COLOR = 0xED4245
    WARNING_COLOR = 0xFEE75C
    INFO_COLOR = 0x5865F2
    
    # Game settings
    POINTS_BASE = 5
    POINTS_DECREMENT = 2
    PENALTY_SECOND_WINNER = 1
