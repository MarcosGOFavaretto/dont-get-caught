from .teacher.teachers.sergio import TeacherSergio
from .classroom.classroom import Classroom, ClassroomRender
from .teacher.teacher import Teacher, TeacherRender
from .student.student import Student, StudentRender
import copy
from ..timer import Timer, time_to_string, TIME_SECOND
from ..config import WINDOW_WIDTH
import pygame
from ..config import ASSETS_FOLDER, EXAM_TIME
from ..fonts import merriweather
from .game_over import GameOver
from .you_win import YouWin
from .options_menu import OptionsMenu
import random
from .classroom.desk import ClassroomNpcDesk
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App
from ..components import ButtonIcon
import time

class GameRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.npc_students_fill_rate = 0.8
        self.clock_tick_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/clock-tick.mp3')
        self.clock_tick_sound.set_volume(0.3)
        self.exam_timer = Timer(wait_time=EXAM_TIME)
        self.game_final_screen = None
        self.game_ends = False

        self.game_options_icon = pygame.image.load(f'{ASSETS_FOLDER}/icons/settings-icon.png')
        self.game_options_icon = pygame.transform.scale(self.game_options_icon, (26, 26)) 

        self.options_menu = OptionsMenu(self)
        self.show_options = False

        self.started = False
        self.animation_classroom_offset = 200
        self.animation_control = 0
        self.start_animation_timer = Timer(wait_time=2 * TIME_SECOND)
        self.start_animation_timer.start()

        self.classroom, self.classroom_render = self.define_classroom()
        self.teacher, self.teacher_render = self.define_teacher()
        self.student, self.student_render = self.define_student()
        self.define_npc_students()

    # Método para renderizar as entidades do jogo.
    #
    def render(self):
        self.app.surface.fill('oldlace')

        self.classroom_render.render()
        self.teacher_render.render()
        self.student_render.render()

        if not self.started:
            self.animate_game_start()

        if self.started:
            self.render_clock()
        self.render_game_options_button()
        if self.show_options:
            self.render_game_options_menu()

        if self.game_ends and self.game_final_screen:
            self.game_final_screen.render()

    def start_game(self):
        self.started = True
        self.exam_timer.start()
        self.classroom.y = 0

    def animate_game_start(self):
        if self.animation_control >= self.animation_classroom_offset:
            self.start_game()
            return
        animation_fn = lambda t: t**1.3 / 10000
        animation_speed = animation_fn(self.start_animation_timer.get_time_passed())
        self.classroom.y -= animation_speed
        self.teacher.position.y -= animation_speed
        self.student.position.y -= animation_speed
        self.animation_control += animation_speed
        self.classroom.update_grid_points_position()


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
    
    def render_game_options_menu(self):
        def hide_options():
            self.show_options = False
        self.options_menu.render(on_close_menu=hide_options)

    def render_game_options_button(self):
        def show_options():
            self.show_options = True
        ButtonIcon(self.app.surface, pygame.rect.Rect(WINDOW_WIDTH - 50, 10, 40, 40), self.game_options_icon, on_click=show_options)

    def game_over(self):
        self.game_final_screen = GameOver(game=self)
        self.exam_timer.stop()
        self.game_ends = True

    def you_win(self):
        self.game_final_screen = YouWin(game=self)
        self.exam_timer.stop()
        self.game_ends = True

    # MÉTODOS DE DEFINIÇÃO INICIAL DO JOGO

    def define_classroom(self) -> tuple[Classroom, ClassroomRender]:
        classroom = Classroom(game=self, dimension=(1000, 600), x=0, y=self.animation_classroom_offset, rows=8, columns=11)
        classroom_render = classroom.get_render(self.app.surface)
        return (classroom, classroom_render)

    def define_teacher(self) -> tuple[Teacher, TeacherRender]:
        teacher = TeacherSergio(game=self)
        teacher_render = teacher.get_render(self.app.surface)
        return (teacher, teacher_render)

    def define_student(self) -> tuple[Student, StudentRender]:
        desk_points = self.classroom.get_desk_points()
        column, row = random.choice(desk_points).to_grid_point()
        self.classroom.get_total_desks()
        student = Student(game=self, position=copy.deepcopy(self.classroom.grid_points[column][row]))
        student_render = student.get_render(self.app.surface)
        return (student, student_render)
    
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