from langchain.tools import tool;
from notes import NoterService
from db import DB

class NoterTools:

    def __init__(self, note_service: NoterService, db: DB):
        self.note_service = note_service
        self.db = db

    def get_all_tools(self):
        return [
            self.build_create_note_tool(),
            self.build_list_notes(),
            self.build_delete_note(),
        ]

    def build_create_note_tool(self):

        @tool
        def create_note(user: str, note: str, folder: str):
            """Creates the given note for the user in a folder."""
            
            print("Creating note...")
            session = self.db.get_session()
            id = self.note_service.create_note(session, user, folder, note)
            session.commit();
            session.close();
            return {
                "note_id": id,
            }
        return create_note
    

    def build_list_notes(self):

        @tool
        def list_notes(user: str, folder: str):
            """Lists notes for the user in a folder."""
            
            print("Listing notes...")
            session = self.db.get_session()
            notes = self.note_service.list_notes(session, user, folder)
            session.close()
            return {
                "notes": [note.to_dict() for note in notes],
            }
        return list_notes
    
    def build_delete_note(self):
            
            @tool
            def delete_note(user: str, note_id: str):
                """Deletes the note with the given id."""
                
                print("Deleting note...")
                session = self.db.get_session()
                self.note_service.delete_note(session, note_id)
                session.commit()
                session.close()
                return {
                    "note_id": note_id,
                }
            return delete_note
    
    