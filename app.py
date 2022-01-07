from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse

import dominate
from dominate.tags import link, div, attr, p, a, ol, li, section, hr

from debug_toolbar.middleware import DebugToolbarMiddleware

from sqlmodel import Session, select
from typing import List, Optional

from models import (
    Hero,
    HeroCreate,
    HeroRead,
    HeroReadWithTeam,
    HeroUpdate,
    TeamReadWithHeroes,
)
from models import Team, TeamCreate, TeamRead, TeamUpdate
from database import create_db_and_tables, engine
from seed import create_heroes


app = FastAPI(debug=True)
# app.add_middleware(DebugToolbarMiddleware)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_heroes()


# ---
@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, lte=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero {hero_id} not found",
        )
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
    hero: HeroUpdate,
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero {hero_id} not found",
        )
    hero_data = hero.dict(exclude_unset=True)
    for key, val in hero_data.items():
        setattr(db_hero, key, val)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero {hero_id} not found",
        )
    session.delete(hero)
    session.commit()
    return {"ok": True}


# ---


@app.post("/teams/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=List[TeamRead])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamReadWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}


# ---

# test html


@app.get("/hello/{n}", response_class=HTMLResponse)
async def hello(n: int = 10):
    """dominate html generation"""
    doc = dominate.document(title="Hello, Zuza!")
    with doc:
        with div(id="header").add(ol()):
            for i in ["home", "about", "contact"]:
                li(a(i.title(), href="/%s.html" % i))
        with div():
            attr(cls="body")
            p("Lorem ipsum..")
        with section():
            p(f"ana are {n} mere")
    doc.add(hr())
    return doc.render(pretty=True)
