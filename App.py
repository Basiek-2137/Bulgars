from gui.views.menu_view import VirtualTrainerApp
from gui.views.login_view import LoginView

def start_main_app(username):
    app = VirtualTrainerApp(username)
    app.mainloop()

if __name__ == "__main__":
    login_window = LoginView(on_login_success=start_main_app)
    login_window.mainloop()