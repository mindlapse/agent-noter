import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = 'note'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String)
    foldername = Column(String)
    created_on = Column(DateTime, default=func.now())
    note = Column(String)


class NoteService:
    
    def create_note(self, session, username, foldername, note) -> str:
        new_note = Note(username=username, foldername=foldername, note=note)
        session.add(new_note)
        session.commit()
        return new_note.id
    
    def read_note(self, session, note_id):
        note = session.query(Note).get(note_id)
        return note
    
    def update_note(self, session, note_id, new_note):
        note = session.query(Note).get(note_id)
        note.note = new_note
        session.commit()
    
    def delete_note(self, session, note_id):
        note = session.query(Note).get(note_id)
        session.delete(note)
    
    def list_notes(self, session, username, foldername):
        notes = session.query(Note).filter_by(username=username, foldername=foldername).all()
        return notes
    
    def list_folders(self,session,  username):
        folders = session.query(Note.foldername).filter_by(username=username).distinct().all()
        return [folder[0] for folder in folders]