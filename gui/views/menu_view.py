import customtkinter as ctk

# Ustawienia motywu aplikacji
ctk.set_appearance_mode("System")  # Tryb jasny/ciemny na podstawie systemu
ctk.set_default_color_theme("blue")  # Kolor przewodni


class VirtualTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wirtualny Trener - Menu Główne")
        self.geometry("800x500")

        # --- Układ siatki (Grid Layout) ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Tworzenie paska bocznego (Sidebar) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Trener", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Przyciski odpowiadające za "Wybór: Statystyki / Ćwiczenia / Znajomi" z diagramu aktywności
        self.btn_exercise = ctk.CTkButton(self.sidebar_frame, text="Trening", command=self.show_exercise_frame)
        self.btn_exercise.grid(row=1, column=0, padx=20, pady=10)

        self.btn_stats = ctk.CTkButton(self.sidebar_frame, text="Statystyki", command=self.show_stats_frame)
        self.btn_stats.grid(row=2, column=0, padx=20, pady=10)

        self.btn_friends = ctk.CTkButton(self.sidebar_frame, text="Znajomi", command=self.show_friends_frame)
        self.btn_friends.grid(row=3, column=0, padx=20, pady=10)

        # Wylogowanie / Zmiana profilu z początku diagramu
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Wyloguj", fg_color="transparent", border_width=2,
                                        text_color=("gray10", "#DCE4EE"))
        self.btn_logout.grid(row=5, column=0, padx=20, pady=20)

        # --- Tworzenie ramek głównych (Widoki) ---
        self.exercise_frame = self.create_exercise_frame()
        self.stats_frame = self.create_stats_frame()
        self.friends_frame = self.create_friends_frame()

        # Domyślnie pokazujemy ekran ćwiczeń
        self.show_exercise_frame()

    # ==========================================
    # WIDOKI (FRAMES)
    # ==========================================

    def create_exercise_frame(self):
        """Widok konfiguracji i uruchamiania treningu"""
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Konfiguracja Treningu", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        # "Wybór ćwiczenia (tymczasowo tylko bułgarski)"
        ctk.CTkLabel(frame, text="Wybierz ćwiczenie:").pack(pady=(10, 0))
        exercise_combo = ctk.CTkComboBox(frame, values=["Przysiad Bułgarski (Dostępne)", "Martwy ciąg (Wkrótce)",
                                                        "Wyciskanie (Wkrótce)"], width=250)
        exercise_combo.pack(pady=(0, 20))

        # "Wybór ciężaru"
        ctk.CTkLabel(frame, text="Wybierz obciążenie (kg):").pack(pady=(10, 0))
        weight_slider = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=20)
        weight_slider.pack()
        weight_label = ctk.CTkLabel(frame, text="0 kg")  # Opcjonalnie można tu dodać dynamiczne odświeżanie wartości
        weight_label.pack(pady=(0, 20))

        # Przejście do "Wyświetlenie GUI asystenta ćwiczenia"
        start_btn = ctk.CTkButton(frame, text="Rozpocznij Trening", height=40, font=ctk.CTkFont(size=16, weight="bold"),
                                  fg_color="#2FA572", hover_color="#106A43")
        start_btn.pack(pady=40)

        return frame

    def create_stats_frame(self):
        """Widok ze statystykami - tu później wejdzie biblioteka Plotly"""
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Twoje Statystyki", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        # "Wyświetlanie statystyk poprzednich ćwiczeń"
        info_label = ctk.CTkLabel(frame,
                                  text="Tutaj pojawią się interaktywne wykresy z biblioteki Plotly.\nPokazujące historię Twoich powtórzeń i użytego ciężaru.",
                                  text_color="gray")
        info_label.pack(pady=20)

        return frame

    def create_friends_frame(self):
        """Widok funkcji społecznościowych"""
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        label = ctk.CTkLabel(frame, text="Społeczność", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        # "Wyświetlanie wyników znajomych"
        friends_box = ctk.CTkTextbox(frame, width=300, height=150)
        friends_box.pack(pady=10)
        friends_box.insert("0.0",
                           "Wyniki znajomych:\n\n1. Jan Kowalski - 50x Przysiad Bułgarski (20kg)\n2. Anna Nowak - 30x Przysiad Bułgarski (15kg)")
        friends_box.configure(state="disabled")  # Tylko do odczytu

        # "Dodanie znajomych"
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
        self.exercise_frame.grid(row=0, column=1, sticky="nsew")

    def show_stats_frame(self):
        self.hide_all_frames()
        self.stats_frame.grid(row=0, column=1, sticky="nsew")

    def show_friends_frame(self):
        self.hide_all_frames()
        self.friends_frame.grid(row=0, column=1, sticky="nsew")

    def hide_all_frames(self):
        self.exercise_frame.grid_forget()
        self.stats_frame.grid_forget()
        self.friends_frame.grid_forget()


if __name__ == "__main__":
    app = VirtualTrainerApp()
    app.mainloop()