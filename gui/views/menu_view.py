import customtkinter as ctk


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, username, on_logout):
        # Inicjalizacja jako ramka, która wypełnia rodzica (transparentne tło)
        super().__init__(master, corner_radius=0, fg_color="transparent")

        self.username = username
        self.on_logout = on_logout  # Funkcja przekazana z main.py, która cofnie nas do logowania

        # --- Układ siatki ramki menu ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Tworzenie paska bocznego (Sidebar) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)  # Wypycha przycisk wylogowania na sam dół

        # Logo / Powitanie z nazwą użytkownika
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Trener", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.user_label = ctk.CTkLabel(self.sidebar_frame, text=f"Witaj, {self.username}!", text_color="gray",
                                       font=ctk.CTkFont(size=12))
        self.user_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Przyciski nawigacyjne
        self.btn_exercise = ctk.CTkButton(self.sidebar_frame, text="Trening", command=self.show_exercise_frame)
        self.btn_exercise.grid(row=2, column=0, padx=20, pady=10)

        self.btn_stats = ctk.CTkButton(self.sidebar_frame, text="Statystyki", command=self.show_stats_frame)
        self.btn_stats.grid(row=3, column=0, padx=20, pady=10)

        self.btn_friends = ctk.CTkButton(self.sidebar_frame, text="Znajomi", command=self.show_friends_frame)
        self.btn_friends.grid(row=4, column=0, padx=20, pady=10)

        # Przycisk wylogowania (korzysta z callbacku)
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Wyloguj", fg_color="transparent",
                                        border_width=2, text_color=("gray10", "#DCE4EE"), command=self.on_logout)
        self.btn_logout.grid(row=6, column=0, padx=20, pady=20)

        # --- Tworzenie ramek z zawartością (Widoki) ---
        self.exercise_frame = self.create_exercise_frame()
        self.stats_frame = self.create_stats_frame()
        self.friends_frame = self.create_friends_frame()

        # Domyślnie pokazujemy ekran ćwiczeń
        self.show_exercise_frame()

    # ==========================================
    # KREACJA WIDOKÓW
    # ==========================================

    def create_exercise_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        label = ctk.CTkLabel(frame, text="Konfiguracja Treningu", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        ctk.CTkLabel(frame, text="Wybierz ćwiczenie:").pack(pady=(10, 0))
        exercise_combo = ctk.CTkComboBox(frame, values=["Przysiad Bułgarski", "Martwy ciąg (Wkrótce)"], width=250)
        exercise_combo.pack(pady=(0, 20))

        ctk.CTkLabel(frame, text="Wybierz obciążenie (kg):").pack(pady=(10, 0))
        weight_slider = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=20)
        weight_slider.pack()

        start_btn = ctk.CTkButton(frame, text="Rozpocznij Trening", height=40, font=ctk.CTkFont(size=16, weight="bold"),
                                  fg_color="#2FA572", hover_color="#106A43")
        start_btn.pack(pady=40)
        return frame

    def create_stats_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        label = ctk.CTkLabel(frame, text="Twoje Statystyki", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))
        info_label = ctk.CTkLabel(frame, text="Miejsce na wykresy Plotly", text_color="gray")
        info_label.pack(pady=20)
        return frame

    def create_friends_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        label = ctk.CTkLabel(frame, text="Społeczność", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=(40, 20))

        friends_box = ctk.CTkTextbox(frame, width=300, height=150)
        friends_box.pack(pady=10)
        friends_box.insert("0.0", "Wyniki znajomych:\n\n1. Jan Kowalski - 50x Przysiad Bułgarski (20kg)")
        friends_box.configure(state="disabled")
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