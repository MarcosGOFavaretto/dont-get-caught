import pygame
from enum import Enum
class RectPosition(Enum):
    TOP_LEFT = 'topleft'
    CENTER = 'center'

def Text(surface: pygame.Surface, content: str, color: pygame.Color, position: tuple[int, int], font: pygame.font.Font, outline_color: pygame.Color | None = None, outline_size: int = 2, rect_pos: RectPosition = RectPosition.TOP_LEFT, line_max_width: int | None = None, line_spacing: int = 0):
    text_surface = font.render(content, True, color)
    if rect_pos == RectPosition.CENTER:
        text_rect = text_surface.get_rect(center=position)
    elif rect_pos == RectPosition.TOP_LEFT:
        text_rect = text_surface.get_rect(topleft=position)
    else:
        raise ValueError("Invalid rect_pos value. Must be 'topleft' or 'center'")
    
    words = content.split(' ')
    wrapped_lines: list[str] = []
    current_line: list[str] = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        line_width, _ = font.size(test_line)
        if line_max_width is None or line_width < line_max_width:
            current_line.append(word)
        else:
            wrapped_lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        wrapped_lines.append(' '.join(current_line))

    y_offset = 0
    for line in wrapped_lines:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(topleft=(text_rect.x, text_rect.y + y_offset))
        if outline_color:
            line_outline_surface = font.render(line, True, outline_color)
            outline_offsets = [(-outline_size, 0), (outline_size, 0), (0, -outline_size), (0, outline_size)]
            for dx, dy in outline_offsets:
                surface.blit(line_outline_surface, (line_rect.x + dx, line_rect.y + dy))
        y_offset += font.get_height() + line_spacing
        surface.blit(line_surface, (line_rect.x, line_rect.y))

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

    