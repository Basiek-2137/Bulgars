import customtkinter as ctk


class LoginFrame(ctk.CTkFrame):
    # Dodaliśmy db_manager jako argument
    def __init__(self, master, db_manager, on_login_success):
        super().__init__(master)
        self.db = db_manager  # Referencja do bazy danych
        self.on_login_success = on_login_success

        # Konfiguracja układu ramki
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # --- Elementy GUI ---
        self.title_label = ctk.CTkLabel(self, text="Wirtualny Trener", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=30, pady=(0, 20))

        self.subtitle_label = ctk.CTkLabel(self, text="Zaloguj się do swojego profilu", font=ctk.CTkFont(size=14))
        self.subtitle_label.grid(row=2, column=0, padx=30, pady=(0, 30))

        self.username_entry = ctk.CTkEntry(self, width=300, placeholder_text="Nazwa użytkownika")
        self.username_entry.grid(row=3, column=0, padx=30, pady=10)

        self.password_entry = ctk.CTkEntry(self, width=300, show="*", placeholder_text="Hasło")
        self.password_entry.grid(row=4, column=0, padx=30, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=ctk.CTkFont(size=12))
        self.error_label.grid(row=5, column=0, padx=30, pady=5)

        self.login_button = ctk.CTkButton(self, text="Zaloguj się", width=300, height=40,
                                          command=self.login_event, font=ctk.CTkFont(size=15, weight="bold"))
        self.login_button.grid(row=6, column=0, padx=30, pady=(20, 10))

        # Opcja rejestracji z podpiętym zdarzeniem kliknięcia
        self.register_label = ctk.CTkLabel(self, text="Nie masz konta? Załóż je tutaj (Kliknij)",
                                           font=ctk.CTkFont(size=12, underline=True), cursor="hand2")
        self.register_label.grid(row=7, column=0, padx=30, pady=(0, 20))
        self.register_label.bind("<Button-1>", self.register_event)  # Nasłuchiwanie kliknięcia myszką

    def login_event(self):
        """Logika weryfikacji danych logowania z bazy SQLite"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Wypełnij wszystkie pola!", text_color="red")
            return

        # Prawdziwe zapytanie do bazy danych
        user_id = self.db.verify_login(username, password)

        if user_id:
            self.error_label.configure(text="")
            # Przekazujemy username i user_id wyżej do aplikacji
            self.on_login_success(username, user_id)
        else:
            self.error_label.configure(text="Niepoprawna nazwa użytkownika lub hasło", text_color="red")

    def register_event(self, event):
        """Prosta logika rejestracji nowego użytkownika"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Wpisz dane w pola wyżej, aby się zarejestrować.", text_color="orange")
            return

        success = self.db.add_user(username, password)
        if success:
            self.error_label.configure(text="Konto utworzone! Możesz się teraz zalogować.", text_color="green")
            self.password_entry.delete(0, 'end')  # Czyścimy hasło po rejestracji
        else:
            self.error_label.configure(text="Taka nazwa użytkownika już istnieje!", text_color="red")