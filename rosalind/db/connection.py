import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from rosalind.db.schema import Base

class ExperimentResultsDatabase:

    def __init__(self):

        self._url = "postgresql://rosiland:minecraft@localhost:5432/rosiland"

        self.db_engine = create_engine(self._url)

        metadata = MetaData()
        metadata.reflect(self.db_engine)

        Base.metadata.create_all(self.db_engine)

        self.session_creator = sessionmaker(bind=self.db_engine)
