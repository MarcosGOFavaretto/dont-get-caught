from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

from .login import AuthLogin

class AuthRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.login_screen = AuthLogin(app)

    def render(self):
        self.login_screen.render()
