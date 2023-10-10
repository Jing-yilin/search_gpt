import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from .chat_model.prompts import TRANSLATE_TEMPLATE, SEARCH_LANGS_TEMPLATE
from .chat_model.conversation_chains import get_conversation_chain


def get_translated_titles(
    titles: list,
    target_language: str,
    model_name: str,
    temperature=0.0,
    verbose: bool = False,
):
    limit = 10
    translated_titles = []
    try:
        translate_chain = get_conversation_chain(
            model_name=model_name,
            temperature=temperature,
            verbose=verbose,
            k=2,
            prompt=TRANSLATE_TEMPLATE,
        )
        for i in range(0, len(titles), limit):
            translated_titles += (
                translate_chain.predict(
                    sentences="\n".join(titles[i : i + limit]),
                    target_language=target_language,
                )
                .replace("```", "")
                .strip()
                .split("\n")
            )
        print(f"translated_titles: \n{translated_titles}")
    except Exception as e:
        print(f"Error: {e}")
        translated_titles = titles
    return translated_titles


def get_keywords_langs(
    keywords: str,
    target_languages: list,
    model_name: str,
    temperature=0.0,
    verbose: bool = False,
) -> list:
    serach_chain = get_conversation_chain(
        model_name=model_name,
        temperature=temperature,
        verbose=verbose,
        k=2,
        prompt=SEARCH_LANGS_TEMPLATE,
    )
    keywords_langs = serach_chain.predict(
        keywords=keywords, target_languages=str(target_languages)
    )
    keywords_langs = keywords_langs.strip().split("\n")
    return keywords_langs
