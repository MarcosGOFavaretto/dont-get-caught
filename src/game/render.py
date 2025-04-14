from pygame import Surface
from .classroom.classroom import Classroom
from .teacher.teacher import Teacher

class GameRender:
    def __init__(self, app):
        self.app = app
        self.classroom: Classroom = None
        self.teacher: Teacher = None
        self.define_classroom()
        self.define_teacher()

    # Método para renderizar as entidades do jogo.
    #
    def render(self):
        self.classroom.get_render(self.app.surface).render()
        self.teacher.get_render(self.app.surface).render()


    # Método para encerrar o jogo e voltar para o menu.
    #
    def game_over(self):
        self.app.open_menu()

    # Define a sala de aula.
    #   - Cria uma sala de aula com as dimensões, número de linhas e colunas.
    def define_classroom(self):
        self.classroom = Classroom(dimension=(1000, 600), x=0, y=0, rows=8, columns=11)

    # Define o professor.
    #   - Cria um professor com nome e posição inicial.
    def define_teacher(self):
        self.teacher = Teacher(name='Oliver Taz', initial_position=self.classroom.grid_points[0][0], game=self)