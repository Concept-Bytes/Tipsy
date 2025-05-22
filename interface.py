# interface.py
import pygame

from settings import *
from helpers import get_cocktail_image_path, get_valid_cocktails, wrap_text
from controller import make_drink

import logging
logger = logging.getLogger(__name__)

pygame.init()
if FULL_SCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((720, 720))
screen_size = screen.get_size()
screen_width, screen_height = screen_size
cocktail_image_offset = screen_width * (1.0 - COCKTAIL_IMAGE_SCALE) // 2
pygame.display.set_caption('Cocktail Swipe')

normal_text_size = 72
small_text_size = int(normal_text_size * 0.6)
text_position = (screen_width // 2, int(screen_height * 0.85))

def add_layer(*args, function=screen.blit, key=None):
    if key == None:
        key = len(layers)
    layers[str(key)] = {'function': function, 'args': args}

def remove_layer(key):
    try:
        del layers[key]
    except KeyError:
        pass
    
layers = {}
def draw_frame():
    for layer in layers.values():
        layer['function'](*layer['args'])
    pygame.display.flip()

def animate_logo_click(logo, rect, base_size, target_size, layer_key, duration=150):
    """Animate a logo click (pop effect): grow from base_size to target_size then shrink back."""
    clock = pygame.time.Clock()
    center = rect.center
    # Expand
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(base_size + (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        add_layer(scaled_img, new_rect, key=layer_key)
        draw_frame()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Shrink back
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        add_layer(scaled_img, new_rect, key=layer_key)
        draw_frame()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_logo_rotate(logo, rect, layer_key, rotation=180):
    """Animate a logo click (rotate effect): rotate the amount of rotation provided"""
    angle = 0
    while angle < rotation:
        angle = (angle + 5) % 360
        rotated_loading = pygame.transform.rotate(logo, angle * -1)
        rotated_rect = rotated_loading.get_rect(center=rect.center)
        # Draw loading image first (under)
        add_layer(rotated_loading, rotated_rect, key=layer_key)
        draw_frame()

def animate_both_logos_zoom(single_logo, double_logo, single_rect, double_rect, base_size, target_size, duration=300):
    """Animate both logos zooming in together and then shrinking back."""
    clock = pygame.time.Clock()
    center_single = single_rect.center
    center_double = double_rect.center
    # Expand
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(base_size + (target_size - base_size) * progress)
        scaled_single = pygame.transform.scale(single_logo, (current_size, current_size))
        scaled_double = pygame.transform.scale(double_logo, (current_size, current_size))
        new_rect_single = scaled_single.get_rect(center=center_single)
        new_rect_double = scaled_double.get_rect(center=center_double)
        add_layer(scaled_single, new_rect_single, key='single_logo')
        add_layer(scaled_double, new_rect_double, key='double_logo')
        draw_frame()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Contract
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_single = pygame.transform.scale(single_logo, (current_size, current_size))
        scaled_double = pygame.transform.scale(double_logo, (current_size, current_size))
        new_rect_single = scaled_single.get_rect(center=center_single)
        new_rect_double = scaled_double.get_rect(center=center_double)
        add_layer(scaled_single, new_rect_single, key='single_logo')
        add_layer(scaled_double, new_rect_double, key='double_logo')
        draw_frame()
        if progress >= 1.0:
            break
        clock.tick(60)

def show_pouring_and_loading(watcher):
    """Overlay pouring_img full screen and a spinning loading_img (720x720) drawn underneath."""
    try:
        pouring_img = pygame.image.load('pouring.png')
        pouring_img = pygame.transform.scale(pouring_img, screen_size)
    except Exception as e:
        logger.exception('Error loading pouring.png')
        pouring_img = None
    try:
        loading_img = pygame.image.load('loading.png')
        loading_img = pygame.transform.scale(loading_img, (70, 70))
    except Exception as e:
        logger.exception('Error loading loading.png')
        loading_img = None
    try:
        checkmark_img = pygame.image.load('checkmark.png')
        checkmark_img = pygame.transform.scale(checkmark_img, (30, 30))
    except Exception as e:
        logger.exception('Error loading loading.png')
        checkmark_img = None
        
    angle = 0

    # Add a background layer
    add_layer(*layers['background']['args'], function=layers['background']['function'], key='pouring_background')
    # Then draw pouring image on top
    if pouring_img:
        add_layer(pouring_img, (0, -150), key='pouring')

    pour_layers = []
    pouring_line = 0
    while not watcher.done():
        angle = (angle - 5) % 360
        if loading_img:
            rotated_loading = pygame.transform.rotate(loading_img, angle)
        
        for index, pour in enumerate(watcher.pours):
            layer_key = f'pour_{index}'
            logo_layer_key = f'{layer_key}_logo'
            
            x_position = screen_width // 3
            y_position = (text_position[1] + small_text_size * pouring_line) - 325

            if logo_layer_key not in pour_layers:
                font = pygame.font.SysFont(None, small_text_size)
                for layer_index, line in enumerate(wrap_text(str(pour), font, screen_width * 0.5)):
                    line_key = f'{layer_key}_{layer_index}'
                    text_surface = font.render(line, True, (255, 255, 255))
                    line_y_position = y_position + small_text_size * layer_index
                    if layer_index > 0:
                        line_y_position = line_y_position - 10 * layer_index
                    text_rect = text_surface.get_rect(topleft=(x_position, line_y_position))
                    pour_layers.append(line_key)
                    add_layer(text_surface, text_rect, key=line_key)
                    pouring_line += 1
                pour_layers.append(logo_layer_key)

            status_position = layers.get(logo_layer_key, {}).get('args', [None, None])[1]
            if status_position:
                status_position = status_position.center
            else:
                status_position = (x_position - small_text_size // 2, y_position - 7 + small_text_size // 2)

            if pour.running and loading_img:
                rect = rotated_loading.get_rect(center=status_position)
                add_layer(rotated_loading, rect, key=logo_layer_key)
            else:
                if checkmark_img:
                    rect = checkmark_img.get_rect(center=status_position)
                    add_layer(checkmark_img, rect, key=logo_layer_key)
                else:
                    remove_layer(logo_layer_key)
                    

        draw_frame()

    for layer in pour_layers:
        remove_layer(layer)

    remove_layer('pouring')
    remove_layer('pouring_background')
    draw_frame()
    pygame.event.clear()  # Drop all events that happened while pouring

def run_interface():

    def load_cocktail_image(cocktail):
        """Given a Cocktail object, load the image for that cocktail and scale it to the screen size"""
        path = get_cocktail_image_path(cocktail)
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (screen_width * COCKTAIL_IMAGE_SCALE, screen_height * COCKTAIL_IMAGE_SCALE))
            return img
        except Exception as e:
            logger.exception(f'Error loading {path}')

    def load_cocktail(index):
        """Load a cocktail based on a provided index. Also pre-load the images for the previous and next cocktails"""
        current_cocktail = cocktails[index]
        current_image = load_cocktail_image(current_cocktail)
        current_cocktail_name = current_cocktail.get('normal_name', '')
        previous_cocktail = cocktails[(index - 1) % len(cocktails)]
        previous_image = load_cocktail_image(previous_cocktail)
        next_cocktail = cocktails[(index + 1) % len(cocktails)]
        next_image = load_cocktail_image(next_cocktail)
        return current_cocktail, current_image, current_cocktail_name, previous_image, next_image

    # Load the static background image (tipsy.png)
    try:
        background = pygame.image.load('./tipsy.jpg')
        background = pygame.transform.scale(background, screen_size)
        add_layer(background, (0, 0), key='background')
    except Exception as e:
        logger.exception('Error loading background image (tipsy.png)')
        add_layer((0, 0), function=screen.fill, key='background')
    
    cocktails = get_valid_cocktails()
    if not cocktails:
        logger.critical('No valid cocktails found in cocktails.json')
        pygame.quit()
        return
    current_index = 0
    current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)
    reload_time = pygame.time.get_ticks()

    margin = 50  # adjust as needed for spacing
    # Load single & double buttons and scale them to 75% of original (base size: 150x150)
    try:
        single_logo = pygame.image.load('single.png')
        single_logo = pygame.transform.scale(single_logo, (150, 150))
        single_rect = pygame.Rect(margin, (screen_height - 150) // 2, 150, 150)
        add_layer(single_logo, single_rect, key='single_logo')
    except Exception as e:
        logger.exception('Error loading single.png:')
        single_logo = None
    try:
        double_logo = pygame.image.load('double.png')
        double_logo = pygame.transform.scale(double_logo, (150, 150))
        double_rect = pygame.Rect(screen_width - margin - 150, (screen_height - 150) // 2, 150, 150)
        add_layer(double_logo, double_rect, key='double_logo')
    except Exception as e:
        logger.exception('Error loading double.png')
        double_logo = None
    if SHOW_RELOAD_COCKTAILS_BUTTON:
        reload_cocktails_rect = pygame.Rect(screen_width - 150, 150, 50, 50)
        try:
            reload_logo = pygame.image.load('reload.png')
            reload_logo = pygame.transform.scale(reload_logo, (50, 50))
            add_layer(reload_logo, reload_cocktails_rect, key='reload_logo')
        except Exception as e:
            logger.exception('Error loading loading.png')
            reload_logo = None
    else:
        reload_cocktails_rect = None
        reload_logo = None

    dragging = False
    drag_start_x = 0
    drag_offset = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                drag_start_x = event.pos[0]
            if event.type == pygame.MOUSEMOTION and dragging:
                current_x = event.pos[0]
                drag_offset = current_x - drag_start_x
            if event.type == pygame.MOUSEBUTTONUP and dragging:
                # If it's a click (minimal drag), check extra logos.
                if abs(drag_offset) < 10:
                    pos = event.pos
                    if single_rect.collidepoint(pos):
                        # Animate single logo click
                        if single_logo:
                            animate_logo_click(single_logo, single_rect, base_size=150, target_size=220, layer_key='single_logo', duration=150)

                        executor_watcher = make_drink(current_cocktail, 'single')

                        show_pouring_and_loading(watcher=executor_watcher)

                    elif double_rect.collidepoint(pos):
                        # Animate double logo click
                        if double_logo:
                            animate_logo_click(double_logo, double_rect, base_size=150, target_size=220, layer_key='double_logo', duration=150)

                        executor_watcher = make_drink(current_cocktail, 'double')

                        show_pouring_and_loading(executor_watcher)
                    
                    elif reload_cocktails_rect and reload_cocktails_rect.collidepoint(pos):
                        logger.debug('Reloading cocktails due to reload button press')
                        animate_logo_rotate(reload_logo, reload_cocktails_rect, layer_key='reload_logo')
                        cocktails = get_valid_cocktails()
                        current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)
                        
                    dragging = False
                    drag_offset = 0
                    continue  # Skip further swipe handling.
                # Otherwise, it's a swipe.
                if abs(drag_offset) > screen_width / 4:
                    if drag_offset < 0:
                        target_offset = -screen_width
                        new_index = (current_index + 1) % len(cocktails)
                    else:
                        target_offset = screen_width
                        new_index = (current_index - 1) % len(cocktails)
                    start_offset = drag_offset
                    duration = 300
                    start_time = pygame.time.get_ticks()
                    while True:
                        elapsed = pygame.time.get_ticks() - start_time
                        progress = min(elapsed / duration, 1.0)
                        current_offset = start_offset + (target_offset - start_offset) * progress
                        add_layer(current_image, (current_offset + cocktail_image_offset, cocktail_image_offset), key='current_cocktail')
                        if drag_offset < 0:
                            add_layer(next_image, (screen_width + current_offset + cocktail_image_offset, cocktail_image_offset), key='next_cocktail')
                        else:
                            add_layer(previous_image, (-screen_width + current_offset + cocktail_image_offset, cocktail_image_offset), key='previous_cocktail')
                        draw_frame()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                    current_index = new_index
                    current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)

                    # Animate both extra logos zooming together.
                    if single_logo and double_logo:
                        animate_both_logos_zoom(single_logo, double_logo, single_rect, double_rect, base_size=150, target_size=175, duration=300)
                else:
                    # Animate snapping back if swipe is insufficient.
                    start_offset = drag_offset
                    duration = 300
                    start_time = pygame.time.get_ticks()
                    while True:
                        elapsed = pygame.time.get_ticks() - start_time
                        progress = min(elapsed / duration, 1.0)
                        current_offset = start_offset * (1 - progress)
                        add_layer(current_image, (current_offset + cocktail_image_offset, cocktail_image_offset), key='current_cocktail')
                        font = pygame.font.SysFont(None, normal_text_size)
                        drink_name = current_cocktail_name
                        text_surface = font.render(drink_name, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=text_position)
                        add_layer(text_surface, text_rect, key='cocktail_name')
                        draw_frame()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                dragging = False
                drag_offset = 0

        # Main drawing (when not in special animation)
        if RELOAD_COCKTAILS_TIMEOUT and pygame.time.get_ticks() - reload_time > RELOAD_COCKTAILS_TIMEOUT:
            logger.debug('Reloading cocktails due to auto reload timeout')
            cocktails = get_valid_cocktails()
            current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)
            reload_time = pygame.time.get_ticks()

        if dragging:
            remove_layer('cocktail_name')
            add_layer(current_image, (drag_offset + cocktail_image_offset, cocktail_image_offset), key='current_cocktail')
            if drag_offset < 0:
                add_layer(next_image, (screen_width + drag_offset + cocktail_image_offset, cocktail_image_offset), key='next_cocktail')
            elif drag_offset > 0:
                add_layer(previous_image, (-screen_width + drag_offset + cocktail_image_offset, cocktail_image_offset), key='previous_cocktail')
        else:
            remove_layer('next_cocktail')
            remove_layer('previous_cocktail')
            add_layer(current_image, (cocktail_image_offset, cocktail_image_offset), key='current_cocktail')
            font = pygame.font.SysFont(None, normal_text_size)
            drink_name = current_cocktail_name
            text_surface = font.render(drink_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=text_position)
            add_layer(text_surface, text_rect, key='cocktail_name')
        draw_frame()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    run_interface()
