import pygame
from enum import Enum
class RectPosition(Enum):
    TOP_LEFT = 'topleft'
    CENTER = 'center'

def Text(surface: pygame.Surface, content: str, color: pygame.Color, position: tuple[int, int], font: pygame.font.Font, outline_color: pygame.Color | None = None, outline_size: int = 2, rect_pos: RectPosition = RectPosition.TOP_LEFT):
    text_surface = font.render(content, True, color)
    if rect_pos == RectPosition.CENTER:
        text_rect = text_surface.get_rect(center=position)
    elif rect_pos == RectPosition.TOP_LEFT:
        text_rect = text_surface.get_rect(topleft=position)
    else:
        raise ValueError("Invalid rect_pos value. Must be 'topleft' or 'center'")
    if outline_color:
        text_outline_surface = font.render(content, True, outline_color)
        outline_offsets = [(-outline_size, 0), (outline_size, 0), (0, -outline_size), (0, outline_size)]
        for dx, dy in outline_offsets:
            surface.blit(text_outline_surface, (text_rect.x + dx, text_rect.y + dy))
    surface.blit(text_surface, text_rect.topleft)

def Button(surface: pygame.Surface, label: str, rect: pygame.Rect, label_font: pygame.font.Font, background_color: pygame.Color | None = None, on_click = None, event_list: list[pygame.event.Event] = []):
    mouse_pos = pygame.mouse.get_pos()
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and rect.collidepoint(event.pos):
                if on_click is not None:
                    on_click()

    is_hovered = rect.collidepoint(mouse_pos)
    btn_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    btn_opacity = 220 if is_hovered else 170 
    if background_color is not None:
        btn_surface.fill((background_color.r, background_color.g, background_color.b, btn_opacity))
    surface.blit(btn_surface, rect.topleft)
    
    text_surface = label_font.render(label, True, pygame.Color(0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    outline_color = pygame.Color(255, 255, 255)
    text_outline_surface = label_font.render(label, True, outline_color)
    outline_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    for dx, dy in outline_offsets:
        surface.blit(text_outline_surface, (text_rect.x + dx, text_rect.y + dy))
    surface.blit(text_surface, text_rect.topleft)

def ButtonIcon(surface: pygame.Surface, rect: pygame.Rect, icon: pygame.Surface, on_click = None, event_list: list[pygame.event.Event] = []):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and rect.collidepoint(event.pos):
                if on_click is not None:
                    on_click()
    surface.blit(icon, rect.topleft)

    