import requests
from requests.exceptions import Timeout
from src.db import SessionLocal
from src.models import Problem  # Импортируем модель Problem


class CodeforcesParser:
    def get_problem(self, difficulty=None):
        url = "https://codeforces.com/api/problemset.problems"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return None
            data = response.json()
            if data["status"] != "OK":
                return None
            problems = data["result"]["problems"]
            if difficulty:
                problems = [p for p in problems if p.get("rating") == difficulty]
            return problems
        except Timeout:
            return None

    def parse_and_save(self):
        """
        Парсит задачи с Codeforces и сохраняет их в базу данных.
        """
        problems = self.get_problem()
        if not problems:
            return

        db = SessionLocal()
        try:
            for problem in problems:
                # Проверяем, существует ли задача в базе данных
                existing_problem = db.query(Problem).filter_by(
                    contest_id=problem["contestId"],
                    index=problem["index"]
                ).first()

                if not existing_problem:
                    # Создаем новую задачу
                    db_problem = Problem(
                        name=problem["name"],
                        contest_id=problem["contestId"],
                        index=problem["index"],
                        rating=problem.get("rating"),
                        tags=", ".join(problem["tags"]),
                    )
                    db.add(db_problem)
            db.commit()
        finally:
            db.close()