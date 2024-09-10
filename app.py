from flask import Flask, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool;
from notes import NoteService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "claude-3-haiku-20240307"

app = Flask(__name__)

llm = ChatAnthropic(
    model=MODEL,
    temperature=0,
    max_tokens=4096,
    timeout=None,
    max_retries=2,
    # other params...
)

note_service = NoteService()
db_username = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_host = os.environ.get("POSTGRES_HOST")
db_port = os.environ.get("POSTGRES_PORT")
db_name = os.environ.get("POSTGRES_DBNAME")

db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


@tool
def create_note(user: str, note: str, folder: str):
    """Creates the given note for the user in a folder."""
    print("Creating note...")
    session = Session() 
    id = note_service.create_note(session, user, folder, note)
    session.commit();
    session.close();
    return {
        "note_id": id,
    }

llm_with_tools = llm.bind_tools([create_note])

@app.route('/', methods=['POST'])
def prompt():
    request_data = request.get_json()

    messages = [
        (
            "system",
            """
            You are Noter, a powerful LLM that manages notes for users in folders.
            If the folder is not known, use the 'default' folder.
            """
            ,
        ),
        ("human", request_data["prompt"]),
    ]
    ai_msg = llm_with_tools.invoke(messages)

    print(ai_msg)
    if ai_msg.tool_calls is not None:
        tool_call = ai_msg.tool_calls[0]
        if tool_call["name"] == "create_note":
            result = create_note.invoke(tool_call["args"])
            print(result)
            
    return jsonify({ "reply": ai_msg.content })


if __name__ == '__main__':
    app.run(port=8888)
