import pathlib
import sys
import os

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

from chat_model.conversation_chains import get_chatgpt_chain

OPENAI_API_KEY="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"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def test_get_chatgpt_chain():
    chain = get_chatgpt_chain(
        temperature=0.0, verbose=True, k=2
    )

    answer = chain.predict(human_input="What is the main idea of the report?")
    assert answer is not None
