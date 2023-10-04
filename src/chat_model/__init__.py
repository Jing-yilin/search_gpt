"""
chat_model package.
"""

from .conversation_chains import get_conversation_chain
from .llms import get_llm, suppotred_llm_models
from .prompts import SEARCH_LANGS_TEMPLATE, TRANSLATE_TEMPLATE

__version__ = "0.1.0"

__all__ = [
    "get_conversation_chain",
    "get_llm",
    "suppotred_llm_models",
    "SEARCH_LANGS_TEMPLATE",
    "TRANSLATE_TEMPLATE",
]