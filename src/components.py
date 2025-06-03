import pygame

def Text(surface: pygame.Surface, content: str, color: pygame.Color, position: tuple[int, int], font: pygame.font.Font, outline_color: pygame.Color | None = None, outline_size: int = 2):
    text_surface = font.render(content, True, color)
    text_rect = text_surface.get_rect(center=position)
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
    
    Text(surface=surface, 
        content=label,
        color=pygame.Color(0, 0, 0),
        outline_color=pygame.Color(255, 255, 255),
        outline_size=2,
        position=rect.center,
        font=label_font)

def ButtonIcon(surface: pygame.Surface, rect: pygame.Rect, icon: pygame.Surface, on_click = None, event_list: list[pygame.event.Event] = []):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and rect.collidepoint(event.pos):
                if on_click is not None:
                    on_click()
    surface.blit(icon, rect.topleft)

    