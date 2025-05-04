import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

background = pygame.image.load(r"C:\pygame\img\image1.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
BTNMOUSE = 150  #Transparência do botão aumenta ao passar o mouse sobre ele

font = pygame.font.Font(r"C:\pygame\font\font.ttf", 32)

btn = [
    {"text": "INICIAR", "rect": pygame.Rect(268, 260, 260, 50)},
    {"text": "OPCOES", "rect": pygame.Rect(280, 340, 240, 50)},
    {"text": "SAIR", "rect": pygame.Rect(300, 420, 200, 50)}
]

btndificuldade = [
    {"text": "FACIL", "rect": pygame.Rect(300, 260, 200, 50)},
    {"text": "MEDIO", "rect": pygame.Rect(300, 340, 200, 50)},
    {"text": "DIFICIL", "rect": pygame.Rect(273, 420, 250, 50)}
]

btnvoltar = {"text": "VOLTAR", "rect": pygame.Rect(300, 500, 200, 50)}

menu_active = True
difficulty_menu_active = False

def draw_text_with_outline(text, font, text_color, outline_color, position):
    textsurface = font.render(text, True, text_color)
    outlinesurface = font.render(text, True, outline_color)
    textrect = textsurface.get_rect(center=position)
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    for dx, dy in offsets:
        screen.blit(outlinesurface, (textrect.x + dx, textrect.y + dy))
    screen.blit(textsurface, textrect.topleft)

def draw_buttons(button_list):
    mouse_pos = pygame.mouse.get_pos() #Pega a posição do mouse

    #'for' usado para detectar se o mouse está sobre o botão
    for button in button_list:
        is_hovered = button["rect"].collidepoint(mouse_pos)
        btnmouse = BTNMOUSE if is_hovered else 100  #Se passar o mouse no botão, diminui a transparência dele
        
        surfacebtn = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
        surfacebtn.fill((255, 255, 255, btnmouse))
        screen.blit(surfacebtn, button["rect"].topleft)
        
        draw_text_with_outline(button["text"], font, PRETO, BRANCO, button["rect"].center)

running = True
while running:
    screen.blit(background, (0, 0))
    
    if menu_active:
        draw_buttons(btn)
    elif difficulty_menu_active:
        draw_buttons(btndificuldade)
        draw_text_with_outline(btnvoltar["text"], font, PRETO, BRANCO, btnvoltar["rect"].center)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                for button in btn:
                    if button["rect"].collidepoint(event.pos):
                        if button["text"] == "INICIAR":
                            menu_active = False
                            difficulty_menu_active = True
                        elif button["text"] == "SAIR":
                            pygame.quit()
                            exit()
            elif difficulty_menu_active:
                for button in btndificuldade:
                    if button["rect"].collidepoint(event.pos):
                        print(f"Dificuldade selecionada: {button['text']}")
                if btnvoltar["rect"].collidepoint(event.pos):
                    menu_active = True
                    difficulty_menu_active = False
    
    pygame.display.flip()

pygame.quit()