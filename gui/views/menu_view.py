import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VirtualTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wirtualny Trener - Logowanie")
        self.geometry("800x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = None
        self.exercise_frame = None
        self.stats_frame = None
        self.friends_frame = None

        self.login_frame = self.create_login_frame()
        self.login_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def create_login_frame(self):
        """Widok ekranu logowania"""
        frame = ctk.CTkFrame(self, corner_radius=0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(frame, text="Logowanie do systemu", font=ctk.CTkFont(size=24, weight="bold"))
        label.grid(row=1, column=0, pady=(0, 20))

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Nazwa użytkownika (np. admin)", width=250)
        self.username_entry.grid(row=2, column=0, pady=10)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Hasło (np. admin)", width=250, show="*")
        self.password_entry.grid(row=3, column=0, pady=10)

        self.error_label = ctk.CTkLabel(frame, text="", text_color="red")
        self.error_label.grid(row=4, column=0)

        login_btn = ctk.CTkButton(frame, text="Zaloguj", command=self.attempt_login, width=250,
                                  font=ctk.CTkFont(weight="bold"))
        login_btn.grid(row=5, column=0, pady=(10, 0), sticky="n")

        return frame

    def attempt_login(self):
        """Prosta weryfikacja danych"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":
            self.error_label.configure(text="")
            self.login_success()
        else:
            self.error_label.configure(text="Nieprawidłowy login lub hasło!")

    def login_success(self):
        """Akcje wykonywane po poprawnym zalogowaniu"""
        self.title("Wirtualny Trener - Menu Główne")
        self.login_frame.grid_forget()

        if not self.sidebar_frame:
            self.build_main_app()

        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.show_exercise_frame()

    def logout(self):
        """Wylogowanie użytkownika i powrót do ekranu logowania"""
        self.title("Wirtualny Trener - Logowanie")

        self.hide_all_frames()
        self.sidebar_frame.grid_forget()

        self.password_entry.delete(0, 'end')
        self.error_label.configure(text="")

        self.login_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def build_main_app(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Trener", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_exercise = ctk.CTkButton(self.sidebar_frame, text="Trening", command=self.show_exercise_frame)
        self.btn_exercise.grid(row=1, column=0, padx=20, pady=10)

        self.btn_stats = ctk.CTkButton(self.sidebar_frame, text="Statystyki", command=self.show_stats_frame)
        self.btn_stats.grid(row=2, column=0, padx=20, pady=10)

        self.btn_friends = ctk.CTkButton(self.sidebar_frame, text="Znajomi", command=self.show_friends_frame)
        self.btn_friends.grid(row=3, column=0, padx=20, pady=10)

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Wyloguj", command=self.logout, fg_color="transparent",
                                        border_width=2,
                                        text_color=("gray10", "#DCE4EE"))
        self.btn_logout.grid(row=5, column=0, padx=20, pady=20)
        self.exercise_frame = self.create_exercise_frame()
        self.stats_frame = self.create_stats_frame()
        self.friends_frame = self.create_friends_frame()

    def create_exercise_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Konfiguracja Treningu", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        ctk.CTkLabel(frame, text="Wybierz ćwiczenie:").pack(pady=(10, 0))
        exercise_combo = ctk.CTkComboBox(frame, values=["Przysiad Bułgarski (Dostępne)", "Martwy ciąg (Wkrótce)",
                                                        "Wyciskanie (Wkrótce)"], width=250)
        exercise_combo.pack(pady=(0, 20))

        ctk.CTkLabel(frame, text="Wybierz obciążenie (kg):").pack(pady=(10, 0))
        weight_slider = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=20)
        weight_slider.pack()
        weight_label = ctk.CTkLabel(frame, text="0 kg")
        weight_label.pack(pady=(0, 20))

        start_btn = ctk.CTkButton(frame, text="Rozpocznij Trening", height=40, font=ctk.CTkFont(size=16, weight="bold"),
                                  fg_color="#2FA572", hover_color="#106A43")
        start_btn.pack(pady=40)

        return frame

    def create_stats_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Twoje Statystyki", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        info_label = ctk.CTkLabel(frame,
                                  text="Tutaj pojawią się interaktywne wykresy z biblioteki Plotly.\nPokazujące historię Twoich powtórzeń i użytego ciężaru.",
                                  text_color="gray")
        info_label.pack(pady=20)

        return frame

    def create_friends_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Społeczność", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        friends_box = ctk.CTkTextbox(frame, width=300, height=150)
        friends_box.pack(pady=10)
        friends_box.insert("0.0",
                           "Wyniki znajomych:\n\n1. Jan Kowalski - 50x Przysiad Bułgarski (20kg)\n2. Anna Nowak - 30x Przysiad Bułgarski (15kg)")
        friends_box.configure(state="disabled")

        add_friend_entry = ctk.CTkEntry(frame, placeholder_text="Nazwa użytkownika...", width=200)
        add_friend_entry.pack(pady=(20, 5))

        add_friend_btn = ctk.CTkButton(frame, text="Dodaj znajomego")
        add_friend_btn.pack()

        return frame

    # ==========================================
    # LOGIKA PRZEŁĄCZANIA WIDOKÓW
    # ==========================================

    def show_exercise_frame(self):
        self.hide_all_frames()
        if self.exercise_frame:
            self.exercise_frame.grid(row=0, column=1, sticky="nsew")

    def show_stats_frame(self):
        self.hide_all_frames()
        if self.stats_frame:
            self.stats_frame.grid(row=0, column=1, sticky="nsew")

    def show_friends_frame(self):
        self.hide_all_frames()
        if self.friends_frame:
            self.friends_frame.grid(row=0, column=1, sticky="nsew")

    def hide_all_frames(self):
        if self.exercise_frame:
            self.exercise_frame.grid_forget()
        if self.stats_frame:
            self.stats_frame.grid_forget()
        if self.friends_frame:
            self.friends_frame.grid_forget()


if __name__ == "__main__":
    app = VirtualTrainerApp()
    app.mainloop()