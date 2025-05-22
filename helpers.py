import base64
import os
import json
import streamlit as st
from settings import *
import assist
import requests
from rembg import remove
from PIL import Image

import logging
logger = logging.getLogger(__name__)


def load_saved_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f'Error loading configuration: {e}')
    return {}


def save_config(data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f'Error saving configuration: {e}')


def load_cocktails():
    if os.path.exists(COCKTAILS_FILE):
        try:
            with open(COCKTAILS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f'Error loading cocktails: {e}')
    return {}


def get_cocktail_image_path(cocktail):
    """Given a Cocktail object, get the path to the image for that cocktail.
    Image file name is assumed to be the normal_name in lower snake_case"""
    file_name = f'{cocktail.get("normal_name", "").lower().replace(" ", "_")}.png'
    path = os.path.join(LOGO_FOLDER, file_name)
    return path


def get_valid_cocktails():
    cocktail_data = load_cocktails().get('cocktails', [])
    cocktails = []
    for cocktail in cocktail_data:
        if os.path.exists(get_cocktail_image_path(cocktail)):
            cocktails.append(cocktail)
    return cocktails


def save_cocktails(data, append=True):
    """Save the given list of cocktails to the cocktails file."""
    try:
        cocktails = load_cocktails()
        with open(COCKTAILS_FILE, 'w') as f:
            if append:
                cocktails['cocktails'] += data['cocktails']
            else:
                cocktails = data
            json.dump(cocktails, f, indent=2)
    except Exception as e:
        st.error(f'Error saving cocktails: {e}')


def get_safe_name(name):
    """Convert a cocktail name to a safe filename-friendly string."""
    return name.lower().replace(' ', '_')


def generate_image(normal_name, regenerate=False, ingredients=None):
    safe_cname = get_safe_name(normal_name)
    filename = os.path.join(LOGO_FOLDER, f'{safe_cname}.png')

    if not regenerate and os.path.exists(filename):
        # If it already exists, skip generation
        return filename
    else:
        background_color = 'plain white'
        if USE_GPT_TRANSPARENCY:
            background_color = 'transparent'
        prompt = (
            f'A realistic illustration of a {normal_name} cocktail on a {background_color} background. '
            'The lighting and shading create depth and realism, making the drink appear fresh and inviting. '
            'Do not include shadows, reflections, or the cocktail name in the image.'
        )
        if ingredients:
            prompt = f'{prompt} The cocktail ingredients are: {", ".join([ingredient for ingredient in ingredients])}'
        try:
            # Generate the image URL
            b64_image = assist.generate_image(prompt)
            logger.debug(f'Image generated for {normal_name}')

            if USE_GPT_TRANSPARENCY:
                save_base64_image(b64_image, filename)
            else:
                # Download + remove background in memory
                logger.debug(f'Removing background from image for {normal_name}')
                from io import BytesIO
                with Image.open(BytesIO(base64.b64decode(b64_image))) as original_img:
                    img = remove(original_img.convert('RGBA'))
                    logger.debug(f'Saving image with removed background for {normal_name}')
                    img.save(filename, 'PNG')

            return filename

        except Exception as e:
            logger.exception('Image generation error')


def save_base64_image(base64_string, output_path):
    """
    Decodes a base64 string and saves it as an image file.

    Args:
        base64_string: The base64 encoded string of the image.
        output_path: The path to save the image file.
    """
    try:
        image_data = base64.b64decode(base64_string)
        with open(output_path, 'wb') as file:
            file.write(image_data)
        logger.debug(f'Image saved to {output_path}')
    except Exception as e:
        logger.exception(f'Error decoding or saving image')


def wrap_text(text, font, width):
    """Wrap text to fit inside a given width when rendered.

    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.

    """
    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)
    return wrapped_lines