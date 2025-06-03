import pygame
import random
from pygame import Surface

class ColaRender:
    def __init__(self, app, dificuldade=1, frase_salva=None, texto_digitado=""):
        self.app = app
        self.surface = app.surface
        self.font = pygame.font.SysFont('', 28)
        self.user_input = texto_digitado
        self.dificuldade = dificuldade
        self.cola_text = frase_salva if frase_salva else self.get_random_phrase()
        self.composicao = ""

    def get_random_phrase(self):
        frases_por_dificuldade = {
            1: [
                "A camada de ozônio protege a Terra dos raios ultravioleta do sol, evitando mutações genéticas.",
                "O ciclo da água envolve processos como evaporação, condensação e precipitação nas nuvens.",
                "A Constituição de 1988 garante direitos fundamentais como saúde, educação e segurança.",
                "A fotossíntese transforma gás carbônico e água em glicose e oxigênio com ajuda da luz solar.",
                "A Revolução Francesa alterou profundamente a organização política e social da Europa no século XVIII."
            ],
            2: [
                "O surgimento do Iluminismo no século XVIII representou uma ruptura com os paradigmas medievais e propôs a razão como elemento central na construção das sociedades modernas e democráticas.",
                "A teoria da evolução de Charles Darwin propõe que a seleção natural age sobre indivíduos com características herdáveis vantajosas, promovendo sua maior sobrevivência e reprodução ao longo de gerações.",
                "Durante a Segunda Guerra Mundial, o conflito entre as potências do Eixo e os Aliados transformou não só a geopolítica global, mas também acelerou o avanço tecnológico e o surgimento de organizações internacionais como a ONU.",
                "A energia elétrica é um vetor indispensável ao desenvolvimento das sociedades contemporâneas, sendo gerada por fontes renováveis e não renováveis que impactam diretamente a sustentabilidade ambiental.",
                "O processo de urbanização acelerada nos séculos XIX e XX provocou mudanças profundas na dinâmica social, espacial e econômica das cidades, exigindo políticas públicas eficientes e planejamento urbano integrado."
            ],
            3: [
                "A dialética hegeliana, estruturada na tríade tese-antítese-síntese, propõe uma dinâmica histórica que ultrapassa a linearidade temporal, configurando um método crítico para a análise das contradições sociais e ideológicas que impulsionam a evolução das sociedades.",
                "A formulação da mecânica quântica, com seus postulados sobre a dualidade onda-partícula, o princípio da incerteza de Heisenberg e a superposição de estados, redefine os fundamentos epistemológicos da física e desafia paradigmas clássicos do determinismo e da causalidade.",
                "A teoria dos sistemas complexos, ao estudar redes adaptativas e interações não-lineares, revela propriedades emergentes que não podem ser explicadas pela simples soma das partes, impactando profundamente campos multidisciplinares como a biologia evolutiva, economia comportamental e análise sociotécnica.",
                "As análises foucaultianas sobre poder-saber expõem as microfísicas do poder, revelando como discursos institucionais e práticas discursivas constroem regimes de verdade, disciplinam corpos e subjetividades, e moldam configurações históricas do saber e da governamentalidade.",
                "A Grande Depressão de 1929, marcada pelo colapso dos mercados financeiros globais, impulsionou o desenvolvimento do intervencionismo estatal e a formulação de políticas keynesianas, redefinindo as relações entre Estado, mercado e sociedade civil no contexto do capitalismo moderno."
            ]
        }
        frases = frases_por_dificuldade.get(self.dificuldade, frases_por_dificuldade[3])
        return random.choice(frases)

    def render(self):
        self.surface.fill((255, 255, 255))
        width, height = self.surface.get_size()

        pygame.draw.line(self.surface, (0, 0, 0), (width // 2, 0), (width // 2, height))

        self.render_multiline_text(self.cola_text, 20, 20, width // 2 - 40, (0, 0, 0))
        time = pygame.time.get_ticks()
        cursor_visible = (time // 500) % 2 == 0 

        display_input = self.user_input
        if cursor_visible:
            display_input += "|"

        self.render_multiline_text(display_input, width // 2 + 20, 20, width // 2 - 40, (0, 0, 255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.close_cola_overlay(self.cola_text, self.user_input)
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.user_input += '\n'
            else:
                letra = event.unicode
                if letra in ["´", "`", "~", "^", '"']:
                    self.composicao = letra
                elif self.composicao:
                    combinacoes = {
                        "~": {"a": "ã", "o": "õ", "e": "ẽ", "i": "ĩ", "u": "ũ",
                            "A": "Ã", "O": "Õ", "E": "Ẽ", "I": "Ĩ", "U": "Ũ"},
                        "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"},
                        "´": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
                            "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"},
                        "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û",
                            "A": "Â", "E": "Ê", "I": "Î", "O": "Ô", "U": "Û"},
                        '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü",
                            "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü"},
                    }

                    if any(letra in d.values() for d in combinacoes.values()):
                        self.user_input += letra
                    else:
                        combinado = combinacoes.get(self.composicao, {}).get(letra)
                        if combinado:
                            self.user_input += combinado
                        else:
                            self.user_input += self.composicao + letra

                    self.composicao = ""
                else:
                    self.user_input += letra

    def render_multiline_text(self, text, x, y, max_width, color):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines):
            rendered = self.font.render(line.strip(), True, color)
            self.surface.blit(rendered, (x, y + i * 30))
