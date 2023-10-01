from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent))


def get_chatgpt_chain(temperature=0.0, verbose=True, k=2):
    """Create a chatgpt chain.

    Args:
        temperature (float): The temperature to use for the language model. Defaults to 0.0.
        verbose (bool): Whether to print the output of the chain. Defaults to True.
        k (int): The number of messages to use for the language model. Defaults to 2.

    Returns:
        ConversationChain: The chatgpt chain.

    Examples:
        >>> from src.chat_model.conversation_chains import get_chatgpt_chain
        >>> chain = get_chatgpt_chain(temperature=0.0, verbose=True, k=2)
        >>> chain.predict(human_input="What is the main idea of the report?")
    """

    llm = OpenAI(temperature=temperature)

    template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    {history}
    Human: {human_input}
    Assistant:"""
    prompt = PromptTemplate(
        input_variables=["history", "human_input"], template=template
    )

    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=verbose,
        memory=ConversationBufferWindowMemory(k=k),
    )

    return chatgpt_chain
