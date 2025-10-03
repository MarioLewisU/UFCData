import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, OperationalError
from database.models  import *

__all__ = ['load_database']

try:
    # Try to connect to 'ufc_data'
    engine = create_engine(
        'postgresql://postgres:0000@localhost:5432/UFCData')
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Connected to database 'UFCData'")
except (ProgrammingError, OperationalError):
    print("Could not connect to database 'UFCData', creating...")

    temp_engine = create_engine(
        'postgresql://postgres:0000@localhost:5432/UFCData')
    with temp_engine.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text("CREATE DATABASE UFCData"))

    engine = create_engine(
        'postgresql://postgres:0000@localhost:5432/UFCData')

    print("Created and connected to database 'UFCData'")


def load_database():
    __prep_database()
    __load_events()
    __load_fighters()
    __load_fights()
    __load_fight_stats()


def __prep_database():
    """
    Prepare the database by creating the schema.
    """

    print("Dropping current schema.")

    # Drop all tables
    BaseModel.metadata.drop_all(engine)

    # Create all tables
    BaseModel.metadata.create_all(engine)

    print("Created new schema")


def __load_events():
    """
    Load raw event data into the database
    """

    print("Loading events...")

    df_events = pd.read_csv('out/events.csv')

    with Session(engine) as session:
        event_entities = [EventModel.from_csv_data(
            data) for _, data in df_events.iterrows()]
        event_entities.reverse()

        session.add_all(event_entities)
        session.commit()


def __load_fighters():
    """
    Load raw fighter data into the database
    """

    print("Loading fighters...")

    df_fighters = pd.read_csv('out/fighters.csv')
    df_fighters.replace({np.nan: None}, inplace=True)

    with Session(engine) as session:
        event_entities = [FighterModel.from_csv_data(
            data) for _, data in df_fighters.iterrows()]

        session.add_all(event_entities)
        session.commit()


def __load_fights():
    """
    Load raw fighter data into the database
    """

    print("Loading fights...")

    df_fights = pd.read_csv('out/fights.csv')
    df_fights.replace({np.nan: None}, inplace=True)

    for _, data in df_fights.iterrows():
        fight_entity = FightModel.from_csv_data(data)
        event_name: str | None = data['event']

        if not event_name:
            print("Skipping fight with no event: ", fight_entity.url)
            continue

        event_name = event_name.strip()

        with Session(engine) as session:
            res = session.execute(select(EventModel).where(
                EventModel.name == event_name)).first()

            if not res:
                print("Could not find event for fight, skipping: ", fight_entity.url)
                continue

            event: EventModel = res[0]
            fight_entity.event_id = event.event_id

            session.add(fight_entity)
            session.commit()


def __load_fight_stats():
    """
    Load raw fight stats data into the database
    """

    print("Loading fight stats...")

    df_fight_stats = pd.read_csv('out/fight_stats.csv')
    df_fight_stats.replace({np.nan: None}, inplace=True)

    for _, data in df_fight_stats.iterrows():
        fight_stats_entity = FightStatsModel.from_csv_data(data)
        bout_name: str | None = data['bout']
        fighter_name: str | None = data['fighter']

        if not bout_name or not fighter_name:
            print("Skipping fight stats with no bout or fighter")
            continue

        bout_name = bout_name.strip()
        fighter_name = fighter_name.strip()

        with Session(engine) as session:
            res = session.execute(select(FightModel).where(
                FightModel.bout == bout_name)).first()

            if not res:
                print("Could not find fight for fight stats, skipping")
                continue

            fight: FightModel = res[0]

            res = session.execute(select(FighterModel).where(
                FighterModel.first_name + ' ' + FighterModel.last_name == fighter_name)).first()

            if not res:
                print("Could not find fighter for fight stats, skipping")
                continue

            fighter: FighterModel = res[0]

            fight_stats_entity.fight_id = fight.fight_id
            fight_stats_entity.fighter_id = fighter.fighter_id

            session.add(fight_stats_entity)
            session.commit()
