import pathlib
import sys
import os

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent.parent))

from chat_model.conversation_chains import get_conversation_chain
from chat_model.prompts import SEARCH_LANGS_TEMPLATE
from common_utils import set_env

set_env()

def test_get_conversation_chain():
    chain = get_conversation_chain(
        model_name="gpt-3.5-turbo-instruct",
        temperature=0.0,
        verbose=False,
        k=2,
        prompt=SEARCH_LANGS_TEMPLATE,
    )

    answer = chain.predict(keywords="Apple15ProMax", target_languages='["Esperanto", "Estonian", "Russian"]')
    assert answer is not None
