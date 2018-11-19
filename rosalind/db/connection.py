import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from rosalind.db.schema import Base

class ExperimentResultsDatabase:

    db_name = "experiments"

    def __init__(self):

        path = os.path.dirname(os.path.realpath(__file__))

        self._url = "sqlite:///{}.db".format(os.path.join(path, self.db_name))

        self.db_engine = create_engine(self._url)

        metadata = MetaData()
        metadata.reflect(self.db_engine)

        Base.metadata.create_all(self.db_engine)

        self.session_creator = sessionmaker(bind=self.db_engine)
