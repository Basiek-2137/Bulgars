import os
from google import genai
from pydantic import BaseModel


class CoachResponse(BaseModel):
    summary: str
    advice: str
    motivation: str

class GeminiCoach():
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyBlw4Gy2DHDnoCz26W0yBFu_AJSifthafU")
        self.client = genai.Client(api_key=api_key)

    def generate_workout_feedback(self, exercise_name, target_reps, completed_reps, errors_list):
        unique_errors = list(set(errors_list))
        errors_text = ", ".join(unique_errors) if unique_errors else "Brak błędów! Idealna technika."

        prompt = f"""
                Jesteś doświadczonym, wymagającym, ale wspierającym trenerem personalnym medycyny sportowej.
                Przeanalizuj zakończoną właśnie serię ćwiczenia i przygotuj krótką, dynamiczną informację zwrotną dla podopiecznego.

                Dane z treningu:
                - Ćwiczenie: {exercise_name}
                - Zaplanowane powtórzenia: {target_reps}
                - Wykonane powtórzenia: {completed_reps}
                - Wykryte błędy techniczne podczas serii: {errors_text}

                Napisz krótką wypowiedź (maksymalnie 4-5 zdań). Skup się na korekcie wykrytych błędów w przysiadzie bułgarskim 
                oraz daj kopa motywacyjnego na kolejną serię. Zwracaj się bezpośrednio do użytkownika.
                """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Błąd połączenia z trenerem AI: {str(e)}"

