import os
import json
import logging

logger = logging.getLogger(__name__)

if 'PYTEST_CURRENT_TEST' not in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

    
CONFIG_FILE = os.getenv('PUMP_CONFIG_FILE', 'pump_config.json')
COCKTAILS_FILE = os.getenv('COCKTAILS_FILE', 'cocktails.json')
LOGO_FOLDER = os.getenv('LOGO_FOLDER', 'drink_logos')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

settings = {
    'DEBUG': {
        'parse_method': json.loads,
        'default': 'false'
    }, 
    'OZ_COEFFICIENT': {
        'parse_method': float,
        'default': '8.0'
    }, 
    'PUMP_CONCURRENCY': {
        'parse_method': int,
        'default': '3'
    }, 
    'RELOAD_COCKTAILS_TIMEOUT': {
        'parse_method': int,
        'default': '0'
    }, 
    'RETRACTION_TIME': {
        'parse_method': float,
        'default': '0'
    }, 
    'COCKTAIL_IMAGE_SCALE': {
        'parse_method': float,
        'default': '1.0'
    }, 
    'INVERT_PUMP_PINS': {
        'parse_method': json.loads,
        'default': 'false'
    }, 
    'FULL_SCREEN': {
        'parse_method': json.loads,
        'default': 'true'
    }, 
    'SHOW_RELOAD_COCKTAILS_BUTTON': {
        'parse_method': json.loads,
        'default': 'false'
    }, 
    'USE_GPT_TRANSPARENCY': {
        'parse_method': json.loads,
        'default': 'false'
    },
    'ALLOW_FAVORITES': {
        'parse_method': json.loads,
        'default': 'false'
    }
}
for name in settings:
    try:
        value = settings[name]['parse_method'](os.getenv(name))
    except (ValueError, json.decoder.JSONDecodeError, TypeError):
        # logger.exception(f'invalid ENV value for {name}')
        value = settings[name]['parse_method'](settings[name]['default'])
    exec(f'{name} = value')

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
