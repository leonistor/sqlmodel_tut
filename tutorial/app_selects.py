from sqlmodel import Session, col, select

from .database import create_db_and_tables, engine
from .models import Hero, Team


more_heroes = [
    Hero(name="Deadpond", secret_name="Dive Wilson"),
    Hero(name="Spider-Boy", secret_name="Pedro Parqueador"),
    Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48),
    Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32),
    Hero(name="Black Lion", secret_name="Trevor Challa", age=35),
    Hero(name="Dr. Weird", secret_name="Steve Weird", age=36),
    Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93),
]


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_1 = Hero(name="Ana Coca", secret_name="Pizdoasa", team=team_z_force)
        hero_2 = Hero(
            name="Nutzi Shefa",
            secret_name="Marioara Cur de Fier",
            team=team_preventers,
        )
        hero_3 = Hero(
            name="Bijboaca",
            secret_name="Zemoasa",
            team=team_z_force,
        )
        hero_robo = Hero(
            name="Robo-Pula",
            secret_name="Robotic Dildo",
            age=48,
            team=team_preventers,
        )
        hero_zdreantza = Hero(
            name="Zdreantza",
            secret_name="Carpeta murdara",
            team=team_preventers,
        )

        session.add(hero_1)
        session.add_all([hero_2, hero_3])
        session.add_all(more_heroes)
        session.add_all([hero_robo, hero_zdreantza])

        session.commit()


def select_heroes():
    with Session(engine) as session:
        stmt = select(Hero).where(col(Hero.age) >= 35)
        results = session.exec(stmt)
        print("--- for:")
        for hero in results:
            print(hero)


def select_one():
    with Session(engine) as session:
        # stmt = select(Hero).where(col(Hero.name) == "Bijboaca")
        # results = session.exec(stmt)
        # bijboaca = results.one()
        bijboaca = session.exec(select(Hero).where(Hero.name == "Bijboaca")).one()
        print(bijboaca)
        # select by id -> get
        coca = session.get(Hero, 1)
        print(coca)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print(f"to be updated: {hero}")

        hero.age = 16
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print(f"just updated: {hero}")


def select_joins():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        print(f"----- joins!")
        for hero, team in results:
            print(f"Hero: {hero} | Team: {team}")


def main():
    create_db_and_tables()
    create_heroes()
    # select_heroes()
    select_one()
    update_heroes()
    select_joins()


if __name__ == "__main__":
    main()
