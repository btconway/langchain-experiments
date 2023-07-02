from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import OpenAIEmbeddings
import logging
import langchain
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.cache import SQLiteCache
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

def chat_interactive(user_input, model_name="claude-v1.3-100k", temperature=0.4, max_tokens_to_sample=75000, streaming=True, verbose=False):
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Replace RedisSemanticCache with SQLiteCache
    langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

    # Read the prompt template from a .txt file
    with open('Anthropic_Prompt.txt', 'r') as file:
        template = file.read()


    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )

    # Initialize the memory
    memory = ConversationBufferMemory(memory_key="chat_history")

    # Initialize the LLMChain with the ChatAnthropic model
    llm_chain = LLMChain(
        llm=ChatAnthropic(
            model=model_name,
            temperature=temperature,
            max_tokens_to_sample=max_tokens_to_sample,
            streaming=streaming,
            verbose=verbose,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        ),
        prompt=prompt,
        verbose=verbose,
        memory=memory,
    )

    # Interactive chat
    if user_input.lower() == "quit":
        return "Chat ended"
    response = llm_chain.predict(human_input=user_input)
    return response
