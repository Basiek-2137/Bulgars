import customtkinter as ctk
# Importujemy menedżera bazy danych do obsługi profilu użytkownika
from data.db_client import DatabaseManager
from gui.views.login_view import LoginFrame
from gui.views.menu_view import MenuFrame


class VirtualTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()

        self.title("Wirtualny Trener - AI")
        self.geometry("900x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_user_name = None
        self.current_user_id = None
        self.current_frame = None
        self.show_login_screen()

    def show_login_screen(self):
        """Wyświetla ramkę logowania i wstrzykuje do niej menedżera bazy danych."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(
            master=self,
            db_manager=self.db,
            on_login_success=self.show_main_menu
        )
        self.current_frame.grid(row=0, column=0, padx=20, pady=20)

    def show_main_menu(self, username, user_id):
        """
        Niszczy ekran logowania i wyświetla menu główne.
        Wywoływana przez LoginFrame po poprawnej weryfikacji w bazie danych.
        """
        self.current_user_name = username
        self.current_user_id = user_id

        print(f"Sesja rozpoczęta: {self.current_user_name} (ID: {self.current_user_id})")

        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = MenuFrame(
            master=self,
            username=self.current_user_name,
            on_logout=self.show_login_screen
        )
        self.current_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = VirtualTrainerApp()
    app.mainloop()