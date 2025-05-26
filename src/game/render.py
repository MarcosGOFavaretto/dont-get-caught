from .teacher.teachers.sergio import TeacherSergio
from .classroom.classroom import Classroom, ClassroomRender
from .teacher.teacher import Teacher, TeacherRender
from .student.student import Student
import copy
from ..timer import Timer, time_to_string, TIME_SECOND
import pygame
from ..config import ASSETS_FOLDER, EXAM_TIME
from ..fonts import merriweather
from .game_over import GameOver
from .you_win import YouWin

class GameRender:
    def __init__(self, app):
        self.app = app
        self.classroom, self.classroom_render = self.define_classroom()
        self.teacher, self.teacher_render = self.define_teacher()
        self.student: Student = self.define_student()
        self.clock_tick_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/clock-tick.mp3')
        self.clock_tick_sound.set_volume(0.3)
        self.exam_timer = Timer(wait_time=EXAM_TIME)
        self.exam_timer.start()
        self.game_final_screen = None
        self.game_ends = False


    # Método para renderizar as entidades do jogo.
    #
    def render(self):
        self.app.surface.fill((255, 255, 255))

        if self.classroom_render: self.classroom_render.render()
        if self.teacher_render: self.teacher_render.render()
        self.render_clock()

        if self.game_ends and self.game_final_screen:
            self.game_final_screen.render()

    def render_clock(self):
        time_str = time_to_string(EXAM_TIME - self.exam_timer.get_time_passed() + TIME_SECOND)
        s = merriweather.render(time_str, True, 'black', 'white')
        self.app.surface.blit(s, (10, 10))

        if self.game_ends:
            return

        if self.exam_timer.time_is_up():
            self.game_over()
            return

        if self.exam_timer.tick():
            self.clock_tick_sound.play()

    def game_over(self):
        self.game_final_screen = GameOver(game=self)
        self.exam_timer.stop()
        self.game_ends = True

    def you_win(self):
        self.game_final_screen = YouWin(game=self)
        self.exam_timer.stop()
        self.game_ends = True

    # Define a sala de aula.
    #   - Cria uma sala de aula com as dimensões, número de linhas e colunas.
    def define_classroom(self) -> tuple[Classroom, ClassroomRender]:
        classroom = Classroom(dimension=(1000, 600), x=0, y=0, rows=8, columns=11)
        classroom_render = classroom.get_render(self.app.surface)
        return (classroom, classroom_render)

    # Define o professor do jogo.
    #   
    def define_teacher(self) -> tuple[Teacher, TeacherRender]:
        teacher = TeacherSergio(game=self)
        # self.teacher = Teacher(game=self)
        teacher_render = teacher.get_render(self.app.surface)
        return (teacher, teacher_render)

    # Define o aluno do jogo.
    #   
    def define_student(self) -> Student:
        student = Student(game=self, position=copy.deepcopy(self.classroom.grid_points[4][3]))
        return student