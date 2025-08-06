import pygame_gui
import pygame

from ..config import WINDOW_WIDTH, WINDOW_HEIGHT

def show_error_toast(manager: pygame_gui.UIManager, message: str, toast_rect_arg: pygame.Rect | None = None ):
    toast_width = 600
    toast_height = 60
    toast_rect = pygame.Rect((WINDOW_WIDTH // 2 - toast_width // 2, WINDOW_HEIGHT // 2 - toast_height // 2), (toast_width, toast_height)) if toast_rect_arg is None else toast_rect_arg
    # Create a small popup window with no title bar (or minimal)
    toast = pygame_gui.elements.UIWindow(
        rect=toast_rect,
        manager=manager,
        window_display_title='Erro',
        object_id="#error_toast"
    )
    # Add a label with the error message inside the window
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((5, 5), (toast_width, toast_height // 2)),
        text=message,
        manager=manager,
        container=toast,
        object_id="#error_toast_label"
    )

    return toast

def show_success_toast(manager: pygame_gui.UIManager, message: str, toast_rect_arg: pygame.Rect | None = None ):
    toast_width = 600
    toast_height = 60
    toast_rect = pygame.Rect((WINDOW_WIDTH // 2 - toast_width // 2, WINDOW_HEIGHT // 2 - toast_height // 2), (toast_width, toast_height)) if toast_rect_arg is None else toast_rect_arg
    # Create a small popup window with no title bar (or minimal)
    toast = pygame_gui.elements.UIWindow(
        rect=toast_rect,
        manager=manager,
        window_display_title='Sucesso',
        object_id="#error_toast"
    )
    # Add a label with the error message inside the window
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((5, 5), (toast_width, toast_height // 2)),
        text=message,
        manager=manager,
        container=toast,
        object_id="#error_toast_label"
    )

    return toast