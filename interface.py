# interface.py
import os
import pygame

from settings import *
from helpers import load_cocktails
from controller import make_drink

def animate_text_zoom(screen, base_text, position, start_size, target_size, duration=300, background=None, current_img=None, image_offset=0):
    """Animate overlay text zooming from a small size to target size."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(start_size + (target_size - start_size) * progress)
        font = pygame.font.SysFont(None, current_size)
        text_surface = font.render(base_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (image_offset, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_logo_zoom(screen, logo, rect, base_size, target_size, duration=300, background=None, current_img=None):
    """Animate one logo zooming from base_size to target_size and back."""
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
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Contract back
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_logo_click(screen, logo, rect, base_size, target_size, duration=150, background=None, current_img=None):
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
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
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
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_both_logos_zoom(screen, single_logo, double_logo, single_rect, double_rect, base_size, target_size, duration=300, background=None, current_img=None):
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
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_single, new_rect_single)
        screen.blit(scaled_double, new_rect_double)
        pygame.display.flip()
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
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_single, new_rect_single)
        screen.blit(scaled_double, new_rect_double)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def show_pouring_and_loading(screen, pouring_img, loading_img, watcher, background=None):
    """Overlay pouring_img full screen and a spinning loading_img (720x720) drawn underneath."""
    angle = 0
    screen_size = screen.get_size()
    screen_width, screen_height = screen_size
    while True:
        if watcher.done():
            break
        angle = (angle + 5) % 360
        rotated_loading = pygame.transform.rotate(loading_img, angle)
        rotated_rect = rotated_loading.get_rect(center=(screen_width // 2, screen_height // 2))
        if background:
            screen.blit(background, (0, 0))
        # Draw loading image first (under)
        screen.blit(rotated_loading, rotated_rect)
        # Then draw pouring image on top
        screen.blit(pouring_img, (0, 0))
        pygame.display.flip()

def run_interface():
    pygame.init()
    if FULL_SCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((0, 0))
    screen_size = screen.get_size()
    screen_width, screen_height = screen_size
    pygame.display.set_caption("Cocktail Swipe")

    def get_cocktail_image_path(cocktail):
        """Given a Cocktail object, get the path to the image for that cocktail.
        Image file name is assumed to be the normal_name in lower snake_case"""
        file_name = f'{cocktail.get("normal_name", "").lower().replace(" ", "_")}.png'
        path = os.path.join(LOGO_FOLDER, file_name)
        return path

    def load_cocktail_image(cocktail):
        """Given a Cocktail object, load the image for that cocktail and scale it to the screen size"""
        path = get_cocktail_image_path(cocktail)
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, screen_size)
            return img
        except Exception as e:
            print(f"Error loading {path}: {e}")

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

    cocktail_data = load_cocktails().get('cocktails', [])

    # Load the static background image (tipsy.png)
    try:
        background = pygame.image.load("./tipsy.png")
        background = pygame.transform.scale(background, screen_size)
    except Exception as e:
        print("Error loading background image (tipsy.png):", e)
        background = None
    
    cocktails = []

    for cocktail in cocktail_data:
        if os.path.exists(get_cocktail_image_path(cocktail)):
            cocktails.append(cocktail)

    if not cocktails:
        print("No valid cocktails found in cocktails.json")
        pygame.quit()
        return
    
    current_index = 0

    current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)

    # Load single & double buttons and scale them to 75% of original (base size: 150x150)
    try:
        single_logo = pygame.image.load("single.png")
        single_logo = pygame.transform.scale(single_logo, (150, 150))
    except Exception as e:
        print("Error loading single.png:", e)
        single_logo = None
    try:
        double_logo = pygame.image.load("double.png")
        double_logo = pygame.transform.scale(double_logo, (150, 150))
    except Exception as e:
        print("Error loading double.png:", e)
        double_logo = None

    # Position extra logos: single on left, double on right, spaced more toward edges.
    margin = 50  # adjust as needed for spacing
    single_rect = pygame.Rect(margin, (screen_height - 150) // 2, 150, 150)
    double_rect = pygame.Rect(screen_width - margin - 150, (screen_height - 150) // 2, 150, 150)

    dragging = False
    drag_start_x = 0
    drag_offset = 0
    clock = pygame.time.Clock()

    normal_text_size = 72  
    text_position = (screen_width // 2, int(screen_height * 0.85))

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
                            animate_logo_click(screen, single_logo, single_rect, base_size=150, target_size=220, duration=150, background=background, current_img=current_image)
                        try:
                            pouring_img = pygame.image.load("pouring.png")
                            pouring_img = pygame.transform.scale(pouring_img, screen_size)
                        except Exception as e:
                            print("Error loading pouring.png:", e)
                            pouring_img = None
                        try:
                            loading_img = pygame.image.load("loading.png")
                            loading_img = pygame.transform.scale(loading_img, (720,720))
                        except Exception as e:
                            print("Error loading loading.png:", e)
                            loading_img = None

                        executor_watcher = make_drink(current_cocktail, 'single')

                        if pouring_img and loading_img:
                            show_pouring_and_loading(screen, pouring_img, loading_img, watcher=executor_watcher, background=background)

                    elif double_rect.collidepoint(pos):
                        # Animate double logo click
                        if double_logo:
                            animate_logo_click(screen, double_logo, double_rect, base_size=150, target_size=220, duration=150, background=background, current_img=current_image)
                        try:
                            pouring_img = pygame.image.load("pouring.png")
                            pouring_img = pygame.transform.scale(pouring_img, screen_size)
                        except Exception as e:
                            print("Error loading pouring.png:", e)
                            pouring_img = None
                        try:
                            loading_img = pygame.image.load("loading.png")
                            loading_img = pygame.transform.scale(loading_img, (720,720))
                        except Exception as e:
                            print("Error loading loading.png:", e)
                            loading_img = None

                        executor_watcher = make_drink(current_cocktail, 'double')

                        if pouring_img and loading_img:
                            show_pouring_and_loading(screen, pouring_img, loading_img, watcher=executor_watcher, background=background)
                        
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
                        if background:
                            screen.blit(background, (0, 0))
                        else:
                            screen.fill((0, 0, 0))
                        screen.blit(current_image, (current_offset, 0))
                        if drag_offset < 0:
                            screen.blit(next_image, (screen_width + current_offset, 0))
                        else:
                            screen.blit(previous_image, (-screen_width + current_offset, 0))
                        # Draw overlay text at normal size.
                        font = pygame.font.SysFont(None, normal_text_size)
                        drink_name = current_cocktail_name
                        text_surface = font.render(drink_name, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=text_position)
                        screen.blit(text_surface, text_rect)
                        # Draw extra logos at their current (base) size.
                        if single_logo:
                            screen.blit(single_logo, single_rect)
                        if double_logo:
                            screen.blit(double_logo, double_rect)
                        pygame.display.flip()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                    current_index = new_index
                    current_cocktail, current_image, current_cocktail_name, previous_image, next_image = load_cocktail(current_index)

                    # Animate both extra logos zooming together.
                    if single_logo and double_logo:
                        animate_both_logos_zoom(screen, single_logo, double_logo, single_rect, double_rect, base_size=150, target_size=175, duration=300, background=background, current_img=current_image)
                else:
                    # Animate snapping back if swipe is insufficient.
                    start_offset = drag_offset
                    duration = 300
                    start_time = pygame.time.get_ticks()
                    while True:
                        elapsed = pygame.time.get_ticks() - start_time
                        progress = min(elapsed / duration, 1.0)
                        current_offset = start_offset * (1 - progress)
                        if background:
                            screen.blit(background, (0, 0))
                        else:
                            screen.fill((0, 0, 0))
                        screen.blit(current_image, (current_offset, 0))
                        font = pygame.font.SysFont(None, normal_text_size)
                        drink_name = current_cocktail_name
                        text_surface = font.render(drink_name, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=text_position)
                        screen.blit(text_surface, text_rect)
                        # Draw extra logos.
                        if single_logo:
                            screen.blit(single_logo, single_rect)
                        if double_logo:
                            screen.blit(double_logo, double_rect)
                        pygame.display.flip()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                dragging = False
                drag_offset = 0

        # Main drawing (when not in special animation)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        if dragging:
            screen.blit(current_image, (drag_offset, 0))
            if drag_offset < 0:
                screen.blit(next_image, (screen_width + drag_offset, 0))
            elif drag_offset > 0:
                screen.blit(previous_image, (-screen_width + drag_offset, 0))
        else:
            screen.blit(current_image, (0, 0))
        font = pygame.font.SysFont(None, normal_text_size)
        drink_name = current_cocktail_name
        text_surface = font.render(drink_name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=text_position)
        screen.blit(text_surface, text_rect)
        # Draw extra logos at their base size.
        if single_logo:
            screen.blit(single_logo, single_rect)
        if double_logo:
            screen.blit(double_logo, double_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_interface()
