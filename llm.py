from langchain_anthropic import ChatAnthropic

class NoterLLM:

    MODEL = "claude-3-haiku-20240307"
    MAX_TOKENS = 4096

    def __init__(self, tools):
        self.llm = ChatAnthropic(
            model=NoterLLM.MODEL,
            temperature=0,
            max_tokens=NoterLLM.MAX_TOKENS,
            timeout=None,
            max_retries=2,
            # other params...
        ).bind_tools(tools)

    def get_llm(self):
        return self.llm
        
    def get_init_prompt(self):
        return """
        You are Noter, a powerful LLM that manages notes for users in folders.
        If the folder is not known, use the 'default' folder.
        """
