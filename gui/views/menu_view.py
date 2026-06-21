import customtkinter as ctk
import cv2
import sys
import os
from PIL import Image, ImageTk
from vision import CameraManager, PoseDetector
from data import GeminiCoach
from core.database import Database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VirtualTrainerApp(ctk.CTk):
    def __init__(self,username):
        super().__init__()

        self.title("Wirtualny Trener - Cyfrowy Asystent Treningu")
        self.geometry("1100x650")

        self.db = Database(db_name="virtual_trainer.db")
        self.current_user = username
        self.user_lang = self.db.get_user_language(self.current_user) or "pl"

        self.cam = None
        self.posse = None
        self.is_training_active = False
        self.target_reps = 10

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Trener", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_menu = ctk.CTkButton(self.sidebar_frame, text="Panel Treningu", command=self.show_menu_view)
        self.btn_menu.grid(row=1, column=0, padx=20, pady=10)

        self.btn_stats = ctk.CTkButton(self.sidebar_frame, text="Statystyki", command=self.show_stats_view)
        self.btn_stats.grid(row=2, column=0, padx=20, pady=10)

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Wyloguj", fg_color="crimson", hover_color="darkred",
                                        command=self.logout)
        self.sidebar_frame.grid_propagate(False)
        self.btn_logout.grid(row=5, column=0, padx=20, pady=20)

        self.main_container = ctk.CTkFrame(self, corner_radius=10)
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.create_menu_view()
        self.create_stats_view()

        self.show_menu_view()

    def create_menu_view(self):
        """Tworzy panel konfiguracji i wbudowany odtwarzacz wideo w jednym widoku"""
        self.menu_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")

        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=3)
        self.menu_frame.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkFrame(self.menu_frame, width=250)
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(left_panel, text="Konfiguracja serii", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        label_ex = ctk.CTkLabel(left_panel, text="Wybierz ćwiczenie:")
        label_ex.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.exercise_combo = ctk.CTkOptionMenu(left_panel,
                                                values=["Przysiad Bułgarski", "Przysiad Klasyczny (Wkrótce)"])
        self.exercise_combo.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        label_reps = ctk.CTkLabel(left_panel, text="Liczba powtórzeń:")
        label_reps.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.reps_entry = ctk.CTkEntry(left_panel, placeholder_text="10")
        self.reps_entry.insert(0, "10")
        self.reps_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_action = ctk.CTkButton(left_panel, text="Rozpocznij Trening", fg_color="green",
                                        hover_color="darkgreen", command=self.toggle_training)
        self.btn_action.grid(row=5, column=0, padx=20, pady=30, sticky="ew")

        self.right_panel = ctk.CTkFrame(self.menu_frame, fg_color="black")
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.video_display = ctk.CTkLabel(self.right_panel,
                                          text="KAMERA WYŁĄCZONA\nSkonfiguruj parametry i kliknij przycisk Start",
                                          font=ctk.CTkFont(size=14))
        self.video_display.grid(row=0, column=0, sticky="nsew")

    def create_stats_view(self):
        """Tworzy panel statystyk (Zabezpieczenie integracji z bazą danych)"""
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")

        stats_label = ctk.CTkLabel(self.stats_frame, text="Historia Twoich Treningów",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        stats_label.pack(pady=20)

        self.data_container = ctk.CTkTextbox(self.stats_frame, width=500, height=300)
        self.data_container.insert("0.0",
                                   "Tutaj ładowane są dane z bazy danych sesji treningowych...\nFunkcja bazy danych działa prawidłowo.")
        self.data_container.configure(state="disabled")
        self.data_container.pack(pady=10)

    def show_menu_view(self):
        self.stats_frame.grid_forget()
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

    def show_stats_view(self):
        self.menu_frame.grid_forget()
        self.stats_frame.grid(row=0, column=0, sticky="nsew")

        top_users = self.db.get_top_users()
        stats_text = "TOP 10 UŻYTKOWNIKÓW (Liczba sesji):\n\n"
        for i, (user, count) in enumerate(top_users, 1):
            stats_text += f"{i}. {user} - {count} sesji\n"

        self.data_container.configure(state="normal")
        self.data_container.delete("0.0", "end")
        self.data_container.insert("0.0", stats_text)
        self.data_container.configure(state="disabled")


    def toggle_training(self):
        """Przełącza stan sesji treningowej między aktywnym a nieaktywnym"""
        if self.is_training_active:
            self.stop_training_session()
        else:
            self.start_training_session()

    def start_training_session(self):
        """Inicjuje proces treningu, rozpoczynając od 10-sekundowego odliczania."""
        wybrane_cwiczenie = self.exercise_combo.get()
        if "Wkrótce" in wybrane_cwiczenie:
            return

        try:
            self.target_reps = int(self.reps_entry.get())
        except ValueError:
            self.target_reps = 10

        self.is_training_active = True

        self.btn_action.configure(text="Zatrzymaj", fg_color="crimson", hover_color="darkred",
                                  command=self.stop_training_session)
        self.btn_menu.configure(state="disabled")
        self.btn_stats.configure(state="disabled")

        self.countdown_time = 10


        self.run_countdown()

    def run_countdown(self):
        """Asynchroniczna pętla odliczająca czas przed włączeniem kamery."""
        if not self.is_training_active:
            return

        if self.countdown_time > 0:
            self.video_display.configure(
                text=f"PRZYGOTUJ SIĘ!\n\nStart za:\n{self.countdown_time}",
                font=ctk.CTkFont(size=40, weight="bold")
            )
            self.countdown_time -= 1
            self.after(1000, self.run_countdown)
        else:
            self.video_display.configure(text="ŁADOWANIE KAMERY...", font=ctk.CTkFont(size=20))
            self.begin_actual_camera_capture()

    def begin_actual_camera_capture(self):
        """Tutaj znajduje się stary kod z Twojej funkcji start_training_session."""
        self.posse = PoseDetector()
        self.all_session_errors = []

        self.cam = CameraManager(self.posse, 0)
        self.update_video_stream()

    def update_video_stream(self):
        if not self.is_training_active or self.cam is None or not self.cam.cap.isOpened():
            return

        ret, frame = self.cam.cap.read()
        if not ret:
            self.stop_training_session()
            return

        frame = self.posse.detect(frame)
        punkty_bulgarskie = self.posse.get_landmarks(frame)
        raport = self.posse.verify_bulgarian_split_squat(punkty_bulgarskie, working_leg='prawa_noga')

        if raport["errors"]:
            for err in raport["errors"]:
                if err not in self.all_session_errors:
                    self.all_session_errors.append(err)

        frame = self.cam.draw_trainer_hud(frame, raport, target_reps=self.target_reps)

        self.last_completed_reps = raport["counter"]

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)

        display_width = self.right_panel.winfo_width()
        display_height = self.right_panel.winfo_height()
        if display_width < 10 or display_height < 10:
            display_width, display_height = 640, 480

        pil_img = pil_img.resize((display_width, display_height), Image.Resampling.LANCZOS)
        tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(display_width, display_height))
        self.video_display.configure(image=tk_img, text="")
        self.video_display.image = tk_img

        if raport["counter"] >= self.target_reps:
            try:
                self.cam.voice.speak("Koniec serii, świetna robota!", override=True)
            except AttributeError:
                pass
            self.stop_training_session()
            return

        self.after(33, self.update_video_stream)

    def stop_training_session(self):
        """Zatrzymuje trening, zapisuje sesję i pokazuje raport AI."""
        self.is_training_active = False

        self.db.save_training_session(self.current_user)

        print("Trwa generowanie podsumowania przez AI Coach...")
        coach = GeminiCoach()
        feedback = coach.generate_workout_feedback(
            exercise_name=self.exercise_combo.get(),
            target_reps=self.target_reps,
            completed_reps=getattr(self, 'last_completed_reps', 0),
            errors_list=getattr(self, 'all_session_errors', [])
        )

        self.show_feedback_popup(feedback)

        if self.cam:
            self.cam.stop()
            self.cam = None
        self.posse = None

        self.btn_action.configure(text="Rozpocznij Trening", fg_color="green")
        self.btn_menu.configure(state="normal")
        self.btn_stats.configure(state="normal")

        self.show_stats_view()

    def logout(self):
        if self.is_training_active:
            self.stop_training_session()
        print("Wylogowywanie z systemu...")
        self.destroy()

    def show_feedback_popup(self, feedback_text):
        """Tworzy osobne okno typu popup dla raportu AI."""
        popup = ctk.CTkToplevel(self)
        popup.title("Raport Trenera AI")
        popup.geometry("400x400")

        textbox = ctk.CTkTextbox(popup, width=350, height=300)
        textbox.pack(padx=20, pady=20)
        textbox.insert("0.0", feedback_text)
        textbox.configure(state="disabled")

        btn_close = ctk.CTkButton(popup, text="Zamknij", command=popup.destroy)
        btn_close.pack(pady=10)



if __name__ == "__main__":
    app = VirtualTrainerApp()
    app.mainloop()
