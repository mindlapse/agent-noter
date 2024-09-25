from flask import Flask, request, jsonify
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from tools import NoterTools
from notes import NoterService
from db import DB
from llm import NoterLLM
from graph import create_graph
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

db = DB()
noter_svc = NoterService()
noter_tools = NoterTools(noter_svc, db)
noter_llm = NoterLLM(noter_tools.get_all_tools())
graph = create_graph(noter_llm)

# llm_with_tools = llm.bind_tools([
#     create_note_tool,
#     list_notes_tool,
#     delete_note_tool,
# ])

# def get_system_prompt():
#     return """
#     You are Noter, a powerful LLM that manages notes for users in folders.
#     If the folder is not known, use the 'default' folder.
#     """

@app.route('/', methods=['POST'])
def prompt():
    request_data = request.get_json()

    user = request.get_json().get("user")
    # user = request_data["user"]
    if user is None:
        return jsonify({ "error": "Must provide 'user' and 'prompt'." })

    state = graph.invoke({
        "user_prompt": request_data["prompt"],
        "tool_call": None,
        "result": None,
    })

    print("Resulting state", state)

    # print(ai_msg)
    # if ai_msg.tool_calls is not None:
    #     tool_call = ai_msg.tool_calls[0]
    #     if tool_call["name"] == "create_note":
    #         result = create_note_tool.invoke(tool_call["args"])
    #         print(result)
    #     if tool_call["name"] == "list_notes":
    #         result = list_notes_tool.invoke(tool_call["args"])
    #         print(result)
    #     if tool_call["name"] == "delete_note":
    #         result = delete_note_tool.invoke(tool_call["args"])
    #         print(result)
            
    return jsonify({ "state": state })


if __name__ == '__main__':
    app.run(port=8888)
