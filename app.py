"""
This program aims to search the input word in the main languages of the world, like English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and Bengali.
1. translate the input word into the main languages of the world
2. search each language using google, bing, duckduckgo, and baidu
3. return the search results
4. use LLM to conclude the results
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from time import time
import asyncio

from src.common_utils import set_env
from src.search_utils import GoogleSearcher, hl_map
from src.llm_utils import (
    get_translated_titles,
    get_keywords_langs,
    ALL_MODELS,
)

set_env()


def set_session_state(i: int):
    st.session_state.state = i


async def main():
    if "state" not in st.session_state:
        st.session_state.state = 1
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "search_items" not in st.session_state:
        st.session_state.search_items = {}

    if st.session_state.state >= 1:
        st.title("Search the World!")
        search_word = st.text_input(
            "Please enter anthing in any language:",
            "巴以冲突",
            on_change=set_session_state,
            args=[1],
        )
        selected_langs = st.multiselect(
            "Please select languages:",
            hl_map.keys(),
            default=["Chinese (Simplified)", "English", "Korean"],
            on_change=set_session_state,
            args=[1],
        )
        target_language = st.selectbox(
            "Please select the target language:",
            hl_map.keys(),
            index=list(hl_map.keys()).index("Chinese (Simplified)"),
            on_change=set_session_state,
            args=[1],
        )
        model_name = st.selectbox(
            "Please select the language model:",
            ALL_MODELS,
            index=ALL_MODELS.index("gpt-3.5-turbo-instruct"),
            on_change=set_session_state,
            args=[1],
        )
        langs = [hl_map[lang] for lang in selected_langs]
        num = st.slider(
            "Please select the number of search results:",
            1,
            50,
            10,
            on_change=set_session_state,
            args=[1],
        )
        st.button("Search", on_click=set_session_state, args=[2])

    if st.session_state.state >= 2:
        if search_word:
            with st.spinner("Searching... "):
                keywords_langs = get_keywords_langs(
                    search_word, selected_langs, model_name
                )
                print(f"keywords_langs: {keywords_langs}")
                with requests.Session() as session:
                    for idx, lang in enumerate(langs):
                        google_searcher = GoogleSearcher(
                            keywords_langs[idx], session, lang=lang, num=num
                        )
                        await google_searcher._google_search()
                        st.session_state.responses[lang] = google_searcher.response
                        st.session_state.search_items[lang] = google_searcher.search_items
                        # sleep
                        await asyncio.sleep(0.5)

                set_session_state(3)

    if st.session_state.state >= 3:
        for lang_idx, lang in enumerate(langs):
            st.header(f"Search Results [{lang}]")
            search_items = st.session_state.search_items[lang]
            titles = [item["title"] for item in search_items.values()]
            print(f"titles: {titles}")
            # Chinese (Simplified) -> Chinese (Simplified)
            translated_titles = (
                titles
                if target_language == selected_langs[lang_idx]
                else get_translated_titles(titles, target_language, model_name)
            )
            # add translated titles to search_items
            for idx, item in search_items.items():
                item["translated_title"] = translated_titles[idx]

            for idx, item in search_items.items():
                st.checkbox(
                    label=f"![]({item['logo']}) [{item['translated_title']}]({item['url']})",
                    value=False,
                )


if __name__ == "__main__":
    asyncio.run(main())
