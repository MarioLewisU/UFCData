from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from pandas import Series
from datetime import datetime


def _parse_date(date_string: str | None):
    # Check for NaN values
    if (date_string is None):
        return

    formats = [
        '%B %d, %Y',
        '%b %d, %Y',
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue


class BaseModel(DeclarativeBase):
    @classmethod
    def from_csv_data(cls, data: Series):
        """
        Creates an instance of the model from raw csv data.
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement from_csv_data")


class ModelWithUrl:
    url = Column(String(128))


class EventModel(BaseModel, ModelWithUrl):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True)

    name = Column(String(128))
    date = Column(Date)
    location = Column(String(64))

    @classmethod
    def from_csv_data(cls, data: Series):
        return EventModel(
            name=data['name'],
            date=_parse_date(data['date']),
            location=data['location'],
            url=data['url']
        )


class FighterModel(BaseModel, ModelWithUrl):
    __tablename__ = 'fighters'

    fighter_id = Column(Integer, primary_key=True)

    first_name = Column(String(32))
    last_name = Column(String(32))
    nickname = Column(String(32), nullable=True)
    height = Column(String(16), nullable=True)
    weight = Column(String(16), nullable=True)
    reach = Column(String(16), nullable=True)
    stance = Column(String(16), nullable=True)
    dob = Column(Date, nullable=True)

    @classmethod
    def from_csv_data(cls, data: Series):
        return FighterModel(
            first_name=data['first'],
            last_name=data['last'],
            nickname=data['nickname'],
            height=data['height'],
            weight=data['weight'],
            reach=data['reach'],
            stance=data['stance'],
            dob=_parse_date(data['dob']),
            url=data['url']
        )


class FightModel(BaseModel, ModelWithUrl):
    __tablename__ = 'fights'

    fight_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey(EventModel.event_id))

    bout = Column(String(128))
    outcome = Column(String(8))
    weight_class = Column(String(128))
    method = Column(String(32))
    round = Column(Integer)
    time = Column(String(8))
    time_format = Column(String(32))
    referee = Column(String(32))
    details = Column(String(256))

    @classmethod
    def from_csv_data(cls, data: Series):
        return FightModel(
            bout=data['bout'],
            outcome=data['outcome'],
            weight_class=data['weightclass'],
            method=data['method'],
            round=data['round'],
            time=data['time'],
            time_format=data['time format'],
            referee=data['referee'],
            details=data['details'],
            url=data['url']
        )


class FightStatsModel(BaseModel):
    __tablename__ = 'fight_stats'

    fight_stats_id = Column(Integer, primary_key=True)
    fight_id = Column(Integer, ForeignKey(FightModel.fight_id))
    fighter_id = Column(Integer, ForeignKey(FighterModel.fighter_id))

    knockdowns = Column(Integer)
    submission_attempts = Column(Integer)
    reversals = Column(Integer)
    control_time = Column(String(8))
    takedowns = Column(Integer)
    takedowns_attempted = Column(Integer)

    total_strikes = Column(Integer)
    total_strikes_attempted = Column(Integer)
    sig_strikes = Column(Integer)
    sig_strikes_attempted = Column(Integer)
    head_strikes = Column(Integer)
    head_strikes_attempted = Column(Integer)
    body_strikes = Column(Integer)
    body_strikes_attempted = Column(Integer)
    leg_strikes = Column(Integer)
    leg_strikes_attemped = Column(Integer)
    distance_strikes = Column(Integer)
    distance_strikes_attempted = Column(Integer)
    clinch_strikes = Column(Integer)
    clinch_strikes_attempted = Column(Integer)
    ground_strikes = Column(Integer)
    ground_strikes_attemped = Column(Integer)

    @classmethod
    def from_csv_data(cls, data: Series):
        return FightStatsModel(
            knockdowns=data['knockdowns'],
            submission_attempts=data['submissionattempts'],
            reversals=data['reversals'],
            control_time=data['controltime'],
            takedowns=data['takedownshit'],
            takedowns_attempted=data['takedownsattempted'],
            total_strikes=data['totalstrikeshit'],
            total_strikes_attempted=data['totalstrikesattempted'],
            sig_strikes=data['sigstrikeshit'],
            sig_strikes_attempted=data['sigstrikesattempted'],
            head_strikes=data['headstrikeshit'],
            head_strikes_attempted=data['headstrikesattempted'],
            body_strikes=data['bodystrikeshit'],
            body_strikes_attempted=data['bodystrikesattempted'],
            leg_strikes=data['legstrikeshit'],
            leg_strikes_attemped=data['legstrikesattempted'],
            distance_strikes=data['distancehit'],
            distance_strikes_attempted=data['distanceattempted'],
            clinch_strikes=data['clinchhit'],
            clinch_strikes_attempted=data['clinchattempted'],
            ground_strikes=data['groundhit'],
            ground_strikes_attemped=data['groundattempted']
        )
