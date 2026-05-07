from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models import OptimizationJob


def test_database_models_create_with_sqlite():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    job = OptimizationJob(input_text="Hello", brief=None)
    db.add(job)
    db.commit()
    assert db.query(OptimizationJob).count() == 1
