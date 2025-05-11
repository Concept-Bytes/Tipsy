import os
from dotenv import load_dotenv


load_dotenv()


CONFIG_FILE = "pump_config.json"
COCKTAILS_FILE = "cocktails.json"
LOGO_FOLDER = "drink_logos"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    OZ_COEFFICIENT= [
    (24.38),   # Pump 1
    (24.23),  # Pump 2
    (25.43),   # Pump 3
    (30.56),   # Pump 4
    (25.60),   # Pump 5
    (19.29),  # Pump 6
    (24.53),  # Pump 7
    (26.94),  # Pump 8
    (25.16),    # Pump 9
    (20.46),  # Pump 10
    (22.52),  # Pump 11
    (25),  # Pump 12
]
except ValueError:
    OZ_COEFFICIENT = 8.0

INVERT_PUMP_PINS = os.getenv('INVERT_PUMP_PINS', 'false') == 'true'
PUMP_CONCURRENCY = int(os.getenv('PUMP_CONCURRENCY', 3))
FULL_SCREEN = os.getenv('FULL_SCREEN', 'true') == 'true'