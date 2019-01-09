import json
from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, JSONB, TEXT, UUID, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TypeDecorator, types



Base = declarative_base()

class Experiments(Base):
    __tablename__ = 'experiments'
    id = Column(UUID, index=True, primary_key=True)
    group_id = Column(UUID, index=True, nullable=False)
    model = Column(VARCHAR(30), index=True)
    env_id = Column(TEXT, index=True)
    status = Column(VARCHAR(30), index=True)
    pid = Column(INTEGER, index=True)
    current_timestep = Column(INTEGER, default=0, index=True)
    total_timesteps = Column(INTEGER, index=True)
    owner = Column(TEXT)
    start_date = Column(TIMESTAMP, default=func.now(), index=True)
    end_date = Column(TIMESTAMP, default=func.now(), index=True)
    updated_date = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), index=True)
    logs = Column(TEXT)
    model_params = Column(JSONB)

class Iterations(Base):
    __tablename__ = 'iterations'
    id = Column(UUID, index=True, primary_key=True)
    experiment_id = Column(VARCHAR(36), index=True)
    iteration = Column(INTEGER, index=True)
    num_episodes = Column(INTEGER, index=True)
    total_episodes = Column(INTEGER, index=True)
    num_timesteps = Column(INTEGER, index=True)
    total_timesteps = Column(INTEGER, index=True)
    average_reward = Column(INTEGER, index=True)
    info = Column(JSONB)

class AuthorizedUsers(Base):
    __tablename__ = 'authorized_users'
    id = Column(INTEGER, index=True, primary_key=True)
    name = Column(VARCHAR(100), index=True)
    role = Column(VARCHAR(30), index=True)
    chat_id = Column(INTEGER, index=True, primary_key=True)
    start_date = Column(TIMESTAMP, default=func.now(), index=True)
    updated_date = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), index=True)

class ClientPool(Base):
    __tablename__ = 'client_pool'
    address = Column(VARCHAR(100), index=True, primary_key=True)
    status = Column(VARCHAR(30), index=True)
    current_experiment = Column(UUID, index=True)
    start_date = Column(TIMESTAMP, default=func.now(), index=True)
    updated_date = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), index=True)