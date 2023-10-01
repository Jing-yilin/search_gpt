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
from src.search_utils import GoogleSearcher, GoogleLang

set_env()

lang_map = {
    "English(英语)": GoogleLang.en,
    "Spanish(西班牙语)": GoogleLang.es,
    "French(法语)": GoogleLang.fr,
    "German(德语)": GoogleLang.de,
    "Italian(意大利语)": GoogleLang.it,
    "Portuguese(葡萄牙语)": GoogleLang.pt,
    "Russian(俄语)": GoogleLang.ru,
    "Chinese(中文)": GoogleLang.zh,
    "Japanese(日语)": GoogleLang.ja,
    "Korean(韩语)": GoogleLang.ko,
    "Arabic(阿拉伯语)": GoogleLang.ar,
    "Hindi(印地语)": GoogleLang.hi,
    "Bengali(孟加拉语)": GoogleLang.bn,
}

if "state" not in st.session_state:
    st.session_state.state = 1
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "search_items" not in st.session_state:
    st.session_state.search_items = {}


def set_session_state(i: int):
    st.session_state.state = i


async def main():
    if st.session_state.state >= 1:
        st.title("Search the World!")

        search_word = st.text_input(
            "Please enter anthing in any language:", "Asia Game"
        )
        selected_langs = st.multiselect(
            "Please select languages:",
            lang_map.keys(),
            default=["English(英语)", "Chinese(中文)"],
            on_change=set_session_state,
            args=[1],
        )
        langs = [lang_map[lang] for lang in selected_langs]
        num = st.slider("Please select the number of search results:", 1, 50, 10)
        st.button("Search", on_click=set_session_state, args=[2])

    if st.session_state.state >= 2:
        if search_word:
            with st.spinner("Searching... "):
                with requests.Session() as session:
                    for lang in langs:
                        google_searcher = GoogleSearcher(
                            search_word, session, lang=lang, num=num
                        )
                        await google_searcher._google_search()
                        st.session_state.responses[lang] = google_searcher.response
                        st.session_state.search_items[
                            lang
                        ] = google_searcher.search_items

                set_session_state(3)

    if st.session_state.state >= 3:
        for lang in langs:
            st.header(f"Search Results [{lang}]")
            search_items = st.session_state.search_items[lang]
            for idx, item in search_items.items():
                st.markdown(
                    f"![]({item['logo']}) [{item['title']}]({item['url']})",
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    asyncio.run(main())
