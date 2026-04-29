import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="virtual_trainer.db"):
        self.db_name = db_name
        self._create_tables()

    def _execute_query(self, query, parameters=(), fetch=False, fetch_all=True):
        """Pomocnicza metoda do wykonywania zapytań SQL."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            if fetch:
                return cursor.fetchall() if fetch_all else cursor.fetchone()
            conn.commit()

    def _create_tables(self):
        """Tworzy tabele, jeśli jeszcze nie istnieją."""
        # Tabela użytkowników
        self._execute_query('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Tabela treningów
        self._execute_query('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                exercise_name TEXT,
                weight REAL,
                reps INTEGER,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # Dodanie testowego użytkownika, jeśli tabela jest pusta
        if not self.get_user("admin"):
            self.add_user("admin", "admin123")
            self.add_user("test", "test")

    # ==========================================
    # LOGIKA KONT (Logowanie i Rejestracja)
    # ==========================================

    def add_user(self, username, password):
        try:
            self._execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return True
        except sqlite3.IntegrityError:
            return False  # Użytkownik o tej nazwie już istnieje

    def get_user(self, username):
        return self._execute_query("SELECT * FROM users WHERE username = ?", (username,), fetch=True, fetch_all=False)

    def verify_login(self, username, password):
        user = self.get_user(username)
        if user and user[2] == password:  # index 2 to hasło w naszej tabeli
            return user[0]  # Zwracamy ID użytkownika
        return None

    # ==========================================
    # LOGIKA TRENINGÓW (Zapis i Odczyt)
    # ==========================================

    def save_workout(self, user_id, exercise_name, weight, reps):
        """Zapisuje wynik zakończonego treningu."""
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._execute_query('''
            INSERT INTO workouts (user_id, exercise_name, weight, reps, date) 
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, exercise_name, weight, reps, date_now))

    def get_user_workouts(self, user_id):
        """Pobiera historię treningów (przyda się do Plotly i Gemini)."""
        return self._execute_query('''
            SELECT exercise_name, weight, reps, date 
            FROM workouts 
            WHERE user_id = ? 
            ORDER BY date DESC
        ''', (user_id,), fetch=True)


# --- Prosty test lokalny ---
if __name__ == "__main__":
    db = DatabaseManager()

    # Symulacja: logowanie
    user_id = db.verify_login("admin", "admin123")
    print(f"ID zalogowanego użytkownika: {user_id}")

    # Symulacja: zapis treningu
    if user_id:
        db.save_workout(user_id, "Przysiad Bułgarski", 20.0, 15)
        db.save_workout(user_id, "Przysiad Bułgarski", 25.0, 12)

        # Odczyt do statystyk
        historia = db.get_user_workouts(user_id)
        print("\nHistoria treningów:")
        for trening in historia:
            print(trening)