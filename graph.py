from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
from llm import NoterLLM

class ToolCall(TypedDict):
    name: str
    args: dict

class NoterState(TypedDict):
    user_prompt: str
    tool_call: ToolCall
    result: dict

class NoterNodeBuilder:
    def __init__(self, llm: NoterLLM):
        self.llm = llm

    def build_llm_node(self):

        def llm_node(state: NoterState):
            messages = [
                ("system", self.llm.get_init_prompt()),
                ("human", state["user_prompt"]),
            ]
            ai_msg = self.llm.get_llm().invoke(messages)
            if ai_msg.tool_calls is not None:
                tool_call = ai_msg.tool_calls[0]
                print("Returning tool call", tool_call)
                return {
                    "tool_call": tool_call,
                }
            print("I'm not sure what you mean")
            return {
                "result": "I'm not sure what you mean"
            }
        return llm_node


def create_graph(llm: NoterLLM) -> StateGraph:
    graph_builder = StateGraph(NoterState)
    node_builder = NoterNodeBuilder(llm)
    
    llm_node = node_builder.build_llm_node()

    graph_builder.add_node(llm_node)
    graph_builder.add_edge(START, "llm_node")
    
    graph = graph_builder.compile()
    return graph


