import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from rosalind.db.schema import Base

class RosalindDatabase:

    def __init__(self):
        if os.environ.get("RUNTIME_MODE") == "TEST":
            self._url = "postgresql://rosiland:minecraft@localhost:5432/rosiland_test"
        else:
            self._url = "postgresql://rosiland:minecraft@localhost:5432/rosiland"

        self.db_engine = create_engine(self._url)

        metadata = MetaData()
        metadata.reflect(self.db_engine)

        Base.metadata.create_all(self.db_engine)

        self.session_creator = sessionmaker(bind=self.db_engine)
