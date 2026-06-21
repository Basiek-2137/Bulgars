import sqlite3
import hashlib
import os


class Database:
    def __init__(self, db_name: str = "virtual_trainer.db") -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)

        self.db_name = db_name
        self.db_path = os.path.join(base_dir, db_name)

        self.create_table()
        # self.seed_database()
        print(f"Nawiązywanie połączenia z bazą danych pod adresem: {self.db_path}")

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create_table(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    preferred_language TEXT DEFAULT 'pl',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS training_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

    def register_user(self, username: str, password: str) -> bool:
        hashed_pw = self._hash_password(password)
        query = "INSERT INTO users (username, password_hash) VALUES (?, ?);"
        print(f"Próba rejestracji użytkownika: {username}")
        try:
            with self._get_connection() as conn:
                conn.execute(query, (username, hashed_pw))
                conn.commit()
            print("Rejestracja udana.")
            return True
        except sqlite3.IntegrityError as e:
            print(f"Błąd rejestracji (prawdopodobnie zajęty login): {e}")
            return False

    def verify_user(self, username: str, password: str) -> bool:
        hashed_pw = self._hash_password(password)
        query = "SELECT id FROM users WHERE username = ? AND password_hash = ?;"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, hashed_pw))
            return cursor.fetchone() is not None

    def get_user_language(self, username: str):
        """Pobiera język użytkownika z bazy."""
        query = "SELECT preferred_language FROM users WHERE username = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def add_user(self, username: str, lang: str):
        """Dodaje użytkownika bez hasła (dla celów testowych Twojego menu)."""
        query = "INSERT INTO users (username, password_hash, preferred_language) VALUES (?, ?, ?);"
        with self._get_connection() as conn:
            conn.execute(query, (username, "none", lang))
            conn.commit()

    def get_top_users(self):
        """Pobiera 10 użytkowników z największą liczbą sesji (lub inną metryką)."""
        query = """
            SELECT username, COUNT(*) as session_count 
            FROM training_sessions 
            GROUP BY username 
            ORDER BY session_count DESC 
            LIMIT 10;
        """
        with self._get_connection() as conn:
            return conn.execute(query).fetchall()

    def seed_database(self):
        """Dodaje przykładowych użytkowników i sesje treningowe do testów."""
        users = [
            ("testowy1", self._hash_password("haslo1")),
            ("atleta_jan", self._hash_password("haslo2")),
            ("fit_anna", self._hash_password("haslo3")),
            ("basiek", self._hash_password("haslo4"))
        ]

        with self._get_connection() as conn:
            for user, pwd in users:
                conn.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?);", (user, pwd))

            sample_sessions = [("basiek",), ("basiek",), ("basiek",), ("atleta_jan",), ("fit_anna",), ("basiek",)]
            conn.executemany("INSERT INTO training_sessions (username) VALUES (?);", sample_sessions)

            conn.commit()
            print("Baza danych została uzupełniona przykładowymi danymi.")

    def save_training_session(self, username: str):
        """Zapisuje sesję treningową dla użytkownika."""
        query = "INSERT INTO training_sessions (username) VALUES (?);"
        with self._get_connection() as conn:
            conn.execute(query, (username,))
            conn.commit()