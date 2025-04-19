from .teacher.teachers.sergio import TeacherSergio
from .classroom.classroom import Classroom, ClassroomRender
from .teacher.teacher import Teacher, TeacherRender
from .student.student import Student
import copy

class GameRender:
    def __init__(self, app):
        self.app = app
        self.classroom: Classroom = None
        self.teacher: Teacher = None
        self.student: Student = None

        self.teacher_render: TeacherRender = None
        self.classroom_render: ClassroomRender = None

        self.define_classroom()
        self.define_teacher()
        self.define_student()

    # Método para renderizar as entidades do jogo.
    #
    def render(self):
        self.classroom_render.render()
        self.teacher_render.render()

    # Método para encerrar o jogo e voltar para o menu.
    #
    def game_over(self):
        self.app.open_menu()

    # Define a sala de aula.
    #   - Cria uma sala de aula com as dimensões, número de linhas e colunas.
    def define_classroom(self):
        self.classroom = Classroom(dimension=(1000, 600), x=0, y=0, rows=8, columns=11)
        self.classroom_render = self.classroom.get_render(self.app.surface)

    # Define o professor do jogo.
    #   
    def define_teacher(self):
        self.teacher = TeacherSergio(game=self)
        # self.teacher = Teacher(game=self)
        self.teacher_render = self.teacher.get_render(self.app.surface)

    # Define o aluno do jogo.
    #   
    def define_student(self):
        self.student = Student(game=self, position=copy.deepcopy(self.classroom.grid_points[0][1]))