from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

# base class for all ORM models
Base = declarative_base()

class TrainingData(Base):
    """
    ORM model for the training data.
    """
    __tablename__ = "training_data"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)

class IdealFunctions(Base):
    """
    ORM model for the ideal functions.
    """
    __tablename__ = "ideal_functions"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y_values = Column(String)

class TestData(Base):
    """
    ORM model for the test data.
    """
    __tablename__ = "test_data"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)

class MappedTestData(Base):
    """
    ORM model for the mapped test data.
    """
    __tablename__ = "mapped_test_data"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    ideal_function = Column(Integer)
    deviation = Column(Float)

class DatabaseHandler:
    """
    Handles database connections and sessions.
    """
    def __init__(self, db_filename):
        self.engine = create_engine(f'sqlite:///{db_filename}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """
        Creates and returns a new session.
        """
        return self.Session()