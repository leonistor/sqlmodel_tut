from sqlmodel import Session
from models import Hero, Team
from database import engine

some_heroes = [
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
        for i in [1, 3, 5]:
            some_heroes[i].team = team_preventers
        for i in [2, 4]:
            some_heroes[i].team = team_z_force
        session.add_all(some_heroes)

        session.commit()
