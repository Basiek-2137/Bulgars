import customtkinter as ctk
from core.database import Database


class LoginView(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()

        self.title("Logowanie")
        self.geometry("400x380")
        self.resizable(False, False)

        self.db = Database()
        self.on_login_success = on_login_success

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="AI Trener", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(30, 20))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nazwa użytkownika", width=250)
        self.username_entry.grid(row=1, column=0, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Hasło", show="*", width=250)
        self.password_entry.grid(row=2, column=0, pady=10)

        self.msg_label = ctk.CTkLabel(self, text="", text_color="red")
        self.msg_label.grid(row=3, column=0, pady=5)

        self.login_btn = ctk.CTkButton(self, text="Zaloguj", width=250, command=self.login)
        self.login_btn.grid(row=4, column=0, pady=10)

        self.register_btn = ctk.CTkButton(self, text="Zarejestruj", width=250, fg_color="transparent",
                                          border_width=1, text_color=("gray10", "#DCE4EE"),
                                          command=self.register)
        self.register_btn.grid(row=5, column=0, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.msg_label.configure(text="Wypełnij wszystkie pola!", text_color="red")
            return

        if self.db.verify_user(username, password):
            self.destroy()
            self.on_login_success(username)
        else:
            self.msg_label.configure(text="Błędny login lub hasło!", text_color="red")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.msg_label.configure(text="Wypełnij wszystkie pola!", text_color="red")
            return

        if self.db.register_user(username, password):
            self.msg_label.configure(text="Konto utworzone! Możesz się zalogować.", text_color="green")
        else:
            self.msg_label.configure(text="Taka nazwa użytkownika już istnieje!", text_color="red")