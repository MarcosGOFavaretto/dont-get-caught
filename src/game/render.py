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
import random
from .classroom.desk import ClassroomNpcDesk
class GameRender:
    def __init__(self, app):
        self.app = app
        self.npc_students_fill_rate = 0.7
        self.clock_tick_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/clock-tick.mp3')
        self.clock_tick_sound.set_volume(0.3)
        self.exam_timer = Timer(wait_time=EXAM_TIME)
        self.exam_timer.start()
        self.game_final_screen = None
        self.game_ends = False
        self.classroom, self.classroom_render = self.define_classroom()
        self.teacher, self.teacher_render = self.define_teacher()
        self.student: Student = self.define_student()
        self.define_npc_students()

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
        classroom = Classroom(game=self, dimension=(1000, 600), x=0, y=0, rows=8, columns=11)
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
        column, row = (4, 3)
        student = Student(game=self, position=copy.deepcopy(self.classroom.grid_points[column][row]))
        return student
    
    def define_npc_students(self):
        for grid_column in self.classroom.grid_points:
            for grid_point in grid_column:
                if self.classroom.is_student_desk(grid_point.column, grid_point.row):
                    classroom_desk = ClassroomNpcDesk(grid_position=copy.deepcopy(self.classroom.grid_points[grid_point.column][grid_point.row]), has_student=False)
                    self.classroom.grid_points[grid_point.column][grid_point.row].classroom_desk = classroom_desk

        npc_students_quant = int(self.classroom.get_total_desks() * self.npc_students_fill_rate)
        for _ in range(npc_students_quant):
            random_desk = self.get_random_desk_without_student()
            random_desk.has_student = True

    def get_random_desk_without_student(self) :
        while True:
            random_grid_point = random.choice(self.classroom.get_grid_points_list())
            grid_point = self.classroom.grid_points[random_grid_point.column][random_grid_point.row]
            if grid_point.classroom_desk is not None and not grid_point.classroom_desk.has_student:
                return grid_point.classroom_desk