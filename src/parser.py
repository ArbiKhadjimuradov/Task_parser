import requests
from sqlalchemy.orm import Session
from .models import Problem, Contest, Tag
from .db import SessionLocal


class CodeforcesParser:
    def __init__(self):
        self.base_url = "https://codeforces.com/api"

    def fetch_problems(self):
        response = requests.get(f"{self.base_url}/problemset.problems")
        data = response.json()
        return data['result']['problems'], data['result']['problemStatistics']

    def parse_and_save(self):
        db = SessionLocal()
        try:
            problems, stats = self.fetch_problems()
            for p, stat in zip(problems, stats):
                contest = db.query(Contest).filter_by(contest_id=p['contestId']).first()
                if not contest:
                    contest = Contest(contest_id=p['contestId'])
                    db.add(contest)
                    db.commit()

                problem = db.query(Problem).filter_by(
                    contest_id=contest.contest_id,
                    index=p['index']
                ).first()

                if not problem:
                    problem = Problem(
                        contest_id=contest.contest_id,
                        name=p['name'],
                        rating=p.get('rating'),
                        solved_count=stat['solvedCount'],
                        index=p['index']
                    )
                    db.add(problem)
                    db.commit()  # Сохраняем задачу, чтобы получить её ID

                # Добавляем теги
                for tag_name in p['tags']:
                    tag = db.query(Tag).filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.add(tag)
                        db.commit()  # Сохраняем тег, чтобы получить его ID

                    # Проверяем, что тег ещё не связан с задачей
                    if tag not in problem.tags:
                        problem.tags.append(tag)

                db.commit()
        except Exception as e:
            db.rollback()  # Откатываем транзакцию в случае ошибки
            raise e
        finally:
            db.close()