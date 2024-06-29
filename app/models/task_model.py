from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base, engine

class Task(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(60))
    description = Column(String(65))
    status = Column(String(25))
    created_at = Column(DateTime)

    def __repr__(self):
        return f'<Task(id={self.id}, title={self.title}, description={self.description}, status={self.status}, created_at={self.created_at}>'

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
