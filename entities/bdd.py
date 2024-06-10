from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./game.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

user_game = Table('user_game', Base.metadata,
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('game_id', Integer, ForeignKey('games.id'))
                  )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=True)

    games = relationship("Game", secondary=user_game, back_populates="users")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)

    users = relationship("User", secondary=user_game, back_populates="games")


Base.metadata.create_all(bind=engine)
