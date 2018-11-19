import json
from sqlalchemy import Column, String, DateTime, func
import sqlalchemy.dialects.sqlite as db_types
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TypeDecorator, types


class Json(TypeDecorator):

    @property
    def python_type(self):
        return object

    impl = types.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None


Base = declarative_base()

class Experiments(Base):
    __tablename__ = 'experiments'
    id = Column(db_types.CHAR(36), index=True, primary_key=True)
    group_id = Column(db_types.CHAR(36), index=True, nullable=False)
    model = Column(db_types.CHAR(30), index=True)
    env_id = Column(db_types.TEXT, index=True)
    status = Column(db_types.CHAR(30), index=True)
    pid = Column(db_types.INTEGER, index=True)
    current_timestep = Column(db_types.INTEGER, index=True)
    total_timesteps = Column(db_types.INTEGER, index=True)
    owner = Column(db_types.TEXT)
    start_date = Column(DateTime, default=func.now(), index=True)
    end_date = Column(DateTime, default=func.now(), index=True)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    logs = Column(db_types.TEXT)
    model_params = Column(Json)

class Iterations(Base):
    __tablename__ = 'iterations'
    id = Column(db_types.CHAR(36), index=True, primary_key=True)
    experiment_id = Column(db_types.CHAR(36), index=True)
    iteration = Column(db_types.INTEGER, index=True)
    num_episodes = Column(db_types.INTEGER, index=True)
    total_episodes = Column(db_types.INTEGER, index=True)
    num_timesteps = Column(db_types.INTEGER, index=True)
    total_timesteps = Column(db_types.INTEGER, index=True)
    average_reward = Column(db_types.INTEGER, index=True)
    info = Column(Json)

class AuthorizedUsers(Base):
    __tablename__ = 'authorized_users'
    id = Column(db_types.INTEGER, index=True, primary_key=True)
    name = Column(db_types.CHAR(100), index=True)
    role = Column(db_types.CHAR(30), index=True)
    chat_id = Column(db_types.INTEGER, index=True, primary_key=True)
    start_date = Column(DateTime, default=func.now(), index=True)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

class ClientPool(Base):
    __tablename__ = 'client_pool'
    address = Column(db_types.CHAR(50), index=True, primary_key=True)
    status = Column(db_types.CHAR(30), index=True)
    current_experiment = Column(db_types.CHAR(30), index=True)
    start_date = Column(DateTime, default=func.now(), index=True)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)