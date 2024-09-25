-- class Note(Base):
--     __tablename__ = 'note'

--     id = Column(String, primary_key=True, default=uuid.uuid4)
--     username = Column(String)
--     foldername = Column(String)
--     created_on = Column(DateTime, default=func.now())
--     note = Column(String)

CREATE TABLE note (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR,
    foldername VARCHAR,
    created_on TIMESTAMP DEFAULT NOW(),
    note TEXT
);
